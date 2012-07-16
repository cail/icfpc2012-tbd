import warnings
from itertools import imap

from world_base import WorldBase
import pprint


def find_single_item(data, value):
    idx = data.index(value)
    assert all(c != value for c in data[idx + 1:])
    return idx
    
class World(WorldBase):
    '''
    >>> world = World.from_file('../data/sample_maps/contest1.map')
    >>> world.score # automatically decides which score to return
    0
    >>> for c in 'LDRDDULULLDDL':
    ...     world = world.apply_command(c)
    ...     if world.terminated: break
    >>> world.score
    212
    '''
    __slots__ = [
        'width',    # including the extra borders 
        'total_lambdas',
        'lift',     # index in the 1d array
        'water',
        'flooding',
        'waterproof',
        # stuff above could be shared between instances.
        'data',     # 1d array
        'robot',    # index in the 1d array
        'collected_lambdas',
        'time',
        'final_score', # non-None when the world is terminated
        'time_underwater',
    ]
    

    #### World interface, kind of
    
    def __init__(self, other = None):
        if other is not None:
            self.width = other.width
            self.total_lambdas = other.total_lambdas
            self.lift = other.lift
            self.water = other.water
            self.flooding = other.flooding
            self.waterproof = other.waterproof
        
            self.data = other.data[:]
            self.robot = other.robot
            self.collected_lambdas = other.collected_lambdas
            self.time = other.time
            self.final_score = other.final_score
            self.time_underwater = other.time_underwater

    @classmethod
    def from_string(World, src):
        src, _, metadata = src.partition('\n\n')
        try:
            assert all(c in 'R#.*\\LO \n' for c in src)
        except AssertionError:
            print src
            raise
        lines = src.split('\n')
        while lines[-1] == '': del lines[-1]

        width = max(imap(len, lines))
        width += 2
        
        # use plain list of interned strings (which would remain interned)
        # it might be even faster than using array.array('b') because of less
        # temporaries and faster string comparison (it does have a fast path).
        data = []
        data.extend('#' for _ in xrange(width))
        for line in lines:
            data.append('#')
            data.extend(imap(intern, line))
            data.extend([' ']*(width-2-len(line)))
            data.append('#')
        data.extend('#' for _ in xrange(width))
        
        world = World()
        world.width = width
        world.lift = find_single_item(data, 'L')
        world.total_lambdas = data.count('\\')
        
        world.data = data
        world.robot = find_single_item(data, 'R')
        world.collected_lambdas = 0
        world.time = 0
        world.final_score = None
        
        metadict = dict(line.split(' ', 1) for line in metadata.split('\n') if line)
        world.water = int(metadict.get('Water', 0))
        world.flooding = int(metadict.get('Flooding', 0))
        world.waterproof = int(metadict.get('Waterproof', 10))
        world.time_underwater = 0
        
        return world
    
    def get_map_string(self):
        lines = []
        height = len(self.data) / self.width
        for i in xrange(1, height - 1):
            offset = i * self.width
            lines.append(''.join(self.data[offset + 1 : offset + self.width - 1]))
        return '\n'.join(lines)
    
    def show(self):
        print self.get_map_string()
        
    # time is an actual field in this implementation.

    @property        
    def terminated(self):
        return self.final_score is not None
    
    @property
    def score(self):
        if self.final_score is not None:
            return self.final_score
        return self.get_score_abort() 

    @property    
    def water_level(self):
        if self.flooding == 0:
            return 0
        return self.water + (self.time - 1) // self.flooding 

    def apply_command(self, command):
        assert not self.terminated
        
        new_world = World(self)
        
        # abort is not a command really
        if command == 'A':
            new_world.final_score = new_world.get_score_abort() 
            return new_world
        
        new_world.time += 1
        
        data = self.data
        new_data = new_world.data
        robot = self.robot
        width = self.width
        
        if command == 'W':
            new_robot = robot
        else:
            direction = [-self.width, self.width, -1, 1]['UDLR'.index(command)]
            new_robot = robot + direction
            new_cell = data[new_robot] 
            if new_cell in ' .':
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
            elif new_cell == '\\':
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
                new_world.collected_lambdas += 1
                if new_world.collected_lambdas == new_world.total_lambdas:
                    new_data[self.lift] = 'O'
            elif new_cell == 'O':
                new_data[robot] = ' '
                new_world.final_score = new_world.get_score_win() 
                return new_world 
            elif new_cell == '*' and command in 'LR' and data[new_robot + direction] == ' ':
                new_data[new_robot + direction] = '*'                
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
            else:
