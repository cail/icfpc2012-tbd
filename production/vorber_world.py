from world_base import WorldBase
class VorberWorld(WorldBase):
    Empty = " "
    Earth = "."
    Wall = "#"
    Lambda = "\\"
    Rock = "*"
    Open = "O"
    Closed = "L"
    Robot = "R"
    Beard = "W"
    Razor = "!"
    LRock = "@"
    Trampoline = "ABCDEFGHI"
    TrampExit = "123456789"
    RockTypes = [Rock,LRock]

    #interface stuff:
    @staticmethod
    def from_string(s):
        w = VorberWorld(s)
        return w
    def get_map_string(self):
        a = []
        for l in range(self.height):
            i = self.height - l - 1
            line = self.world[i*self.width:(i+1)*self.width]
            #s = map(VorberWorld.elementToChar, line)
            s = line
            s+="\n"
            a += s
        res = "".join(a[:-1])
        return res

    def show(self):
        print self

    @property
    def terminated(self):
        return self.complete or self.aborted or self.dead

    @property
    def score(self):
        if self.check_end():
            return self.final_score
        else:
            return self.get_score_abort()

    def apply_command(self, c):
        assert not self.terminated
        self.move_player(c)
        if not self.terminated:
            self.update()
        return self

    #end interface stuff

    def lambda_count(self):
        return reduce(lambda a,b: a+b,  map(lambda e: 1 if e in [VorberWorld.Lambda, VorberWorld.LRock] else 0, self.world))

    def __init__(self, ss):
        s, _, metadata = ss.partition("\n\n")
        lines = s.split("\n")
        if len(lines[-1]) == 0:
            lines = lines[:-1]
        self.height = len(lines)
        self.time_underwater = 0
        elines = lines[::-1]
        self.width = max(map(len, elines))
        elines = map(lambda l:l+(self.width-len(l))*" ", elines)
        self.world = list(reduce(lambda a,b:a+b, elines))
        self.height = len(elines)
        self.width = max(map(len, elines))
        self.collected_lambdas = 0
        self.new_world = self.world[:]
        self.complete = False
        self.dead = False
        self.aborted = False
        self.can_lose = False
        self.final_score = 0
        self.time = 0
        self.initial_lambda_count = self.lambda_count()
        for l in lines:
            if 'R' in l:
                self.robot_x = l.index('R')
                self.robot_y = self.height - lines.index(l) - 1
                break
        self.parse_meta(metadata)
        self.flood_timer = self.flooding

    def parse_meta(self, metadata):
        metadict = dict(line.split(' ', 1) for line in metadata.split('\n') if line)
        self.water = int(metadict.get("Water", 0))
        self.flooding = int(metadict.get("Flooding", 0))
        self.waterproof = int(metadict.get("Waterproof", 0))
        self.growth = int(metadict.get("Growth", 25))
        self.razors = int(metadict.get("Razors", 0))
        self.trampolines = dict(line[11:].split(" targets ") for line in metadata.split('\n') if line.startswith("Trampoline"))

    def __repr__(self):
        res = "VorberWorld\n"
        res += self.get_map_string()
        res += "\nRobot pos: " + str(self.robot_x)+" " + str(self.robot_y) + "\n"
        res += "Turn: " + str(self.time) + "\n"
        res += "Water level: " + str(self.water) + "\n"
        res += "flood timer: " + str(self.flood_timer) + "\n"
        res += "time underwater: " + str(self.time_underwater) + "\n"
        res += "Razors: " + str(self.razors) + "\n"
        res += "Initial lambda count: " + str(self.initial_lambda_count) + "\n"
        res += "collected: "  + str(self.collected_lambdas) + "\n"

        return res

    def check_range(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True


    def get(self, x,y):
        if not self.check_range(x, y):
            return None
        return self.world[y*self.width+x]

    def get_new(self, x,y):
        if not self.check_range(x, y):
            return None
        return self.new_world[y*self.width+x]

    def set(self, x, y, value):
        if not self.check_range(x, y):
            return
        self.new_world[y*self.width + x] = value

    def set_in_world(self, x, y, value):
        if not self.check_range(x, y):
            return
        self.world[y*self.width + x] = value
        self.new_world[y*self.width + x] = value

    def grow_beard(self, x, y, value=Beard):
        if self.check_range(x,y):
            if value == VorberWorld.Beard:
                if self.get(x,y) == VorberWorld.Empty:
                    self.set(x,y,VorberWorld.Beard)
            elif value == VorberWorld.Empty:
                if self.get(x,y) == VorberWorld.Beard:
                    self.set(x,y, VorberWorld.Empty)
        else:
            print x, y, "onoes", self.get(x,y)

    def update_cell(self, x, y):
        t = self.get(x,y)
        if t in VorberWorld.RockTypes:
            fallen = False
            target = []
            if self.get(x, y-1) == VorberWorld.Empty:
                self.set(x, y, VorberWorld.Empty)
                self.set(x, y-1, t)
                target.append((x,y-1))
                fallen = True
            if self.get(x, y-1) in VorberWorld.RockTypes and self.get(x+1, y) == VorberWorld.Empty and self.get(x+1, y-1) == VorberWorld.Empty:
                self.set(x,y, VorberWorld.Empty)
                self.set(x+1,y-1, t)
                target.append((x+1, y-1))
                fallen = True
            if self.get(x, y-1) in VorberWorld.RockTypes and (self.get(x+1, y) != VorberWorld.Empty or self.get(x+1, y-1) != VorberWorld.Empty) and self.get(x-1, y) == VorberWorld.Empty and self.get(x-1,y-1) == VorberWorld.Empty:
                self.set(x,y, VorberWorld.Empty)
                self.set(x-1,y-1, t)
                target = (x-1,y-1)
                fallen = True
            if self.get(x,y-1) == VorberWorld.Lambda and self.get(x+1, y) == VorberWorld.Empty and self.get(x+1, y-1) == VorberWorld.Empty:
               self.set(x,y,VorberWorld.Empty)
               self.set(x+1,y-1, t)
               target.append((x+1, y-1))
               fallen = True
            if fallen:
                self.check_dead()
            if t == VorberWorld.LRock and fallen:
                print "FALLEN!", target
                tx,ty = target[0]
                d = self.get(tx,ty-1)
                print d
                if d not in [None, VorberWorld.Empty]:
                    print tx, ty
                    self.set(tx, ty ,VorberWorld.Lambda)


        if self.get(x,y) == VorberWorld.Closed and self.initial_lambda_count == self.collected_lambdas:
            self.set(x,y,VorberWorld.Open)

        if self.time % self.growth == 0:
            if self.get(x,y) == VorberWorld.Beard:
                self.grow_beard(x-1,y-1)
                self.grow_beard(x-1,y)
                self.grow_beard(x-1,y+1)
                self.grow_beard(x,y-1)
                self.grow_beard(x,y)
                self.grow_beard(x,y+1)
                self.grow_beard(x+1,y-1)
                self.grow_beard(x+1,y)
                self.grow_beard(x+1,y+1)


    def check_dead(self):
        if self.check_range(self.robot_x, self.robot_y + 1) and self.get(self.robot_x, self.robot_y + 1) not in VorberWorld.RockTypes and self.get_new(self.robot_x, self.robot_y+1) in VorberWorld.RockTypes:
            self.dead = True
        return self.dead


    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                self.update_cell(x, y)
                #if self.dead:

        if self.robot_y < self.water: # not <= since Water is 1-based and y is 0-based
            self.time_underwater += 1
        else:
            self.time_underwater = 0
        if self.time_underwater > self.waterproof:
            self.dead = True
        if self.flooding > 0:
            self.flood_timer -= 1
            if self.flood_timer == 0:
                self.water += 1
                self.flood_timer = self.flooding

        self.world = self.new_world[:]


    def move_player(self, move):
        old_x = self.robot_x
        old_y = self.robot_y
        cv = self.get(old_x, old_y)
        if cv != VorberWorld.Robot:
            return

        self.time += 1
        new_x = old_x
        new_y = old_y
        if move == 'L':
            new_x = old_x - 1
        if move == 'R':
            new_x = old_x + 1
        if move == 'U':
            new_y = old_y + 1
        if move == 'D':
            new_y = old_y - 1
        if move == 'A':
            self.time -= 1
            self.aborted = True
        if move == 'S':
            if self.razors > 0:
                self.razors -= 1
                self.grow_beard(old_x-1, old_y-1, VorberWorld.Empty)
                self.grow_beard(old_x-1, old_y, VorberWorld.Empty)
                self.grow_beard(old_x-1, old_y+1, VorberWorld.Empty)
                self.grow_beard(old_x, old_y-1, VorberWorld.Empty)
                self.grow_beard(old_x, old_y, VorberWorld.Empty)
                self.grow_beard(old_x, old_y+1, VorberWorld.Empty)
                self.grow_beard(old_x+1, old_y-1, VorberWorld.Empty)
                self.grow_beard(old_x+1, old_y, VorberWorld.Empty)
                self.grow_beard(old_x+1, old_y+1, VorberWorld.Empty)
        if move == 'W':
            pass

        if abs(old_x - new_x) + abs(old_y - new_y) == 1:

            tv = self.get(new_x, new_y)
            if tv in [VorberWorld.Empty, VorberWorld.Earth, VorberWorld.Lambda, VorberWorld.Open, VorberWorld.Razor]:
                if tv == VorberWorld.Lambda:
                    self.collected_lambdas+= 1
                if tv == VorberWorld.Open:
                    self.complete = True
                    self.robot_x = new_x
                    self.robot_y = new_y
                    self.set_in_world(old_x, old_y, VorberWorld.Empty)
                    return
                if tv == VorberWorld.Razor:
                    self.razors += 1
                self.robot_x = new_x
                self.robot_y = new_y
                self.set_in_world(new_x, new_y, VorberWorld.Robot)
                self.set_in_world(old_x, old_y, VorberWorld.Empty)
            if tv is not None and tv in VorberWorld.Trampoline:
                dest = self.trampolines[tv]
                print "dest: ", dest
                idx = self.new_world.index(dest)
                self.new_world[idx] = VorberWorld.Robot
                self.robot_x = idx % self.width
                self.robot_y = idx / self.width
                self.set_in_world(old_x, old_y, VorberWorld.Empty)
                for t in self.trampolines.keys():
                    if self.trampolines[t] == dest:
                        self.trampolines.pop(t)
                        self.new_world[self.world.index(t)] = VorberWorld.Empty

            if tv in VorberWorld.RockTypes and old_x + 1 == new_x and old_y == new_y and self.check_range(old_x+2, old_y) and self.get(old_x+2, old_y) == VorberWorld.Empty:
                self.robot_x = new_x
                self.robot_y = new_y
                self.set_in_world(new_x, new_y, VorberWorld.Robot)
                self.set_in_world(old_x, old_y, VorberWorld.Empty)
                self.set_in_world(new_x+1, new_y, tv)
            if tv in VorberWorld.RockTypes and old_x - 1 == new_x and old_y == new_y and self.check_range(old_x-2, old_y) and self.get(old_x-2, old_y) == VorberWorld.Empty:
                self.robot_x = new_x
                self.robot_y = new_y
                self.set_in_world(new_x, new_y, VorberWorld.Robot)
                self.set_in_world(old_x, old_y, VorberWorld.Empty)
                self.set_in_world(new_x-1, new_y, tv)
        else:
            pass

    def check_end(self):
        if self.final_score != 0:
            return True
        if self.complete:
            self.final_score += self.collected_lambdas*75 - self.time
            return True
        if self.dead:
            self.final_score += self.collected_lambdas*25 - self.time
            return True
        if self.aborted:
            self.final_score += self.collected_lambdas*50 - self.time
            return True
        return False

    def run_chain(self, chain):
        for c in chain:
            self.move_player(c)
            self.update()
            if self.check_end():
                break
        return self.score

if __name__ == "__main__":
    mmap = VorberWorld.from_file("../data/sample_maps/horock1.map")
    route = "WWWWWWWWWWWWWWWWWWWLLLUUUUUULLLLLLLLLRRRRRRRRRRRR"
    interactive = True
    if interactive:
        path = ""
        Done = False
        while not Done:
            print mmap
            m = raw_input("Your Move: ").upper()[0]
            path += m
            mmap.move_player(m)
            mmap.update()
            Done = mmap.check_end()

        print mmap
        print "Score: ", mmap.score
        print "Path:", path
    else:
        print "Score: ", mmap.run_chain(route)
        print mmap


