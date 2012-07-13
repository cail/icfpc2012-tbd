

class Map(object):
    __slots__ = [
        'width',
        'height',
        'data',
        'robot',    # (x, y); zero based, because!
        'lambdas',
        'moves',
        'dead',
        'lifted',
        'aborted'
    ]

    @staticmethod
    def load(file_name):
        map = Map()
        with open(file_name) as fin:
            lines = [line.rstrip() for line in fin]

        assert all(len(line) == len(lines[0]) for line in lines)

        map.data = {}
        map.lambdas = 0
        map.moves = 0
        map.dead = False
        map.lifted = False
        map.aborted = False
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
        print 'moves:', self.moves
        print 'lambdas:', self.lambdas
        print 'dead:', self.dead
        print 'aborted:', self.aborted
        print 'lifted:', self.lifted
        if self.dead:
            print 'score:',self.score()

    def move(self, dx, dy):
        ''' move robot only

        Without map update step.
        Return False if move failed, a character indicating what we've visited otherwise..'''

        assert dx*dx+dy*dy == 1

        x, y = self.robot
        new_cell = self.data.get((x+dx, y+dy), '#')
        if new_cell in ' .\\O':
            self.data[self.robot] = ' '
            self.robot = x+dx, y+dy
            self.data[self.robot] = 'R'
            return new_cell

        if dy == 0 and new_cell == '*':
            behind = (x+2*dx, y)
            if self.data.get(behind) == ' ':
                self.data[self.robot] = ' '
                self.robot = x+dx, y+dy
                self.data[self.robot] = 'R'
                self.data[behind] = '*'
                return new_cell

        return False

    def update(self):
        '''updates the map.
        returns whether the robot is dead after the update.'''

        data = self.data
        u = {}

        has_lambdas = '\\' in data.values()
        # because lambdas can not disappear during updates

        res = False
        for (x, y), c in data.items():
            # because it's actually irrelevant in what order we update
            if c == '*':
                under = data.get((x, y-1))
                if under == ' ':
                    u[x, y] = ' '
                    u[x, y-1] = '*'
                    if self.robot == (x, y-2):
                        res = True
                elif under == '*':
                    if data.get((x+1, y)) == ' ' and data.get((x+1, y-1)) == ' ':
                        u[x, y] = ' '
                        u[x+1, y-1] = '*'
                        if self.robot == (x+1, y-2):
                            res = True
                        continue
                    if data.get((x-1, y)) == ' ' and data.get((x-1, y-1)) == ' ':
                        u[x, y] = ' '
                        u[x-1, y-1] = '*'
                        if self.robot == (x-1, y-2):
                            res = True
                        continue
                elif under == '\\':
                    if data.get((x+1, y)) == ' ' and data.get((x+1, y-1)) == ' ':
                        u[x, y] = ' '
                        u[x+1, y-1] = '*'
                        if self.robot == (x+1, y-2):
                            res = True
            if c == 'L' and not has_lambdas:
                u[x, y] = 'O'

        data.update(**u)
        return res

    def execute(self, command):
        '''executes one command for the robot.
        returns whether the game is finished after this move.
        '''
        assert not self.dead

        if command == 'A':
            self.dead = True
            self.aborted = True
            return True
        elif command == 'W':
            self.moves += 1
            self.dead = self.update()
            return not self.dead
        elif command in 'UDLR':
            dx = 0
            dy = 0
            if command == 'U':
                dy = 1
            elif command == 'D':
                dy = -1
            elif command == 'L':
                dx = -1
            elif command == 'R':
                dx = 1
            visited = self.move(dx, dy)
            if visited == '\\':
                self.lambdas += 1
            elif visited == 'O':
                self.dead = True
                self.lifted = True
            self.moves += 1
            self.dead = self.dead or self.update()
            return not self.dead

    def score(self):
        res = -self.moves
        res += self.lambdas * 25
        if self.aborted:
            res += self.lambdas * 25
        if self.lifted:
            res += self.lambdas * 50
        return res


def main():
    map = Map.load('../data/sample_maps/contest1.map')
    map.show()
    print map.move(-1, 0)
    map.show()
    map.update()
    map.show()


if __name__ == '__main__':
    main()