#                warnings.warn('Action failed!')
                new_robot = robot
        if new_robot != robot:
            # another copy :( at least it's temporary
            data = new_data
            new_world.data = new_data = new_data[:]
            new_world.robot = new_robot
            
        for i in xrange(len(data) / width - 2, 0, -1):
            offset = i * width
            for offset in xrange(offset + 1, offset + width - 1):
                cell = data[offset]
                if cell == '*':
                    offset_below = offset + width 
                    cell_below = data[offset_below]
                    if cell_below == ' ':
                        new_data[offset] = ' '
                        new_data[offset_below] = '*'
                        if offset_below + width == new_robot:
                            new_world.final_score = new_world.get_score_lose()
                    elif cell_below == '*' or cell_below == '^': # '^' is frozen stone (that is, 'slippery wall')
                        if data[offset + 1] == ' ' and data[offset_below + 1] == ' ':
                            new_data[offset] = ' '
                            new_data[offset_below + 1] = '*'
                            if offset_below + width + 1 == new_robot:
                                new_world.final_score = new_world.get_score_lose() 
                        elif data[offset - 1] == ' ' and data[offset_below - 1] == ' ':
                            new_data[offset] = ' '
                            new_data[offset_below - 1] = '*'
                            if offset_below + width - 1 == new_robot:
                                new_world.final_score = new_world.get_score_lose() 
                    elif cell_below == '\\':
                        if data[offset + 1] == ' ' and data[offset_below + 1] == ' ':
                            new_data[offset] = ' '
                            new_data[offset_below + 1] = '*'
                            if offset_below + width + 1 == new_robot:
                                new_world.final_score = new_world.get_score_lose()
                                
        if new_robot >= len(data) - width * (new_world.water_level + 1):
            new_world.time_underwater += 1
            if new_world.time_underwater > new_world.waterproof:
                new_world.final_score = new_world.get_score_lose() 
        else:
            new_world.time_underwater = 0

        return new_world
     
    # not __hash__ because semantics is slightly different
    def get_hash(self):
        s = ''.join(self.data) + repr((self.total_lambdas, self.collected_lambdas)) # but not time!
        # TODO: clarify what exactly should be hashed
        # TODO: 64-bit hash
        return hash(s)
   
    
    #### Implementation stuff
    
    def index_to_coords(self, index):
        return index % self.width-1, (len(self.data)-index-1)//self.width-1
    
    def coords_to_index(self, (x,reverse_y)):
        return ( (( len(self.data) / self.width ) - reverse_y) * self.width ) + x
    
    def __getitem__(self, (x, y)):
        if x < 0 or x >= self.width-2:
            return '#'
        #i = x+1+(y+1)*self.width
        i = len(self.data)-(y+2)*self.width+x+1
        if i < 0 or i >= len(self.data):
            return '#'
        return self.data[i]
    
    @property
    def robot_coords(self):
        return self.index_to_coords(self.robot)

    @property
    def lift_coords(self):
        return self.index_to_coords(self.lift)
    
    def enumerate_lambdas_index(self):
        return [i for i,x in enumerate(self.data) if x == '\\']
    
    def enumerate_something_index(self, something):
        return [i for i,x in enumerate(self.data) if x == something]
    
    def enumerate_lambdas(self):
        start = 0
        try:
            while True:
                i = self.data.index('\\', start)
                yield self.index_to_coords(i)
                start = i+1
        except ValueError:
            pass
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod(report=True)
