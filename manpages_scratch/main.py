from world import World

if __name__ == '__main__':
    import os, logging, pprint, world

    PRODUCTION = 'production'
    PATH = os.path.dirname(__file__)
    
    # Please note that in the release logging is to be turned off globally.
    # That snippet does the job for development-mode work with production
    if PRODUCTION in PATH:
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.DEBUG)
    logging.info('Directory name %s', PATH)
    
    world = World.from_file('../data/sample_maps/contest1.map')
    world.show()
    pprint.pprint([x for x in world.enumerate_lambdas()], None)
    pprint.pprint(world[0,1])
    #logging.debug('%i', world.robot)
    