
import sys
import signal

from world import World
from search import Solver 
import mask_errors
import genetic

mask_errors.MASK_ERRORS = True


def handler(signum, stack):
    if signum != signal.SIGINT:
        return
    print>>realout, solver.get_best()[1]
    print 'final score', solver.get_best()[0]
    exit()


@mask_errors.failsafe(default=None)
def call_genetic():
    global solver
    print 'genetic'
    solution = genetic.solve(World(world), 50)
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
    
    call_genetic()
    
    solver.solve()
    
    print>>realout, solver.get_best()[1]
    print 'final score', solver.get_best()[0]
    
    sys.stdout = realout
    