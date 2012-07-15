import random
import re

import backtrack
import genetic
import world

time_limit = 50

class fuzz_solver:
    def __init__(self):
        self.name = 'fuzzy'
    
    def solve(self, src, filename):
        actions = [ 'L', 'R', 'U', 'D', 'W' ]
        solution = ''        
        for _ in range(random.randint(1, len(src))):
            solution += random.choice(actions)
        return solution
    
    pass

class vlad_solver:
    def __init__(self):
        self.name = 'Vlad'
    
    def solve(self, src, filename):
        world_obj = world.World.from_string(src)
        _, solution = backtrack.solve(world_obj, time_limit)
        return solution
        
    pass

class drw_solver:
    def __init__(self):
        self.name = 'DRW'
    
    def solve(self, src,  filename):
        world_obj = world.World.from_string(src)
        solver = genetic.GeneticSolver(world_obj)
        solution = solver.solve(time_limit)
        return solution

    pass

class predefined_solver:
    def __init__(self):
        self.name = 'manual'
        self.solution_srcs = open('../../data/maps_manual/scores', "r").read()
        lines = self.solution_srcs.split('\n')
        self.solutions = { }
        current_map = 'null'
        for line in lines:
            if line == '':
                current_map = 'null'            
            elif line.startswith('Path: '):
                self.solutions[current_map] = re.search("Path: (.*)", line).group(1)
            elif not line.startswith('Score'):                
                current_map = line
    
    def solve(self, src, filename):
        if filename in self.solutions.iterkeys():
            return self.solutions[filename]
        else:
            return None

    pass
