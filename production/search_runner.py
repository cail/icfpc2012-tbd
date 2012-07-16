from time import clock

from search import Solver
from world import World


def run_test(map_path, timeout):
    start = clock()
    world = World.from_file(map_path)
    print 'solving {:50}'.format(map_path),
    
    start = clock()
    solver = Solver(world, timeout=timeout)
    solver.solve()
    score, solution = solver.get_best()
    solver.log_stats()
    t = clock()-start    
    
    
    world = World.from_file(map_path)
    for cmd in solution:
        world = world.apply_command(cmd)
        if world.terminated:
            break
    validated_score = world.score
    
    assert score == validated_score, (score, validated_score)
    print '{:>10} {:>10.3f}s'.format(score, t)
    
    
if __name__ == '__main__':
    from glob import glob
    #maps = glob('../data/sample_maps/beard*.map')
    maps = glob('../data/*/*.map')
    maps.sort()
    
    for map in maps:
        run_test(map, timeout=5)