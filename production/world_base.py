

class WorldBase(object):

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return cls.from_string(f.read())

    def get_score_abort(self):
        return 50*self.collected_lambdas-self.time
