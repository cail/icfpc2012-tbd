

def validate(simulator, map_name, route):
    '''Validate with my emulator
    
    Follows webvalidator interface, except that as a first parameter it takes
    simulator class. 
    Return tuple (score, world).
    '''
    
    route, _, _ = route.partition('A')
    
    world = simulator.from_file('../data/sample_maps/{}.map'.format(map_name))
    
    for c in route:
        world = world.apply_command(c)
        if world.terminated:
            break
        
    return (world.score, world.get_map_string())
