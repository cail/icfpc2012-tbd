from collections import defaultdict
import webvalidator
import re
import dual_world

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
    
    ('contest8', 'RRRRRRRULD'), # map should be completely evaluated on death
    ('contest8', 'RRRRRUD'), # and with down-up evaluation as well.     
    
    # Pls add your own tests everyone, especially for interesting cases
    ]

from world import World
from dict_world import DictWorld
from dual_world import DualWorld
from vorber_world import VorberWorld
world_classes = [World, DictWorld, DualWorld, VorberWorld] 

class WebValidatorProxy(object):
    def __init__(self, map_name, commands):
        self.score, self.map_string = webvalidator.validate(map_name, commands, 10.0)
    def get_map_string(self):
        return self.map_string

def official_map_file_name(map_name):
    return '../data/sample_maps/{}.map'.format(map_name)
    
def validate(map_name, commands, world_classes):
    '''Validate commands with given simulators, then (or on error) with the web-validator,
    return True if no deviations were found.
    
    `map_name` should be like 'contest3', without path or extension.
    
    Use validate_custom() to validate custom maps without the possibility to use the web-validator.
    '''
    with open(official_map_file_name(map_name)) as f:
        data = f.read()
    return validate_internal(data, commands, map_name, world_classes)
    
def validate_custom(map_path, commands, world_classes):
    '''Validate commands with given simulators, then (or on error) with the web-validator,
    return True if no deviations were found.
    
    `map_path` should be a proper pathname, like '../data/maps_manual/abort1.map'
    
    Use validate() to validate on standard maps against the web-validator.
    '''
    with open(map_path) as f:
        data = f.read()
    return validate_internal(data, commands, None, world_classes)
    
def validate_internal(map_data, commands, web_map_name, world_classes):
    '''Validate commands with given simulators, then (or on error) with the web-validator.
    
    Return True if no deviations were found.
    '''
    def format_world_state(world):
        return '{}\nScore:{!r}'.format(world.get_map_string(), world.score)
    
    def check_worlds(worlds, commands, prev_world, always_webvalidate = False):
        result_dict = defaultdict(list)
        for world in worlds:
            result_dict[format_world_state(world)].append(world.__class__.__name__)
            
        if web_map_name and (always_webvalidate or len(result_dict) > 1):
            web_world = WebValidatorProxy(web_map_name, commands)
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

    try:
        # dirty hack yo
        old_suppress_errors = dual_world.suppress_errors 
        dual_world.suppress_errors = True
        
        worlds = [cls.from_string(map_data) for cls in world_classes]
        
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
        if not web_map_name: 
            return True
        return check_worlds(worlds, commands, None, True)
    
    finally:
        dual_world.suppress_errors = old_suppress_errors
        

def run_all_tests(world_classes):
    total_tests = len(tests) 
    failed_tests = 0
    for i, (map_name, commands) in enumerate(tests):
        print '{}/{} {} {}'.format(i + 1, total_tests, map_name, commands)
        if not validate(map_name, commands, world_classes):
            failed_tests += 1
            break;
    if not failed_tests:
        print 'All tests pass!'
        return True
    print '{} of {} tests fail!'.format(failed_tests, total_tests)
    return False

def run_interactively(world, initial_commands=''):
    def cleanup(commands):
        return [c for c in commands.upper() if c in 'UDLRWA']
    def print_world(world):
        if hasattr(world, 'robot'):
            robot = world.robot 
            coords = world.index_to_coords(robot)
        elif hasattr(world, 'robot_coords'):
            robot = '-' 
            coords = world.robot_coords
        elif hasattr(world, 'robot_x'):
            robot = '-' 
            coords = (world.robot_x, world.robot_y) 
            
        print world.get_map_string()
        print 'Time: {:>2}, Robot: x={}, y={}, idx={}'.format(world.time, coords[0] + 1, coords[1] + 1, robot)
        if world.flooding:
            print 'Water level: {}, underwater: {}/{}'.format(
                    world.water_level, world.underwater, world.waterproof)
        print
        
    commands = cleanup(initial_commands)
    executed_commands = []
    print_world(world)
    while not world.terminated:
        while not commands:
            commands = cleanup(raw_input('> '))
        for c in commands:
            executed_commands.append(c)
            world = world.apply_command(c)
            print_world(world)
            if world.terminated: break
        commands = ''
    executed_commands = ''.join(executed_commands)
    print "Score:", world.score
    print "Commands:", executed_commands 
    return executed_commands
                       
if __name__ == '__main__':
    run_all_tests(world_classes)
