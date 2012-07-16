import sys
import signal

from world import World
from search import Solver 
import mask_errors

mask_errors.MASK_ERRORS = True


def handler(signum, stack):
    if signum != signal.SIGINT:
        return
    print>>realout, solver.get_best()[1]
    exit()


if __name__ == '__main__':
    realout = sys.stdout
    sys.stdout = sys.stderr

    signal.signal(signal.SIGINT, handler)
    
    data = sys.stdin.read()
    world = World.from_string(data)
    
    world.show()
    
    solver = Solver(world, timeout=1000000)
    solver.solve()
    
    print>>realout, solver.get_best()[1]
    
    sys.stdout = realout
    