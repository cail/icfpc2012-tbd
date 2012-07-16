from copy import copy
from itertools import imap

from world_base import WorldBase
import pprint

application_counter = 0

TRAMPOLINE_SOURCE_LETTERS = set('ABCDEFGHI')
TRAMPOLINE_TARGET_LETTERS = set('123456789')
TRAMPOLINE_LETTERS = TRAMPOLINE_SOURCE_LETTERS | TRAMPOLINE_TARGET_LETTERS
VALID_MAP_CHARACTERS = set('R#.*\\LO !W@\n') | TRAMPOLINE_LETTERS  
 
def find_single_item(data, value):
    idx = data.index(value)
    assert all(c != value for c in data[idx + 1:])
    return idx

def enhance_trampoline_mapping(mapping, data):
    '''Convert { src : dst } to { src : (dst_idx, [src_idx]) }
    
    >>> sorted(enhance_trampoline_mapping({'A' : '2', 'B' : '2', 'C' : '1'}, '_21CBA').iteritems())
    [('A', (1, [5, 4])), ('B', (1, [5, 4])), ('C', (2, [3]))]
    '''
    trampolines = dict((c, (idx, []))
                       for idx, c in enumerate(data)
                       if c in TRAMPOLINE_LETTERS)

    for src, dst in mapping.iteritems():
        trampolines[dst][1].append(trampolines[src][0])
    
    return dict((src, (trampolines[dst][0], trampolines[dst][1]))
                for src, dst in mapping.iteritems())
                    
                
                
    
    
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
        'trampolines',
        'growth',
        'neighbours8',
        
        # stuff above could be shared between instances.
        'data',     # 1d array
        'robot',    # index in the 1d array
        'collected_lambdas',
        'time',
        'final_score', # non-None when the world is terminated
        'time_underwater',
        'razors',
        'beards',
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
            self.trampolines = other.trampolines
            self.growth = other.growth
            self.neighbours8 = other.neighbours8
            
        
            self.data = copy(other.data)
            self.robot = other.robot
            self.collected_lambdas = other.collected_lambdas
            self.time = other.time
            self.final_score = other.final_score
            self.time_underwater = other.time_underwater
            self.razors = other.razors

    @classmethod
    def from_string(my_class, src):
        src, _, metadata = src.partition('\n\n')
        try:
            assert all(c in VALID_MAP_CHARACTERS for c in src)
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
        
        world = my_class()
        world.width = width
        world.lift = find_single_item(data, 'L')
        world.total_lambdas = data.count('\\') + data.count('@')
        world.neighbours8 = [d1 + d2 
                             for d1 in (-1, 0, 1) 
                             for d2 in (-width, 0, width)
                             if d1 + d2]
                
        world.data = data
        world.robot = find_single_item(data, 'R')
        world.collected_lambdas = 0
        world.time = 0
        world.final_score = None
        
        trampoline_mapping = {}
        metadict = {}
        for key, value in (line.split(' ', 1) for line in metadata.split('\n') if line):
            if key.upper() == 'TRAMPOLINE':
                src, _, trg = value.partition(' targets ')
                src, trg = [s.strip().upper() for s in (src, trg)]
                assert src and trg
                trampoline_mapping[src] = trg
            else:
                metadict[key] = value
                
        world.trampolines = enhance_trampoline_mapping(trampoline_mapping, world.data)
                
        world.water = int(metadict.get('Water', 0))
        world.flooding = int(metadict.get('Flooding', 0))
        world.waterproof = int(metadict.get('Waterproof', 10))
        world.growth = int(metadict.get('Growth', 25))
        world.time_underwater = 0
        world.razors = int(metadict.get("Razors", 0))

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
        global application_counter
        application_counter += 1
        assert not self.terminated
        
        new_world = self.__class__(self)
        
        # abort is not a command really
        if command == 'A':
            new_world.final_score = new_world.get_score_abort() 
            return new_world
        
        new_world.time += 1
        
        data = self.data
        new_data = new_world.data
        robot = self.robot
        width = self.width
        beards_cut = False
        
        if command == 'W':
            new_robot = robot
        elif command == 'S':
            if self.razors > 0:
                for d in self.neighbours8:
                    if new_data[robot + d] == 'W':
                        new_data[robot + d] = ' '
                        beards_cut = True
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
            elif new_cell == '@' and command in 'LR' and data[new_robot + direction] == ' ':
                new_data[new_robot + direction] = '@'                
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
            elif new_cell == '*' and command in 'LR' and data[new_robot + direction] == ' ':
                new_data[new_robot + direction] = '*'                
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
            elif new_cell in self.trampolines:
                destination, sources = self.trampolines[new_cell]
                new_robot = destination
                new_data[robot] = ' '
                new_data[new_robot] = 'R'
                for src in sources:
                    new_data[src] = ' '
            elif new_cell == '!':
                new_data[new_robot] = 'R'
                new_data[robot] = ' '
                new_world.razors += 1
            else:
#                warnings.warn('Action failed!')
                new_robot = robot
        if new_robot != robot or beards_cut:
            # another copy :( at least it's temporary
            data = new_data
            new_world.data = new_data = copy(new_data)
            new_world.robot = new_robot
            
        if new_robot >= len(data) - width * (new_world.water_level + 1):
            new_world.time_underwater += 1
            if new_world.time_underwater > new_world.waterproof:
                new_world.final_score = new_world.get_score_lose()
        else:
            new_world.time_underwater = 0
            
        def rock_falls(data, new_world, new_data, new_robot, cell, offset, new_offset):
            new_data[offset] = ' '
            below_new_offset = new_offset + width
            if cell == '@' and data[below_new_offset] != ' ': 
                new_data[new_offset] = '\\'
            else:
                new_data[new_offset] = cell
            if new_robot == below_new_offset:
                new_world.final_score = new_world.get_score_lose() 
        
        # pypy optimizer is funny
        ord_rock, ord_horock, ord_beard = ord('*'), ord('@'), ord('W')
        beards_growing = new_world.time % self.growth == 0 
        
        for i in reversed(xrange(1, len(data) / width - 1)):
            offset = i * width
            for offset in xrange(offset + 1, offset + width - 1):
                cell = data[offset]
                if ord(cell) == ord_rock or ord(cell) == ord_horock:
                    offset_below = offset + width 
                    cell_below = data[offset_below]
                    if cell_below == ' ':
                        rock_falls(data, new_world, new_data, new_robot, cell, offset, offset_below)
                    elif cell_below == '*' or cell_below == '^' or cell_below == '@':
                        # '^' is frozen stone (that is, 'slippery wall')
                        if data[offset + 1] == ' ' and data[offset_below + 1] == ' ':
                            rock_falls(data, new_world, new_data, new_robot, cell, offset, offset_below + 1)
                        elif data[offset - 1] == ' ' and data[offset_below - 1] == ' ':
                            rock_falls(data, new_world, new_data, new_robot, cell, offset, offset_below - 1)
                    elif cell_below == '\\':
                        if data[offset + 1] == ' ' and data[offset_below + 1] == ' ':
                            rock_falls(data, new_world, new_data, new_robot, cell, offset, offset_below + 1)
                elif ord(cell) == ord_beard and beards_growing:
                    for d in self.neighbours8:
                        if data[offset + d] == ' ':
                            new_data[offset + d] = 'W'
        

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
