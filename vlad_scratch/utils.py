


def path_to_nearest_lambda(world):
    '''
    return path to nearest lambda or None
    '''
    
    dds = [('L', -1), ('R', +1), ('U', -world.width), ('D', +world.width)]
    
    data = world.data
    visited = {world.robot: (-1, '*')}
    tasks = set([world.robot])
    
    while tasks:
        new_tasks = set()
        for i in tasks:
            for dir, delta in dds:
                j = i+delta
                if data[j] in ' .' and j not in visited:
                    visited[j] = i, dir
                    new_tasks.add(j)
                    
                if data[j] == '\\':
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
    
    
    
    
    