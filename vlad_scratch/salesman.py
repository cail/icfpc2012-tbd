from utils import dist, enumerate_paths_to_goals



def salesman_lower_bound_naive(world, need_exit=True):
    
    if world.collected_lambdas == world.total_lambdas:
        # go straight to exit
        return dist(world.robot_coords, world.lift_coords)
    
    max_dist = 0
    for xy in world.enumerate_lambdas():
        d1 = dist(world.robot_coords, xy)
        if need_exit:
            d2 = dist(xy, world.lift_coords)
        else:
            d2 = 0
        #print d1, d2
        max_dist = max(max_dist, 
                       d1+d2)
    return max_dist


def salesman_lower_bound_(world, need_exit=True):
    walkable = ' .!*\\R' # TODO: all allowed chars except # and ^
    
    if world.collected_lambdas == world.total_lambdas:
        # go straight to exit
        #return dist(world.robot_coords, world.lift_coords)
        _, path = next(e for goal in 'OL' for e in 
                       enumerate_paths_to_goals(world,
                                                start=world.robot,
                                                walkable=walkable,
                                                goal=goal))
        return len(path)
    max_dist = 0
    for idx, path in enumerate_paths_to_goals(world, 
                                              start=world.robot, 
                                              walkable=walkable,
                                              goal='\\'):
        d1 = len(path)
        if need_exit:
            _, path2 = next(enumerate_paths_to_goals(world,
                                                     start=idx,
                                                     walkable=walkable,
                                                     goal='L'))
            d2 = len(path2)
        else:
            path2 = ''
            d2 = 0
                
        #print d1, d2, (path, idx, path2)
        
        max_dist = max(max_dist, 
                       d1+d2)
    assert max_dist >= salesman_lower_bound_naive(world, need_exit)            
    return max_dist


def salesman_lower_bound(world, need_exit=True):
    walkable = ' .!*\\R' # TODO: all allowed chars except # and ^
    
    if world.collected_lambdas == world.total_lambdas:
        # go straight to exit
        #return dist(world.robot_coords, world.lift_coords)
        _, path = next(e for goal in 'OL' for e in 
                       enumerate_paths_to_goals(world,
                                                start=world.robot,
                                                walkable=walkable,
                                                goal=goal))
        return len(path)
    
    dists1 = {}
    for idx, path in enumerate_paths_to_goals(world, 
                                              start=world.robot, 
                                              walkable=walkable,
                                              goal='\\'):
        #print idx, path
        dists1[idx] = len(path)
        
    if need_exit:
        dists2 = {}
        for idx, path in enumerate_paths_to_goals(world, 
                                                  start=world.lift, 
                                                  walkable=walkable,
                                                  goal='\\'):
            dists2[idx] = len(path)
            
        assert set(dists1.keys()) == set(dists2.keys())
        #if set(dists1.keys()) != set(dists2.keys()):
        #    print set(dists1.keys())
        #    print set(dists2.keys())
        #    world.show()
        #    print world.total_lambdas
        #    raw_input()
            
        max_dist = max(dists1[i]+dists2[i] for i in dists1)

    else:
        if dists1 == {}:
            assert world.collected_lambdas != world.total_lambdas
            max_dist = 0
            #world.show()
            #print world.total_lambdas
            #raw_input()
        else:
            max_dist = max(dists1.values())
                
    #assert max_dist == salesman_lower_bound_(world, need_exit)            
    return max_dist


if __name__ == '__main__':
    from world import World
    
    world = World.from_file('../data/sample_maps/contest3.map')
    
    world.show()
    
    #print salesman_lower_bound_naive(world)
    print salesman_lower_bound(world)