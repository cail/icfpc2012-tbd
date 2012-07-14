

class WorldBase(object):
    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return cls.from_string(f.read())

    def get_score_lose(self):
        return self.collected_lambdas * 25 - self.time
    
    def get_score_abort(self):
        return self.collected_lambdas * 25 - self.time
    
    def get_score_win(self):
        return self.collected_lambdas * 75 - self.time
    
