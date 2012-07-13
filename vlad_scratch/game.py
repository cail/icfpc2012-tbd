

class Map(object):
    __slots__ = [
        'width',
        'height',
        'data',
        'robot',   # (x, y); zero based, because!
        'aborted', # whether robot executed Abort
        'lifted',  # whether robot has entered lambda lift 
        'dead',    # whether robot was killed by rock
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
        map.aborted = False
        map.lifted = False
        map.dead = False
            
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
        
    def execute_command(self, c):
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
        
    def move(self, dx, dy):
        ''' move robot only 
        
        Without map update step. 
        Return whether move was sucessfull.'''
        
        assert dx*dx+dy*dy == 1
        
        x, y = self.robot
        new_cell = self.data.get((x+dx, y+dy), '#')
        if new_cell in ' .\\O':
            if new_cell == 'O':
                self.lifted = True
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
        
    def update(self):
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
        
    def ending(self):
        '''return either None or additional score'''
        if self.lifted:
            return 50
        if self.dead:
            return 0
        if self.aborted:
            return 25
    
                

def play(map):
    map.show()
    while True:
        print '>>>',
        commands = raw_input()
        for c in commands:
            map.execute_command(c)
            map.update()
            map.show()
            e = map.ending()
            if e is not None:
                map.show()
                print 'Ending score:', e
                return
    
    
def main():
    map = Map.load('../data/sample_maps/contest1.map')
    
    play(map)


if __name__ == '__main__':
    main()