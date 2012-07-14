

class DualWorld(object):
    def __init__(self, w1, w2):
        self.w1 = w1
        self.w2 = w2
        assert w1.get_map_string() == w2.get_map_string()
        
    def apply_command(self, c):
        w1, e1 = self.w1.apply_command(c)
        w2, e2 = self.w2.apply_command(c)
        assert e1 == e2   
        return DualWorld(w1, w2), e1
    
    def get_score_abort(self):
        s1 = self.w1.get_score_abort()
        s2 = self.w2.get_score_abort()
        assert s1 == s2
        return s1
    
    def get_map_string(self):
        result = self.w1.get_map_string()
        assert result == self.w2.get_map_string()
        return result
    
    def show(self):
        print self.get_map_string()
        print '(simulated by both {} and {})'.format(type(self.w1), type(self.w2))