from time import clock
import logging


class StopSearch(Exception):
    pass


class SolverBase(object):
    def __init__(self, world, timeout=None):
        self.best_score = 0
        self.best_solution = ''
        self.timeout = timeout
        self.start = clock()
        self.stop_flag = False
        
    def check_stop(self):
        if self.stop_flag or \
           self.timeout is not None and clock()-self.start > self.timeout:
            raise StopSearch()
        
    def signal_stop(self):
        self.stop_flag = True
        
    def search(self):
        raise NotImplementedError()    
    
    def solve(self):
        try:
            self.search()
        except StopSearch:
            logging.info('StopSearch exception')
            pass
        