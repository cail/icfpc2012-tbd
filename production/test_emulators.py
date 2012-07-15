from collections import defaultdict
import webvalidator
import re

tests = [
    ('contest1', 'LDRDDULULLDD'), # almost complete solution
    ('contest1', 'LDRDDULULLDDL'), # complete optimal solution
    ('contest1', 'LDRDDULULLDDLLLL'), # complete solution with extra stuff
    ('contest2', 'RRUDRRULURULLLLDDDL'), # complete optimal solution
    ('contest3', 'LDDDRRRRDDLLLLLDRRURRURUR'), # complete optimal(?) solution
    
    ('contest5', 'LLURURUUURRRRRUULLL'), # reasonably good solutions
    ('contest6', 'RUULRRRRRRRRRRUUULLLLLLLDLLLUUUUUURULURR'),
        
    ('contest8', 'WWWRRRLLLWWWA'), # abort or death?

    ('contest1', 'LW'), # there was a bug
    
    ('flood1', 'LLLLDDDDDWWWWUUUWWWWWW'), # surface barely in time
    ('flood1', 'LLLLDDDDDWWWWWWWWWWWW'), # drowning
    ('flood1', 'W'*100), # passive drowning

    ('flood1', 'WWWWWWWWLLLLWWWDDDWDWWWWU'), # jump out of water the same turn water rises on the last turn of waterproof

    ('flood1', 'LLLLDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWUWWW'), # goes really wrong if you forget to reset underwater timer when getting out 
    
    
    
    # Pls add your own tests everyone, especially for interesting cases
    ]


class WebValidatorProxy(object):
    def __init__(self, map_name, commands):
        self.score, self.map_string = webvalidator.validate(map_name, commands, 10.0)
    def get_map_string(self):
        return self.map_string

def validate(map_name, commands, *world_classes):
    '''Validate commands with given simulators, then (or on error) with the web-validator.
    
    Return True if no deviations were found.
    '''
    can_has_webvalidator = re.match(r'^(contest|flood|trampoline)\d+$', map_name) is not None
    
    def format_world_state(world):
        return '{}\nScore:{!r}'.format(world.get_map_string(), world.score)
    
    def check_worlds(worlds, commands, prev_world, always_webvalidate = False):
        result_dict = defaultdict(list)
        for world in worlds:
            result_dict[format_world_state(world)].append(world.__class__.__name__)
            
        if can_has_webvalidator and (always_webvalidate or len(result_dict) > 1):
            web_world = WebValidatorProxy(map_name, commands)
            result_dict[format_world_state(web_world)].insert(0, '*Web validator*')
            
        if len(result_dict) > 1:
            print 'Simulations diverge after {!r}'.format(commands)
            if prev_world is not None:  
                print 'Previous state:'
                print format_world_state(prev_world)
                print
            for result, emulators in result_dict.iteritems():
                print '## ' + ', '.join(emulators)
                print result
                print
            print
            return False
        return True
    
    assert len(world_classes)
        
    worlds = [cls.from_file('../data/sample_maps/{}.map'.format(map_name)) for cls in world_classes]
    # check initial states
    if not check_worlds(worlds, '', None): return False
    
    for i, c in enumerate(commands):
        prev_world = worlds[0]
        worlds = [world.apply_command(c) for world in worlds]
        if not check_worlds(worlds, commands[:i+1], prev_world): return False
        terminated, not_terminated = [], []
        for w in worlds:
            (terminated if w.terminated else not_terminated).append(w.__class__.__name__)
        if terminated and not_terminated:
            if all(w.terminated for w in worlds): break
            print 'Simulations diverge after {!r}'.format(commands)
            print format_world_state(worlds[0])
            print 'Terminated:', ', '.join(terminated)
            print 'Not terminated:', ', '.join(not_terminated)
            return False
        if terminated:
            break
    # check last state against the web-validator if possible
    if not can_has_webvalidator: 
        return True
    return check_worlds(worlds, commands, None, True)

def run_all_tests(*world_classes):
    total_tests = len(tests) 
    failed_tests = 0
    for i, (map_name, commands) in enumerate(tests):
        print '{}/{} {} {}'.format(i + 1, total_tests, map_name, commands)
        if not validate(map_name, commands, *world_classes):
            failed_tests += 1
            break;
    if not failed_tests:
        print 'All tests pass!'
        return True
    print '{} of {} tests fail!'.format(failed_tests, total_tests)
    return False

                       
if __name__ == '__main__':
    from world import World
    from dict_world import DictWorld
    from dual_world import DualWorld
    from vorber_world import VorberWorld
    run_all_tests(World, DictWorld, DualWorld, VorberWorld)
