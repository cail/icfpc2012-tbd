from world_base import WorldBase


def assert_eq(a, b):
    assert a == b, (a, b)
    

class DualWorld(WorldBase):
    def __init__(self, w1, w2):
        self.error = ''
        self.w1 = w1
        self.w2 = w2
        s1 = w1.get_map_string()
        s2 = w2.get_map_string()
        if s1 != s2:
            self.error = 'simulation diverged!!'
            print 'simulation diverged!!!!!'
            print s1
            print '---'
            print s2
            print '---'
            #assert False
        
    @staticmethod
    def from_string(s):
        from dict_world import DictWorld
        from world import World
        return DualWorld(DictWorld.from_string(s), 
                         World.from_string(s))
        
    def apply_command(self, c):
        w1 = self.w1.apply_command(c)
        w2 = self.w2.apply_command(c)
        return DualWorld(w1, w2)
    
    def get_score_abort(self):
        s1 = self.w1.get_score_abort()
        s2 = self.w2.get_score_abort()
        if s1 == s2:
            return s1
        else:
            return self.error_message+'\n'+s1+'\n'+s2
    
    def get_map_string(self):
        result = self.w1.get_map_string()
        assert_eq(result, self.w2.get_map_string())
        return result
    
    def show(self):
        print self.get_map_string()
        print '(simulated by both {} and {})'.format(type(self.w1), type(self.w2))
        

    @property
    def terminated(self):
        result = self.w1.terminated
        assert_eq(result, self.w2.terminated)
        return result

    @property
    def score(self):
        result = self.w1.score
        assert_eq(result, self.w2.score)
        return result
    
    ##### data access interface
    
    @property
    def time(self):
        result = self.w1.time
        assert_eq(result, self.w2.time)
        return result
    
    @property
    def total_lambdas(self):
        result = self.w1.total_lambdas
        assert_eq(result, self.w2.total_lambdas)
        return result
    
    @property
    def collected_lambdas(self):
        result = self.w1.collected_lambdas
        assert_eq(result, self.w2.collected_lambdas)
        return result
        
    @property
    def robot_coords(self):
        result = self.w1.robot_coords
        assert_eq(result, self.w2.robot_coords)
        return result
    
    @property
    def lift_coords(self):
        result = self.w1.lift_coords
        assert_eq(result, self.w2.lift_coords)
        return result
    
    def __getitem__(self, coords):
        result = self.w1[coords]
        assert_eq(result, self.w2[coords])
        return result
    
    def enumerate_lambdas(self):
        result = set(self.w1.enumerate_lambdas())
        assert_eq(result, set(self.w2.enumerate_lambdas()))
        return result
    
    
    
