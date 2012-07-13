class strategy:
    def __init__(self, name):
        self.name = name
    
    def solve(self, world):
        return 'R';
    
    def name(self):
        return self.name
    
    pass

def enumerate_all():
    return [ strategy('name1'), strategy('name2') ]