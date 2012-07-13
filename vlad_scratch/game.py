

class Map(object):
    __slots__ = [
        'width',
        'height',
        'data',
        'robot',    # (x, y); zero based, because!
    ]

    @staticmethod
    def load(file_name):
        map = Map()
        with open(file_name) as fin:
            lines = [line.rstrip() for line in fin]

        assert all(len(line) == len(lines[0]) for line in lines)
                    
        map.data = {}
        map.height = len(lines)
        map.width = len(lines[0].rstrip('\n'))
        map.robot = None
            
        for i, line in enumerate(lines):
            i = map.height-1-i
            for j, c in enumerate(line.strip('\n')):
                map.data[j, i] = c
                if c == 'R':
                    assert map.robot is None
                    map.robot = j, i
                
        return map
    
    def show(self):
        for i in range(self.height):
            print ''.join(self.data[j, self.height-1-i] 
                          for j in range(self.width))
        print 'robot at', self.robot
        
    def move(self, dx, dy):
        ''' move robot only 
        
        Without map update step. 
        Return whether move was sucessfull.'''
        
        assert dx*dx+dy*dy == 1
        
        x, y = self.robot
        new_cell = self.data.get((x+dx, y+dy), '#')
        if new_cell in ' .\\O':
            self.data[self.robot] = ' '
            self.robot = x+dx, y+dy
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
        
            
    
def main():
    map = Map.load('../data/sample_maps/contest1.map')
    map.show()
    print map.move(-1, 0)
    map.show()


if __name__ == '__main__':
    main()