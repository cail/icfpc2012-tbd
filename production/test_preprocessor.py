
from world import World

from preprocessor import reachability_step, stone_reachability_step, preprocess_world

from preprocessor_tests import reachability_tests, stone_reachability_tests



def parse_result(s):
    lines = s.split('\n')
    assert lines[0] == ''
    del lines[0]
    assert all(len(lines[0]) == len(line) for line in lines)
    width = len(lines[0])
    #data = sum(map(list, lines), [])
    data = ['0']*(width+2) + [c for line in lines for c in '0'+line+'0'] + ['0']*(width+2)
    return width+2, data


def data_to_string(width, data):
    lines = []
    for i in range(0, len(data), width):
        lines.append(''.join(data[i:i+width]))
    return '\n'.join(lines)

   
def test_processing_step(tests, step, verbose=False):
    fails = 0
    for test, result in tests:
        if verbose:
            print '-'*10
            print test
        assert test.startswith('\n')
        test = test[1:]
        world = World.from_string(test)
        width = world.width
        data = world.data
        
        reachable = step(width, data)
        
        if verbose:
            print data_to_string(width, reachable)
        
        w, expected = parse_result(result)
        
        assert w == width
        assert len(expected) == len(data), (len(expected), len(data))
        
        expected_bool = [{'0':False, '1':True}[e] for e in expected]
        actual_string = [{False:'0', True:'1'}[e] for e in reachable]
        
        if expected_bool != reachable:
            if not verbose:
                print '-'*10
                print test
                print data_to_string(width, actual_string)
            print 'fail, expected'
            print data_to_string(width, expected)
            fails += 1
            
    assert fails == 0, fails
    print 'ok'
    
    
def check_preprocessor(world, commands, verbose=True):
    
    w1 = world
    w2 = preprocess_world(w1)
    n = 0
    for cmd in commands:
        pw1 = w1
        pw2 = w2
        w1 = w1.apply_command(cmd)
        w2 = w2.apply_command(cmd)
        n += 1
        
        if w1.terminated or w2.terminated:
            break
        
    t1 = w1.terminated, w1.score
    t2 = w2.terminated, w2.score
    
    if t1 != t2:
        print
        pw1.show()
        pw2.show()
        print
        w1.show()
        print t1
        w2.show()
        print t2
        print commands[:n]
        
        assert False
    
    
def fuzzy_tests():
    from glob import glob
    from random import choice, randrange, seed
    
    seed(666)
    
    print 'preprocessor fuzzy tests:'
    
    maps = []
    maps += glob('../data/sample_maps/trampoline*.map')
    maps += glob('../data/sample_maps/contest*.map')
    maps += glob('../data/sample_maps/flood*.map')
    maps += glob('../data/maps_manual/*.map')
    
    exclude = ['abort_immediately', 'tricky']
    
    for map_path in maps:
        print map_path,
        if any(e in map_path for e in exclude):
            print 'ignored'
            continue
        world = World.from_file(map_path)
        
        for i in range(50):
            commands = ''.join(choice('LRUDW') for _ in range(randrange(1000)))
            check_preprocessor(world, commands, verbose=False)
            if i % 10 == 0:
                print '.',
        print
        
    print 'fuzzy tests ok'
            
            
if __name__ == '__main__':
    
    print 'reachability step tests'
    test_processing_step(reachability_tests, reachability_step)
    
    print 'stone reachability step tests'
    test_processing_step(stone_reachability_tests, stone_reachability_step)
    
    #exit()
    
    fuzzy_tests()
