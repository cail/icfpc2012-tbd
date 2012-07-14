

def validate(simulator, map_name, route):
    '''Validate with my emulator
    
    Follows webvalidator interface, except that as a first parameter it takes
    simulator class. 
    Return tuple (score, world).
    '''
    
    route, _, _ = route.partition('A')
    
    world = simulator.load_file('../data/sample_maps/{}.map'.format(map_name))
    
    e = None
    for c in route:
        world, e = world.apply_command(c)
        if e is not None:
            break
        
    if e is not None:
        score = e
    else:
        score = world.intermediate_score()
        assert score is not None
        
    return (score, world.get_map_string())
