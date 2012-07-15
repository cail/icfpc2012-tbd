import warnings


def dist((x1, y1), (x2, y2)):
    return abs(x1-x2)+abs(y1-y2)



def path_to_nearest_lambda_or_exit(world):
    '''
    return path to nearest lambda or None
    '''
    
    dds = [('L', -1), ('R', +1), ('U', -world.width), ('D', +world.width)]
    
    data = world.data
    visited = {world.robot: (-1, '*')}
    tasks = set([world.robot])
    
    if world.collected_lambdas == world.total_lambdas:
        if 'O' not in world.data:
            warnings.warn('path to nearest lambda or exit: O not in data!')
        goal = 'O'
    else:
        goal = '\\'
    
    while tasks:
        new_tasks = set()
        for i in tasks:
            for dir, delta in dds:
                j = i+delta
                if data[j] in ' .!' and j not in visited:
                    visited[j] = i, dir
                    new_tasks.add(j)
                    
                if data[j] == goal:
                    path = [dir]
                    while i != -1:
                        i, dir = visited[i]
                        path.append(dir)
                    path = ''.join(path)[::-1]
                    assert path.startswith('*')
                    return path[1:]
                    
        tasks = new_tasks
                    
                
if __name__ == '__main__':
    from world import World
    
    world = World.from_file('../data/sample_maps/contest5.map')
    
    world.show()
    
    print path_to_nearest_lambda(world)
    
    
    
    
    