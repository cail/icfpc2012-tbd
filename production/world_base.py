

class WorldBase(object):
    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return cls.from_string(f.read())
        
    def apply_commands(self, commands):
        world = self
        for command in commands:
            if world.terminated:
                break
            world = world.apply_command(command)
        return world

    def get_score_lose(self):
        return self.collected_lambdas * 25 - self.time
    
    def get_score_abort(self):
        return self.collected_lambdas * 50 - self.time
    
    def get_score_win(self):
        return self.collected_lambdas * 75 - self.time
    
