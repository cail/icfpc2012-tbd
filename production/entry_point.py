
import sys
import signal

from world import World
from search import Solver 
import mask_errors
import genetic
import utils

mask_errors.MASK_ERRORS = True


def handler(signum, stack):
    if signum != signal.SIGINT:
        return
    print>>realout, solver.get_best()[1]
    print 'final score', solver.get_best()[0]
    exit()



@mask_errors.failsafe(default=None)
def greedy(world):
    initial_world = World(world)
    global solver
    cmds = ''
    while not world.terminated:
        if len(cmds) > 10000:
            break
        #print cmds
        t = utils.path_to_nearest_lambda_or_lift(world)
        if t is None:
            break
        _, c = t
        #print c
        world = world.apply_commands(c)
        cmds += c
        if world.score > solver.best_score:
            solver.best_score = world.score
            solver.best_solution = cmds
            
    print 'greedy', solver.best_score, len(solver.best_solution)
    
    if initial_world.apply_commands(cmds).score < 0:
        solver.best_score = 0
        solver.best_solution = ''
        print 'shit!'


@mask_errors.failsafe(default=None)
def call_genetic(world):
    global solver
    print 'genetic'
    solution = genetic.solve(World(world), 5)
    score = World(world).apply_commands(solution).score
    print 'genetic done', score
    if score > 0:
        solver.best_score = score
        solver.best_solution = solution
        


if __name__ == '__main__':
    realout = sys.stdout
    sys.stdout = sys.stderr

    signal.signal(signal.SIGINT, handler)
    
    data = sys.stdin.read()
    world = World.from_string(data)
    
    world.show()
    
    solver = Solver(world, timeout=1000000)
    
    greedy(World(world))
    
    call_genetic(World(world))
    
    solver.solve()
    
    print>>realout, solver.get_best()[1]
    print 'final score', solver.get_best()[0]
    
    sys.stdout = realout
    