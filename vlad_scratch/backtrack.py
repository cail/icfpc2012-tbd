import sys
sys.path.append('../production') # for pypy

from time import clock
from itertools import *

from world import World

from preprocessor import preprocess_world
from utils import dist, path_to_nearest_lambda_or_lift
from upper_bound import upper_bound


class C(object):
    pass



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
    


    

def solve(state, time_limit=15):
    
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
    
    def rec(state, depth, stack_size):
        if clock() - start > time_limit:
            return
        
        s = state.get_score_abort()
        
        if depth <= 0 or stack_size <= 0:
            check(s)
            return

        preprocessed = preprocess_world(state)
        
        if upper_bound(preprocessed)-state.time <= best.score:
            return
        
        aggressive_preprocess(preprocessed)

        frozen_state = preprocessed.get_hash()
        old_score = visited.get(frozen_state)
        if old_score is not None and s <= old_score:
            return
        
        visited[frozen_state] = s
        
        check(s)
        
        zzz = 'LRUDW'
        num_commands = len(commands)
        next_steps = set()
        
        greedy = path_to_nearest_lambda_or_lift(state)
        if greedy is not None:
            greedy = [greedy]
        else:
            greedy = []
            
        #greedy = []
        
        for cmds in chain(greedy, product(zzz, zzz)):
            new_state = state
            for cmd in cmds:
                if new_state.final_score is None:
                    new_state = new_state.apply_command(cmd)
                    # TODO: check()
                commands.append(cmd)
            
            if new_state.final_score is None:
                h = new_state.get_hash()
                if h not in next_steps:
                    next_steps.add(h)
                    if cmds in greedy:
                        new_depth = depth
                    else:
                        new_depth = depth-1
                    rec(new_state, new_depth, stack_size-1)
            else:
                check(new_state.final_score)
                
            for _ in cmds:
                commands.pop()
        assert num_commands == len(commands)
        
    num_states = 0
    
    max_stack_size = min(100, 100000000//len(state.data))
    
    for depth in range(1, 50):
        if clock() - start > time_limit:
            break
        print 'depth', depth
        visited.clear() # because values for smaller depths are invalid
        assert commands == []
        rec(state, depth, max_stack_size)
        print len(visited), 'states visited'
        num_states += len(visited)
        if clock() - start > 1:
            print '({} states per second)'.format(num_states/(clock()-start+0.01))            
        
    print '{} states visited total, ({} states per second)'.format(num_states, num_states/(clock()-start+0.01))
    
    return best.score, best.solution
        

if __name__ == '__main__':
    
    from dual_world import DualWorld
    from dict_world import DictWorld
    from test_emulators import validate
    
    map_name = 'flood3'
    map_path = '../data/sample_maps/{}.map'.format(map_name)
    world = World.from_file(map_path)
    
    world.show()
    
    start = clock()

    score, solution = solve(world)
    
    print 'it took', clock()-start

    print '****'
    print score, solution
    
    print 'validating...',
    
    world = DualWorld.from_file(map_path)
    for cmd in solution:
        world = world.apply_command(cmd)
        if world.terminated:
            break
    validated_score = world.score
    
    assert score == validated_score, (score, validated_score)
    
    validate(map_name, solution, World, DictWorld, DualWorld)
    
    print 'ok'
    
