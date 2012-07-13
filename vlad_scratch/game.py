

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
            
    
def main():
    map = Map.load('contest1.map')
    map.show()


if __name__ == '__main__':
    main()