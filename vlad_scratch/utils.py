import warnings


def dist((x1, y1), (x2, y2)):
    return abs(x1-x2)+abs(y1-y2)


def enumerate_paths_to_goals(world, start, walkable, goal):
    '''
    yield paths as strings
    
    start and goal cells does not have to be in walkable
    '''
    
    #TODO: teleporters!
    
    dds = [('L', -1), ('R', +1), ('U', -world.width), ('D', +world.width)]
    
    data = world.data
    visited = {start: (-1, '*')}
    tasks = set([start])
    
    while tasks:
        new_tasks = set()
        for i in tasks:
            for dir, delta in dds:
                j = i+delta
                if data[j] in walkable and j not in visited:
                    visited[j] = i, dir
                    new_tasks.add(j)
                    
                if data[j] == goal:
                    path = [dir]
                    k = i
                    while k != -1:
                        k, dir = visited[k]
                        path.append(dir)
                    path = ''.join(path)[::-1]
                    assert path.startswith('*')
                    yield path[1:]
                    
        tasks = new_tasks



def path_to_nearest_lambda_or_lift(world):
    '''
    return path to nearest lambda (lift if all lambdas are collected) or None
    '''
    
    if world.collected_lambdas == world.total_lambdas:
        if 'O' not in world.data:
            warnings.warn('path to nearest lambda or exit: O not in data!')
        goal = 'O'
    else:
        goal = '\\'
    
    return next(enumerate_paths_to_goals(world, start=world.robot, walkable=' .!', goal=goal),
                None)
    
                
if __name__ == '__main__':
    from world import World
    
    world = World.from_file('../data/sample_maps/contest5.map')
    
    world.show()
    
    print path_to_nearest_lambda_or_lift(world)
    
    
    
    
    