

class Map(object):

    @staticmethod
    def load(file_name):
        map = Map()
        with open(file_name) as fin:
            lines = [line.rstrip() for line in fin]

        assert all(len(line) == len(lines[0]) for line in lines)
                    
        map.data = {}
        map.height = len(lines)
        map.width = len(lines[0].rstrip('\n'))
            
        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip('\n')):
                map.data[j, map.height-1-i] = c
                
        return map
    
    def show(self):
        for i in range(self.height):
            print ''.join(self.data[j, self.height-1-i] 
                          for j in range(self.width))
            
    
def main():
    map = Map.load('contest1.map')
    map.show()


if __name__ == '__main__':
    main()