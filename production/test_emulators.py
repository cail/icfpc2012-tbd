from collections import defaultdict

tests = [
    ('contest1', 'LDRDDULULLDD'), # almost complete solution
    ('contest1', 'LDRDDULULLDDL'), # complete optimal solution
    ('contest2', 'RRUDRRULURULLLLDDDL'), # complete optimal solution
    ('contest3', 'LDDDRRRRDDLLLLLDRRURRURUR'), # complete optimal(?) solution
    
    ('contest8', 'WWWRRRLLLWWWA'), # abort or death?

    ('contest1', 'LW'), # there was a bug
    
    # flood is not implemented in fj's world    
    ('flood1', 'LLLLDDDDDWWWWUUUWWWWWW'), # surface barely in time
    ('flood1', 'LLLLDDDDDWWWWWWWWWWWW'), # drowning
    ('flood1', 'W'*100), # passive drowning
    # write your own tests, especially for interesting cases
    ]
    

def web_validate(map_name, commands):
    from webvalidator import validate
    return validate(map_name, commands, 10.0)

def validate(map_name, commands, *world_classes):
    '''Validate with my emulator
    
    Follows webvalidator interface, except that as a first parameter it takes
    simulator class. 
    Return tuple (score, world).
    '''
    def format_state(world_map, result):
        return '{}\nResult:{!r}'.format(world_map, result)
    
    def check_worlds(worlds, commands, prev_map, always_webvalidate = False):
        result_dict = defaultdict(list)
        for world, result in worlds:
            result_dict[format_state(world.get_map_string(), result)].append(world.__class__.__name__)
        if always_webvalidate or len(result_dict) > 1:
            webcmd = ''.join(c for c in commands if c in 'UDLRWA')
            web_score, web_map = web_validate(map_name, webcmd)
            result_dict[format_state(web_map, web_score)].insert(0, '*Web validator*')
        if len(result_dict) > 1:
            print 'Emulations diverge after', commands  
            print 'Previous state:'
            print format_state(prev_map, None)
            print
            for result, emulators in result_dict.iteritems():
                print '## ' + ', '.join(emulators)
                print result
                print
            print
            return False
        return True
    
    assert len(world_classes)
        
    worlds = [(cls.from_file('../data/sample_maps/{}.map'.format(map_name)), None) for cls in world_classes]
    
    # check initial states
    if not check_worlds(worlds, '<just created>', ''): return False
    
    for i, c in enumerate(commands):
        new_worlds = [world.apply_command(c) for world, result in worlds]
        prev_map = worlds[0][0].get_map_string()
        if not check_worlds(new_worlds, commands[:i+1], prev_map): return False
        if new_worlds[0][1] is not None:
            return check_worlds(new_worlds, commands[:i+1], worlds[0][0].get_map_string(), prev_map)
        worlds = new_worlds
    # check last state
    for i, (world, result) in enumerate(worlds):
        if result is None:
            worlds[i] = (world, world.get_score_abort())
    return check_worlds(worlds, commands + ' <forced abort>', ('Same as this', None), True)    

def run_all_tests():
    from world import World
    from dict_world import DictWorld
    total_tests = len(tests) 
    failed_tests = 0
    for i, (map_name, commands) in enumerate(tests):
        print '{}/{} {} {}'.format(i + 1, total_tests, map_name, commands)
        if not validate(map_name, commands, World, DictWorld):
            failed_tests += 1
    if not failed_tests:
        print 'All tests pass!'
        return True
    print '{} of {} tests fail!'.format(failed_tests, total_tests)
    return False


if __name__ == '__main__':
    run_all_tests()