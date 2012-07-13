from copy import deepcopy


class Map(object):
    '''
    >>> map = Map.load_file('../data/sample_maps/contest1.map')
    >>> for c in 'LDRDDULULLDDL':
    ...     assert map.ending() is None
    ...     map.execute_command_inplace(c)
    ...     map.update()
    >>> map.ending()
    212
    
    
    Alternatively, in functional style:
    >>> map = Map.load_file('../data/sample_maps/contest1.map')
    >>> for c in 'LDRDDULULLDDL':
    ...     map, e = map.execute_command(c)
    >>> e
    212
    '''
    
    __slots__ = [
        'width',
        'height',
        'data',
        'initial_lambdas',
        'commands',# list of commands executed so far
        'robot',   # (x, y); zero based, because!
        'aborted', # whether robot executed Abort
        'lifted',  # whether robot has entered lambda lift 
        'dead',    # whether robot was killed by rock
        'water',
        'flooding',
        'waterproof',
        'underwater', # time spend underwater
    ]

    def __init__(self):
        self.data = {}
        self.height = 0
        self.width = 0
        self.commands = []
        self.robot = None
        self.initial_lambdas = 0
        self.aborted = False
        self.lifted = False
        self.dead = False
        
        self.water = 0
        self.flooding = 0
        self.waterproof = 10
        
        self.underwater = 0
        

    @staticmethod
    def load(lines):
        map = Map()
        #assert all(len(line) == len(lines[0]) for line in lines)
        
        if '' in lines:
            params = lines[lines.index('')+1:]
            lines = lines[:lines.index('')]
            for param in params:
                name, value = param.split()
                if name == 'Water':
                    map.water = int(value)
                elif name == 'Flooding':
                    map.flooding = int(value)
                elif name == 'Waterproof':
                    map.waterproof = int(value)
                else:
                    assert False, param
                    
        map.height = len(lines)
        map.width = max(len(line) for line in lines)
            
        for i, line in enumerate(lines):
            i = map.height-1-i
            for j, c in enumerate(line):
                assert c in 'R#*\\.LO ', c
                map.data[j, i] = c
                if c == 'R':
                    assert map.robot is None
                    map.robot = j, i
                elif c == '\\':
                    map.initial_lambdas += 1
            for j in range(len(line), map.width):
                map.data[j, i] = ' '
                
        return map
    
    def time(self):
        return len(self.commands)
    
    def water_level(self):
        if self.flooding == 0:
            return 0
        return self.water+(self.time()-1)//self.flooding-1
        # time-1 because we check it in update
        # -1 because our coords are zero-based
    
    @staticmethod
    def load_string(string):
        lines = string.split('\n')
        return Map.load(lines)
        pass

    @staticmethod
    def load_file(file_name):
        with open(file_name) as fin:
            lines = [line.rstrip('\n') for line in fin]
        return Map.load(lines)
    
    def get_map_string(self):
        lines = []
        for i in range(self.height):
            lines.append(''.join(self.data.get((j, self.height-1-i), '#') 
                                 for j in range(self.width)))
        return '\n'.join(lines)
    
    def show(self):
        print self.get_map_string()
        print 'robot at {}; current score is {}'.format(self.robot, self.intermediate_score())
        
    def execute_command_inplace(self, c):
        assert c != 'A', 'according to webvalidator behavior, abort is not command'
        
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
        else:
            raise 'unknown command'
        self.commands.append(c)
    
    def execute_command(self, c):
        '''
        return pair (new map, final score or None)
        '''
        other = deepcopy(self)
        other.execute_command_inplace(c)
        other.update()
        return other, other.ending()
    
    def freeze(self):
        '''return immutable (hashable) state'''
        data = frozenset(self.data.items())
        return (data, self.time(), self.aborted, self.lifted, self.dead)
        
    def move(self, dx, dy):
        ''' move robot only 
        
        Without map update step. 
        Return whether move was sucessfull.
        '''
        
        assert dx*dx+dy*dy == 1
        
        x, y = self.robot
        new_cell = self.data.get((x+dx, y+dy), '#')
        if new_cell in ' .\\O':
            if new_cell == 'O':
                self.lifted = True
            self.data[self.robot] = ' '
            self.robot = x+dx, y+dy
            if new_cell != 'O':
                self.data[self.robot] = 'R'
            return True
        
        if dy == 0 and new_cell == '*':
            behind = (x+2*dx, y+2*dy)
            if self.data.get(behind) == ' ':
                self.data[self.robot] = ' '
                self.robot = x+dx, y+dy
                self.data[self.robot] = 'R'
                self.data[behind] = '*'
                return True

        return False
        
    def update(self):
        
        _, y = self.robot
        if y <= self.water_level():
            self.underwater += 1
        
        data = self.data
        u = {}
        
        def fall(x, y):
            if self.robot == (x, y-1):
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
                    
        data.update(**u)
        
    def count_lambdas(self):
        return sum(1 for c in self.data.values() if c == '\\')
    
    def collected_lambdas(self):
        return self.initial_lambdas-self.count_lambdas()
        
    def intermediate_score(self):
        '''score assuming we abort in time'''
        return 50*self.collected_lambdas()-self.time()
        
    def ending(self):
        '''return either None or additional score'''
        
        # TODO: clarify in what order winning and drowning are tested
        
        if self.underwater > self.waterproof:
            return 25*self.collected_lambdas()-self.time()
        if self.lifted:
            return 75*self.collected_lambdas()-self.time()
        if self.aborted:
            return 50*self.collected_lambdas()-self.time()
        if self.dead:
            return 25*self.collected_lambdas()-self.time()
    
                
def play(map):
    map.show()
    while True:
        print '>>>',
        commands = raw_input()
        for c in commands:
            if c == 'A':
                e = map.intermediate_score()
                break
            map.execute_command_inplace(c)
            map.update()
            map.show()
            e = map.ending()
            if e is not None:
                break
    map.show()
    print 'Final score:', e
            
            

def validate(map_name, route):
    '''Validate with my emulator
    
    Follows webvalidator interface.
    Return tuple (score, world).
    '''
    map = Map.load_file('../data/sample_maps/{}.map'.format(map_name))
    
    e = None
    for c in route:
        if c == 'A':
            break
        map.execute_command_inplace(c)
        map.update()
        e = map.ending()
        if e is not None:
            break
    
    if e is not None:
        score = e
    else:
        score = map.intermediate_score()
        assert score is not None
        
    return (score, map.get_map_string())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    my = validate('contest1', 'RRR')
