import random

class strategy:
    def __init__(self, name):
        self.name = name
    
    def solve(self, world):
        actions = [ 'L', 'R', 'U', 'D', 'W' ]
        solution = ''        
        for _ in random.randint(len(world)):
            solution += random.choice(actions)
        return solution
        
    def name(self):
        return self.name
    
    pass

def enumerate_all():
    return [ strategy('name1'), strategy('name2') ]