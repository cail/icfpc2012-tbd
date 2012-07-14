def play(world):
    world.show()
    e = None
    finished = False
    while not finished:
        print '>>>',
        commands = raw_input()
        for c in commands:
            if c == 'A':
                finished = True
                break
            world, e = world.apply_command(c)
            world.show()
            if e is not None:
                finished = True
                break


    if e is None:
        e = world.get_score_abort()
    
    print 'Final score:', e
    
    
if __name__ == '__main__':
    from dict_world import DictWorld
    from world import World
    from dual_world import DualWorld
    
    map_name = '../data/sample_maps/contest1.map'
    world = DualWorld(DictWorld.from_file(map_name),
                      World.from_file(map_name))
    
    play(world)
