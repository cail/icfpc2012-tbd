#import sys
#sys.path.append('../production') # for pypy

from time import clock

from game import Map, validate
from areas import filter_walls

class C(object):
    pass


def dist((x1, y1), (x2, y2)):
    return abs(x1-x2)+abs(y1-y2)


def upper_bound(state):
    '''
    Upper bound on total score
    '''
    max_dist = 0
    
    if state.data[state.lift] == 'O':
        max_dist = dist(state.robot, state.lift)
    else:
        for xy in state.enumerate_lambdas():
            max_dist = max(max_dist, 
                           dist(state.robot, xy)+dist(xy, state.lift))
            
    return 75*state.initial_lambdas-state.time()-max_dist


def solve(state):
    start = clock()
    
    best = C()
    
    best.score = 0
    best.solution = ''
    
    commands = []
    
    def check(score):
        if  score > best.score:
            best.score = score
            best.solution = ''.join(commands)
            print 'better solution found: ', best.score, best.solution
            
    visited = {}
    
    def rec(state, depth):
        s = state.intermediate_score()
        
        if depth <= 0:
            check(s)
            return

        if upper_bound(state) <= best.score:
            return

        frozen_state = state.freeze()
        old_score = visited.get(frozen_state)
        if old_score is not None and s <= old_score:
            return
        
        visited[frozen_state] = s
        
        check(s)
        
        for cmd in 'LRUDW':
            commands.append(cmd)
            new_state, e = state.execute_command(cmd)
            if e is None:
                rec(new_state, depth-1)
            else:
                check(e)
            commands.pop()
        
    num_states = 0
        
    for depth in range(1, 30):
        print 'depth', depth
        visited.clear() # because values for smaller depths are invalid
        rec(state, depth)
        print len(visited), 'states visited'
        num_states += len(visited)
        
    print '{} states visited total, ({} states per second)'.format(num_states, num_states/(clock()-start+0.01))
    
    return best.score, best.solution
        

if __name__ == '__main__':
    map_name = 'contest2'
    map = Map.load_file('../data/sample_maps/{}.map'.format(map_name))
    map.data = filter_walls(map.data) # minimize structures for cloning etc.
    print len(map.data), 'nonwall cells'
    
    map.show()
    
    start = clock()

    score, solution = solve(map)
    
    print 'it took', clock()-start

    print '****'
    print score, solution
    
    print 'validating...',
    validated_score, _ = validate(map_name, solution)
    assert score == validated_score, (score, validated_score)
    print 'ok'
    
