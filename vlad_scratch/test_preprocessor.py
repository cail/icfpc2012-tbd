from world import World

from preprocessor import reachability_step, stone_reachability_step

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
        
        if expected != reachable:
            if not verbose:
                print '-'*10
                print test
                print data_to_string(width, reachable)
            print 'fail, expected'
            print data_to_string(width, expected)
            fails += 1
            
    assert fails == 0, fails
    print 'ok'
            
            
if __name__ == '__main__':
    
    def bool_to_01(b):
        return {False:'0', True:'1'}[b]
    def bool_step_to_01(step):
        return lambda w, h: map(bool_to_01, step(w, h))
    
    print 'reachability'
    test_processing_step(reachability_tests, bool_step_to_01(reachability_step))
    
    print 'stone reachability'
    test_processing_step(stone_reachability_tests, bool_step_to_01(stone_reachability_step))
    # because currently imprecise (but correct version) is used
    
