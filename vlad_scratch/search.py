import sys
sys.path.append('../production') # for pypy


import logging

from time import clock, sleep
from collections import defaultdict, Counter
from itertools import product, islice

from mask_errors import failsafe
from solver_base import SolverBase
from preprocessor import preprocess_world
from upper_bound import upper_bound
from utils import dist, path_to_nearest_lambda_or_lift, interesting_actions


class PathEntry(object):
    __slots__ = [
        'cache_entry',
        'command',
        ]
    def __repr__(self):
        return 'PathEntry(cache_entry={}, command={!r})'.format(self.cache_entry, self.command)
    
class CacheEntry(object):
    __slots__ = [
        'time',
        'command', # recommended command
        ]

class Solver(SolverBase):
    def __init__(self, world, timeout=15):
        SolverBase.__init__(self, world, timeout)
        
        self.cache = {} # aggressively preprocessed state hash -> cache entry
        
        self.ub_ce_cache = {} # raw world hash -> (ub, cache entry)
        
        self.path = []
        self.state = world
        
        self.stats = defaultdict(int)
    
                
    def get_ub_and_cache_entry(self, world):
        '''
        return upper bound and CacheEntry;
        
        given world is raw (not even preprocessed);
        calls are cached
        '''
        assert not world.terminated
        
        raw_hash = world.get_hash()
        result = self.ub_ce_cache.get(raw_hash)
        if result is not None:
            self.stats['ub ce hit'] += 1
            ub, cache_entry = result
            return ub-world.time, cache_entry

        self.check_stop()

        preprocessed = preprocess_world(world)
        self.stats['preprocess'] += 1
        
        ub = upper_bound(preprocessed)
        
        aggressive_preprocess(preprocessed) #inplace
        
        key = preprocessed.get_hash()
        cache_entry = self.cache.get(key)
        if cache_entry is None:
            cache_entry = self.cache[key] = CacheEntry()
            cache_entry.time = 100000000
            cache_entry.command = None
            
        self.ub_ce_cache[raw_hash] = ub, cache_entry
        return ub-world.time, cache_entry
        
    def check(self):
        if self.state.score > self.best_score:
            self.best_score = self.state.score
            self.best_solution = ' '.join(p.command for p in self.path)
            logging.info('better solution found {} {!r}'.format(self.best_score, self.best_solution))
            
            for pe in self.path:
                pe.cache_entry.command = pe.command
    
    def rec(self, depth, stack_depth):
        self.stats['node'] += 1
        self.check()
        
        self.check_stop()
        
        if depth <= 0 or stack_depth <= 0 or self.state.terminated:
            return
        
        ub, cache_entry = self.get_ub_and_cache_entry(self.state)
        
        t = self.state.time
        if cache_entry.time <= t:
            self.stats['cache cut'] += 1
            return
        cache_entry.time = t

        if ub <= self.best_score:
            self.stats['ub cut'] += 1
            return
        
        current_state = self.state
        
        ia = []
        greedy_commands = []
        if cache_entry.command is not None:
            greedy_commands = [cache_entry.command]
        else:
            ia = interesting_actions(preprocess_world(current_state)) # TODO: remove preprocessing step
            
            if ia:
                greedy_commands = ia[:1]
                ia = ia[1:]
            
            #ptn = path_to_nearest_lambda_or_lift(current_state)
            #if ptn is not None:
            #    _, ptn = ptn
            #    assert len(ptn) > 0
            #    greedy_commands = [ptn]
        
        
        #ordinary_commands = list('LRUDW')
        ordinary_commands = [''.join(cmd) for cmd in product('LRUDW', repeat=1)]
        # TODO: remove those that lead to duplicates
        
        ordinary_commands.extend(ia)
        
        for g in greedy_commands:
            if g in ordinary_commands:
                ordinary_commands.remove(g)
                
        
        def visit_child(cmd, depth_delta):
            pe = PathEntry()
            pe.cache_entry = cache_entry
            pe.command = cmd
            
            self.state = current_state.apply_commands(cmd)
            self.path.append(pe)
            
            self.rec(depth-depth_delta, stack_depth-1)
            
            self.path.pop()
        
        
        for cmd in greedy_commands:
            visit_child(cmd, 0)
        
        children = {}
        for cmd in ordinary_commands:
            self.check_stop()
            t = current_state.apply_commands(cmd)
            if t.terminated:
                ub = t.score
            else:
                ub, _ = self.get_ub_and_cache_entry(t)
            children[cmd] = ub
            
        ordinary_commands = sorted(children, key=children.get, reverse=True)
        
        for cmd in ordinary_commands:
            visit_child(cmd, 1)
        
        self.state = current_state
        
    
    @failsafe(default=None)
    def search(self):
        stack_depth = min(200, 10**8//len(self.state.data))
        logging.info('Max stack depth: {}'.format(stack_depth))
        
        for depth in range(0, 100, 1):
            logging.info('depth: {}'.format(depth))
            self.rec(depth, stack_depth)
            
            for cache_entry in self.cache.itervalues():
                cache_entry.time += 1e-3
        
            
    def log_stats(self):
        logging.info('{} cache entries'.format(len(self.cache)))
        logging.info('{} ub_ce_cache entries'.format(len(self.ub_ce_cache)))
        logging.info('stats: {}'.format(self.stats))
        logging.info('{} preprocesses per second'.format(self.stats['preprocess']/(clock()-self.start+1e-3)))
        logging.info('search took {}s'.format(clock()-self.start))
    
    def get_best(self):
        return self.best_score, self.best_solution.replace(' ', '')
    


@failsafe(default=None)
def aggressive_preprocess(world):
    '''
    inplace, because why not?
    '''
    #return

    data = world.data
    rx, ry = rxy = world.robot_coords
    num_lambdas = 0
    
    sectors = [Counter() for _ in range(4)]
    
    for i in range(len(data)):
        xy = world.index_to_coords(i)
        if dist(rxy, xy) > 7:
            if data[i] in '\\*':
                x, y = xy
                idx = 0
                if x-rx > y-ry:
                    idx += 1
                if x-rx > ry-y:
                    idx += 2
                sectors[idx][data[i]] += 1
            data[i] = '?'
    for sector in sectors:
        data.extend(sector.elements())


    
def main():
    
    FORMAT = '%(levelname)7s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    
    from world import World
    from dual_world import DualWorld
    from dict_world import DictWorld
    from test_emulators import validate_custom, validate

    
    map_name = 'horock3'
    map_path = '../data/sample_maps/{}.map'.format(map_name)
    #map_path = '../data/maps_manual/horo2.map'
    world = World.from_file(map_path)
    
    world.show()
    
    sleep(0.1) # for stdout to flush
    
    solver = Solver(world)
    solver.solve()
    score, solution = solver.get_best()
    solver.log_stats()

    sleep(0.1) # for stderr to flush
    
    print '****'
    print 'Solution:', score, repr(solution)
    
    '''
    print 'validating...',
    
    world = DualWorld.from_file(map_path)
    for cmd in solution:
        world = world.apply_command(cmd)
        if world.terminated:
            break
    validated_score = world.score
    
    assert score == validated_score, (score, validated_score)
    '''
    
    validate(map_name, solution, [World])
    #validate_custom(map_path, solution, [World])#, DictWorld, DualWorld])
    
    print 'ok'
    
    
if __name__ == '__main__':
    main()    