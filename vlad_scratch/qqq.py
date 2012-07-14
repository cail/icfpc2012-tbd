from dict_world import DictWorld
from world import World
from dual_world import DualWorld
from play import play

    
if __name__ == '__main__':
    
    map_name = '../data/sample_maps/contest8.map'
    world = DualWorld(DictWorld.from_file(map_name),
                      World.from_file(map_name))
    
    play(world)
