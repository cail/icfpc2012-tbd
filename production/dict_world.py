from copy import deepcopy

from world_base import WorldBase


class DictWorld(WorldBase):
    '''
    >>> world = DictWorld.from_file('../data/sample_maps/contest1.map')
    >>> world.get_score_abort()
    0
    >>> for c in 'LDRDDULULLDDL':
    ...     world, final_score = world.apply_command(c)
    ...     if final_score is not None: break
    >>> final_score
    212
    '''
    
    __slots__ = [
        'width',
        'height',
        'data',
        'total_lambdas',
        'commands',# list of commands executed so far
        'robot_coords',   # (x, y); zero based, because!
        'lift_coords',    # (x, y)
        'aborted', # whether robot executed Abort
        'lifted',  # whether robot has entered lambda lift_coords 
        'dead',    # whether robot was killed by rock
        'water',
        'flooding',
        'waterproof',
        'time_underwater', # time spend time_underwater
    ]
    
    #### World interface, kind of

    def __init__(self):
        self.data = {}
        self.height = 0
        self.width = 0
        self.commands = []
        self.robot_coords = None
        self.lift_coords = None
        self.total_lambdas = 0
        self.aborted = False
        self.lifted = False
        self.dead = False
        
        self.water = 0
        self.flooding = 0
        self.waterproof = 10
        
        self.time_underwater = 0
        

    @staticmethod
    def from_string(src):
        lines = src.split('\n')
        if lines[-1] == '': 
            del lines[-1]
                
        w = DictWorld()
        #assert all(len(line) == len(lines[0]) for line in lines)
        
        if '' in lines:
            params = lines[lines.index('')+1:]
            lines = lines[:lines.index('')]
            for param in params:
                name, value = param.split()
                if name == 'Water':
                    w.water = int(value)
                elif name == 'Flooding':
                    w.flooding = int(value)
                elif name == 'Waterproof':
                    w.waterproof = int(value)
                else:
                    assert False, param
                    
        w.height = len(lines)
        w.width = max(len(line) for line in lines)
            
        for i, line in enumerate(lines):
            i = w.height-1-i
            for j, c in enumerate(line):
                assert c in 'R#*\\.LO ', c
                w.data[j, i] = c
                if c == 'R':
                    assert w.robot_coords is None
                    w.robot_coords = j, i
                elif c == '\\':
                    w.total_lambdas += 1
                elif c in 'LO':
                    assert w.lift_coords == None
                    w.lift_coords = j, i
            for j in range(len(line), w.width):
                w.data[j, i] = ' '
                
        return w
    
    def get_map_string(self):
        lines = []
        for i in range(self.height):
            lines.append(''.join(self.data.get((j, self.height-1-i), '#') 
                                 for j in range(self.width)))
        return '\n'.join(lines)
    
    def show(self):
        print self.get_map_string()
        print 'robot_coords at {}; current score is {}'.format(self.robot_coords, self.score)
        
    @property        
    def terminated(self):
        return self.lifted or self.dead or self.aborted
    
    @property
    def score(self):
        # TODO: clarify in what order winning and drowning are tested
        if self.lifted:
            return self.get_score_win()
        if self.dead:
            return self.get_score_lose()
        # aborted or running
        return self.get_score_abort()
        
    
    @property
    def time(self):
        return len(self.commands)
    
    @property
    def water_level(self):
        if self.flooding == 0:
            return 0
        return self.water + (self.time - 1)//self.flooding
        # time-1 because we check it in update
        
    def apply_command(self, c):
        '''
        return updated world
        '''
        assert not self.terminated
        
        other = deepcopy(self)
        other.execute_command_inplace(c)
        if other.terminated:
            return other
        other.update()
        return other
    
    
    #### Implementation stuff
        
    def execute_command_inplace(self, c):
        if c == 'L':
            self.move(-1, 0)
        elif c == 'R':
            self.move(1, 0)
        elif c == 'U':
            self.move(0, 1)
        elif c == 'D':
            self.move(0, -1)
        elif c == 'W':
            pass
        elif c == 'A':
            self.aborted = True
            # return immediately because A is not really a command.
            return
        else:
            raise 'unknown command'
        self.commands.append(c)
        
    def move(self, dx, dy):
        ''' move robot_coords only 
        
        Without map update step. 
        Return whether move was sucessfull.
        '''
        
        assert dx*dx+dy*dy == 1
        
        x, y = self.robot_coords
        new_cell = self.data.get((x+dx, y+dy), '#')
        if new_cell in ' .\\O':
            if new_cell == 'O':
                self.lifted = True
            self.data[self.robot_coords] = ' '
            self.robot_coords = x+dx, y+dy
            if new_cell != 'O':
                self.data[self.robot_coords] = 'R'
            return True
        
        if dy == 0 and new_cell == '*':
            behind = (x+2*dx, y+2*dy)
            if self.data.get(behind) == ' ':
                self.data[self.robot_coords] = ' '
                self.robot_coords = x+dx, y+dy
                self.data[self.robot_coords] = 'R'
                self.data[behind] = '*'
                return True

        return False
        
    def update(self):
        _, y = self.robot_coords
        if y < self.water_level:
            self.time_underwater += 1
            if self.time_underwater > self.waterproof:
                self.dead = True
                # still run the rest of the update
        else:
            self.time_underwater = 0
        
        data = self.data
        u = {}
        
        def fall(x, y):
            if self.robot_coords == (x, y-1):
                self.dead = True
        
        has_lambdas = '\\' in data.values() 
        # because lambdas can not disappear during updates 
        
        for (x, y), c in data.items():
            # because it's actually irrelevant in what order we update
            if c == '*':
                under = data.get((x, y-1))
                if under == ' ':
                    u[x, y] = ' '
                    u[x, y-1] = '*'
                    fall(x, y-1)
                    continue
                if under == '*':
                    if data.get((x+1, y)) == ' ' and data.get((x+1, y-1)) == ' ':
                        u[x, y] = ' '
                        u[x+1, y-1] = '*'
                        fall(x+1, y-1)
                        continue
                    if data.get((x-1, y)) == ' ' and data.get((x-1, y-1)) == ' ':
                        u[x, y] = ' '
                        u[x-1, y-1] = '*'
                        fall(x-1, y-1)
                        continue
                if under == '\\':
                    if data.get((x+1, y)) == ' ' and data.get((x+1, y-1)) == ' ':
                        u[x, y] = ' '
                        u[x+1, y-1] = '*'
                        fall(x+1, y-1)
                        continue
            if c == 'L' and not has_lambdas:
                u[x, y] = 'O'
                    
        #data.update(**u)
        for k, v in u.items():
            data[k] = v
        # to please pypy
        
    def enumerate_lambdas(self):
        for k, v in self.data.items():
            if v == '\\':
                yield k
                
    def count_lambdas(self):
        return sum(1 for _ in self.enumerate_lambdas())
    
    @property
    def collected_lambdas(self):
        return self.total_lambdas-self.count_lambdas()
                
    def __getitem__(self, coords):
        return self.data.get(coords, '#')
    
                

if __name__ == '__main__':
    import doctest
    doctest.testmod()
