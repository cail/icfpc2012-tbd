import sys
sys.path.append('../production') # for pypy

from time import clock

from dual_world import DualWorld
from world import World
from dict_world import DictWorld
from localvalidator import validate

from preprocessor import preprocess_world

class C(object):
    pass


def dist((x1, y1), (x2, y2)):
    return abs(x1-x2)+abs(y1-y2)


def aggressive_preprocess(world):
    '''
    inplace, because why not?
    '''
    #return

    data = world.data
    rxy = world.robot_coords
    num_lambdas = 0
    for i in range(len(data)):
        xy = world.index_to_coords(i)
        if dist(rxy, xy) > 7:
            if data[i] == '\\':
                num_lambdas += 1
            data[i] = '!'
    data.extend(['\\']*num_lambdas)
    

def upper_bound(state):
    '''
    Upper bound on total score
    '''
    
    collectable_lambdas = state.collected_lambdas+sum(1 for _ in state.enumerate_lambdas())

    # TODO: take trampolines into account

    if collectable_lambdas == state.total_lambdas:
            
        if state.collected_lambdas == state.total_lambdas:
            max_dist = dist(state.robot_coords, state.lift_coords)
        else:
            max_dist = 0
            for xy in state.enumerate_lambdas():
                max_dist = max(max_dist, 
                               dist(state.robot_coords, xy)+dist(xy, state.lift_coords))
        return 75*state.total_lambdas-state.time-max_dist
    
    else:
        max_dist = 0
        for xy in state.enumerate_lambdas():
            max_dist = max(max_dist, 
                           dist(state.robot_coords, xy))
                    
        return 50*collectable_lambdas-state.time-max_dist


TIME_LIMIT = 15


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
        if clock() - start > TIME_LIMIT:
            return
        
        s = state.get_score_abort()
        
        if depth <= 0:
            check(s)
            return

        preprocessed = preprocess_world(state)
        
        ub = upper_bound(preprocessed)
        if upper_bound(preprocessed) <= best.score:
            return
        
        aggressive_preprocess(preprocessed)

        frozen_state = hash(preprocessed.freeze())
        old_score = visited.get(frozen_state)
        if old_score is not None and s <= old_score:
            return
        
        visited[frozen_state] = s
        
        check(s)
        
        for cmd in 'LRUDW':
            commands.append(cmd)
            new_state, e = state.apply_command(cmd)
            if e is None:
                rec(new_state, depth-1)
            else:
                check(e)
            commands.pop()
        
    num_states = 0
        
    for depth in range(1, 100, 3):
        if clock() - start > TIME_LIMIT:
            break
        print 'depth', depth
        visited.clear() # because values for smaller depths are invalid
        rec(state, depth)
        print len(visited), 'states visited'
        num_states += len(visited)
        if clock() - start > 1:
            print '({} states per second)'.format(num_states/(clock()-start+0.01))            
        
    print '{} states visited total, ({} states per second)'.format(num_states, num_states/(clock()-start+0.01))
    
    return best.score, best.solution
        

if __name__ == '__main__':
    map_name = 'contest9'
    map = World.from_file('../data/sample_maps/{}.map'.format(map_name))
    #map.data = filter_walls(map.data) # minimize structures for cloning etc.
    #print len(map.data), 'nonwall cells'
    
    map.show()
    
    start = clock()

    score, solution = solve(map)
    
    print 'it took', clock()-start

    print '****'
    print score, solution
    
    print 'validating...',
    validated_score, _ = validate(DualWorld, map_name, solution)
    assert score == validated_score, (score, validated_score)
    print 'ok'
    
