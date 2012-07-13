from game import Map, validate
from time import clock


class C(object):
    pass


def upper_bound(state):
    max_dist = 0
    rx, ry = state.robot
    for (x, y), cell in state.data.items():
        if cell in 'LO\\':
            max_dist = max(max_dist, abs(rx-x)+abs(ry-y))
            
    return 75*state.initial_lambdas-state.time()-max_dist


def solve(state):
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
        
    for depth in range(1, 20):
        print 'depth', depth
        visited.clear() # because values for smaller depths are invalid
        rec(state, depth)
        
    print len(visited), 'states visited'
    
    return best.score, best.solution    
        

if __name__ == '__main__':
    map = Map.load_file('../data/sample_maps/contest1.map')
    
    map.show()
    
    start = clock()

    score, solution = solve(map)
    
    print 'it took', clock()-start

    print 'validating...',
    validated_score, _ = validate(1, solution)
    assert score == validated_score, (score, validated_score)
    print 'ok'
    
