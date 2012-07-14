import random
import backtrack
import world

class strategy:
    def __init__(self, name):
        self.name = name
    
    def solve(self, src):
        actions = [ 'L', 'R', 'U', 'D', 'W' ]
        solution = ''        
        for _ in range(random.randint(1, len(src))):
            solution += random.choice(actions)
        return solution
        
    def name(self):
        return self.name
    
    pass

class vlad_solver:
    def __init__(self):
        self.name = 'Vlad'
    
    def solve(self, src):
        world_obj = world.World.from_string(src)
        _, solution = backtrack.solve(world_obj)
        return solution
        
    def name(self):
        return self.name
    
    pass

def enumerate_all():
    return [ strategy('fuzzy'), vlad_solver() ]