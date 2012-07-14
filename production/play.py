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
        e = world.intermediate_score()
    
    print 'Final score:', e
    
    
if __name__ == '__main__':
    from dict_world import DictWorld
    
    world = DictWorld.load_file('../data/sample_maps/contest1.map')
    
    play(world)
