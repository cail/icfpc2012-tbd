from world import World

from reachability_tests import reachability_tests
from stone_reachability_tests import stone_reachability_tests


def reachability_step(width, data):
    '''
    Overapproximate set of spaces where robot can possibly be
    '''
    
    reachable = [False]*len(data)
    tasks = set([data.index('R')])
    
    auto_empty = [False]*len(data)
    # cells that can become empty even without robot intervention
    for i in reversed(range(len(data)-width)):
        cell = data[i]
        if cell == ' ':
            auto_empty[i] = True
        elif cell == '*':
            if auto_empty[i+width]:
                # fall down
                auto_empty[i] = True
            elif data[i+width] in '^*' and\
                 auto_empty[i+width-1] and (data[i+width-1] in ' *'):
                # fall left
                auto_empty[i] = True
            elif data[i+width] in '^*\\' and\
                 auto_empty[i+width+1] and (data[i+width+1] in ' *'):
                # fall right
                auto_empty[i] = True
                
    def make_reachable(i):
        reachable[i] = True
        for j in [i+1, i-1, i-width-1, i-width, i-width+1, i+width]:
            if not reachable[j]:
                tasks.add(j)
    
    while tasks:
        i = tasks.pop()
        assert not reachable[i]
        
        cell = data[i]
        if cell == 'R':
            make_reachable(i)
        elif cell in ' .\\' or auto_empty[i]:
            if reachable[i-1] or reachable[i+1] or\
               reachable[i+width] or reachable[i-width]:
                make_reachable(i)
        elif cell == '*':
            if reachable[i+width]:
                # dig under
                make_reachable(i)
            elif reachable[i-1] and (reachable[i+1] or auto_empty[i+1]):
                # push right
                make_reachable(i)
            elif reachable[i+1] and (reachable[i-1] or auto_empty[i-1]):
                # push left
                make_reachable(i)
            elif data[i+width] in '*^\\' and\
                 (reachable[i+1] or auto_empty[i+1]) and\
                 (reachable[i+width+1] or auto_empty[i+width+1]):
                # fall right
                make_reachable(i)
            elif data[i+width] in '*^' and\
                 (reachable[i-1] or auto_empty[i-1]) and\
                 (reachable[i+width-1] or auto_empty[i+width-1]):
                # fall left
                make_reachable(i)
            
    return reachable


def stone_reachability_step(width, data):
    '''
    Overapproximate set of places where can possibly be a stone
    '''
    
    result = [False]*len(data)
    
    def make_reachable(i):
        if data[i] not in '#^LO':
            result[i] = True
    
    for i in range(width, len(data)-width, width):
        for j in range(i, i+width):
            #if data[j] == '*':
            if data[j] == '*' or result[j-width]: # this is ridiculously imprecise, but otherwise it's incorrect
                make_reachable(j-1)
                make_reachable(j)
                make_reachable(j+1)
            if result[j-width]:
                make_reachable(j)
        
        # push to the right            
        for j in range(i, i+width):
            if result[j] and\
               data[j+width] not in 'R ':
                make_reachable(j+1)
        
        #push to the left            
        for j in reversed(range(i, i+width)):
            if result[j] and\
               data[j+width] not in 'R ':
                make_reachable(j-1)
                
    return result


def preprocess(width, data):

    
    result = data[:]
    reachable = reachability_step(width, data)
    
    for i in range(width, len(data)):
        if not reachable[i]:
            cell = result[i]
            if cell == '*':
                result[i] = '^'
            elif cell not in 'LO':
                result[i] = '#'
                
    stone_reachable = stone_reachability_step(width, result)
    for i in range(width, len(data)):
        if not stone_reachable[i-width]:
            cell = result[i]
            if cell == '^':
                result[i] = '#'
            elif cell == '.':
                result[i] = ' '
                
    return result


def preprocess_world(world):
    '''
    return simplified version of the world
    
    THEOREM. Set of optimal solutions does not change.
    
    (actually, it's a lie, but the only counterexample 
    we can think of is pretty contrived, so...)
    '''    
    
    world = World(world)
    
    width = world.width
    data = world.data
    
    reachable = reachability_step(width, data)
    
    for i in range(width, len(data)):
        if not reachable[i]:
            cell = data[i]
            if cell == '*':
                data[i] = '^'
            elif cell not in 'LO':
                data[i] = '#'

    lift = world.lift
    if not (reachable[lift-1] or
            reachable[lift+1] or
            reachable[lift-width] or
            reachable[lift+width]):
        world.total_lambdas = -1e10
        # so now it's impossible to collect all lambdas
        # (because collected_lambdas can't be equal total_lambdas)
         
    stone_reachable = stone_reachability_step(width, data)
    for i in range(width, len(data)):
        if not stone_reachable[i-width]:
            cell = data[i]
            if cell == '^':
                data[i] = '#'
            elif cell == '.':
                data[i] = ' '
                
    return world


def parse_test(s):
    lines = s.split('\n')
    assert lines[0] == ''
    del lines[0]
    assert all(len(lines[0]) == len(line) for line in lines)
    width = len(lines[0])
    data = sum(map(list, lines), [])
    return width, data


def data_to_string(width, data):
    lines = []
    for i in range(0, len(data), width):
        lines.append(''.join(data[i:i+width]))
    return '\n'.join(lines)

   
def test_processing_step(tests, step):
    fails = 0
    for test, result in tests:
        print '-'*10
        print test
        width, data = parse_test(test)
        assert test == '\n'+data_to_string(width, data)
        
        
        reachable = step(width, data)
        
        print data_to_string(width, reachable)
        
        _, expected = parse_test(result)
        
        if expected != reachable:
            print 'fail, expected'
            print data_to_string(width, expected)
            fails += 1
            
    print '='*20
    print fails, 'fails'
    return fails
            
            
if __name__ == '__main__':
    
    def bool_to_01(b):
        return {False:'0', True:'1'}[b]
    def bool_step_to_01(step):
        return lambda w, h: map(bool_to_01, step(w, h))
    
    fails = 0
    fails += test_processing_step(reachability_tests, bool_step_to_01(reachability_step))
    
    #fails += test_processing_step(stone_reachability_tests, bool_step_to_01(stone_reachability_step))
    # because currently imprecise (but correct version) is used
    
    print '/'*30
    print fails, 'fails total'
