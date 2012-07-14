import warnings
from itertools import imap

from world_base import WorldBase


def find_single_item(data, value):
    idx = data.index(value)
    assert all(c != value for c in data[idx + 1:])
    return idx
    
class World(WorldBase):
    '''
    >>> world = World.from_file('../data/sample_maps/contest1.map')
    >>> world.get_score_abort() # abort is part of public interface too!
    0
    >>> for c in 'LDRDDULULLDDL':
    ...     world, final_score = world.apply_command(c)
    ...     if final_score is not None: break
    >>> final_score
    212
    '''
    __slots__ = [
        'width',    # including the extra borders 
        'total_lambdas',
        'lift',     # index in the 1d array
        # stuff above could be shared.
        'data',     # 1d array
        'robot',    # index in the 1d array
        'collected_lambdas',
        'time',
    ]
    
    def __init__(self, other = None):
        if other is not None:
            self.width = other.width
            self.total_lambdas = other.total_lambdas
            self.lift = other.lift
            self.data = other.data[:]
            self.robot = other.robot
            self.collected_lambdas = other.collected_lambdas
            self.time = other.time

    @classmethod
    def from_string(World, src):
        assert all(c in 'R#.*\\LO \n' for c in src)
        lines = src.split('\n')
        if lines[-1] == '': del lines[-1]
        
        width = max(imap(len, lines))
        #assert all(len(l) == width for l in lines)
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
            
    def get_score_lose(self):
        return self.collected_lambdas * 25 - self.time
    
    def get_score_win(self):
        return self.collected_lambdas * 75 - self.time

    def apply_command(self, command):
        new_world = World(self)
        new_world.time += 1
        
        data = self.data
        new_data = new_world.data
        robot = self.robot
        
        if command == 'A':
            return new_world, new_world.get_score_abort() 
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
                return new_world, new_world.get_score_win()
            elif new_cell == '*' and data[new_robot + direction] == ' ':
                new_data[new_robot + direction] = '*'                
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
            else:
                warnings.warn('Action failed!')
                new_robot = robot
        if new_robot != robot:
            # another copy :( at least it's temporary
            data = new_data
            new_world.data = new_data = new_data[:]
            new_world.robot = new_robot
        
        width = self.width
        for i in xrange(1, len(data) / width - 1):
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
                            return new_world, new_world.get_score_lose()
                        continue
                    if cell_below == '*':
                        if data[offset + 1] == ' ' and data[offset_below + 1] == ' ':
                            new_data[offset] = ' '
                            new_data[offset_below + 1] = '*'
                            if offset_below + width + 1 == new_robot:
                                return new_world, new_world.get_score_lose()
                            continue
                        if data[offset - 1] == ' ' and data[offset_below - 1] == ' ':
                            new_data[offset] = ' '
                            new_data[offset_below - 1] = '*'
                            if offset_below + width - 1 == new_robot:
                                return new_world, new_world.get_score_lose()
                            continue
                    if cell_below == '\\':
                        if data[offset + 1] == ' ' and data[offset_below + 1] == ' ':
                            new_data[offset] = ' '
                            new_data[offset_below + 1] = '*'
                            if offset_below + width + 1 == new_robot:
                                return new_world, new_world.get_score_lose()
                            continue
                        
        return new_world, None
     
    def freeze(self):
        '''
        For hashing
        '''
        return (tuple(self.data), self.time)
   
    def index_to_coords(self, index):
        return index%self.width-1, index//self.width-1
    
    @property
    def robot_coords(self):
        return self.index_to_coords(self.robot)

    @property
    def lift_coords(self):
        return self.index_to_coords(self.robot)
    
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
    world = World.from_file('../data/sample_maps/contest1.map')
    world.show()
#    for c in 'LDRDDULULLDDL':
#        print c
#        world, final_score = world.apply_command(c)
#        world.show()
#        print final_score
    import doctest
    doctest.testmod()
