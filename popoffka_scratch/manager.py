import sys, signal
sys.path.append('../production')
from world import World
import random

# you'll most likely want to redefine Solver
class Solver:
    def __init__(self, data):
        '''Accepts a string describing the map as the only argument.
        '''
        self.data = data
        self.solution = ('A', 0)
        self.stopped = False

    def start(self):
        '''Starts trying to solve the task, slowly making the solution better.
        It's ok if start() finishes by itself (e.g. if it thinks it found the best possible solution).
        Should periodically (at least once in 10 seconds) check if self.stopped is True, and if it is, stop executing.
        '''
        self.stopped = False
        while True:
            m = World.from_string(self.data)
            program = ''
            while True:
                if random.randint(1, 100) <= 33:
                    ch = 'A'
                else:
                    ch = random.choice('ULDR')
                program += ch
                m, final_score = m.apply_command(ch)
                if final_score is not None:
                    break
            if final_score > self.solution[1]:
                self.solution = (program, final_score)

            if self.stopped:
                break

    def stop(self):
        '''Sets self.stopped to True in order to stop a working start().
        '''
        self.stopped = True

    def get_solution(self):
        '''Returns the best solution found so far.
        '''
        return self.solution[0]

# this is where all the magic hapens
class SolvingManager:
    def __init__(self, infile, solverclass):
        '''Accepts an input file (file object, not file name) and a Solver class as arguments.
        Will immediately read the whole input file. Will set a handler for SIGINT.
        '''
        self.data = infile.read()
        self.solver = solverclass(self.data)
        signal.signal(signal.SIGINT, self.sigint_handler)

    def start(self):
        '''Tells the solver to start solving the task.
        '''
        self.solver.start()

    def sigint_handler(self, signum, stack):
        '''Tells the solver to stop solving.
        '''
        if signum != signal.SIGINT:
            return

        self.solver.stop()

    def get_solution(self):
        '''Returns the best solution found so far.
        '''
        return self.solver.get_solution()

def main():
    # let's protect ourselves from accidentally sending bullshit to stdout during the solving process
    realout = sys.stdout
    sys.stdout = sys.stderr

    man = SolvingManager(sys.stdin, Solver)
    man.start()

    sys.stdout = realout
    print man.get_solution()


if __name__ == '__main__':
    main()
