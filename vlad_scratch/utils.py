import warnings
from itertools import chain

from world import World


def dist((x1, y1), (x2, y2)):
    return abs(x1-x2)+abs(y1-y2)


def enumerate_paths_to_goals(world, start, walkable, goals):
    '''
    yield (goal_index, paths) as strings
    
    start and goal cells does not have to be in walkable
    '''
    
    #TODO: teleporters!
    
    dds = [('L', -1), ('R', +1), ('U', -world.width), ('D', +world.width)]
    
    data = world.data
    visited = {start: (-1, '*')}
    tasks = set([start])
    yielded = set()
    
    while tasks:
        new_tasks = set()
        for i in tasks:
            for dir, delta in dds:
                j = i+delta
                if data[j] in walkable and j not in visited:
                    visited[j] = i, dir
                    new_tasks.add(j)
                    
                if data[j] in goals and j not in yielded:
                    yielded.add(j)
                    path = [dir]
                    k = i
                    while k != -1:
                        k, dir = visited[k]
                        path.append(dir)
                    path = ''.join(path)[::-1]
                    assert path.startswith('*')
                    yield j, path[1:]
                    
        tasks = new_tasks



def path_to_nearest_lambda_or_lift(world):
    '''
    return pair (idx, path) to nearest lambda (lift if all lambdas are collected) or None
    '''
    
    if world.collected_lambdas == world.total_lambdas:
        if 'O' not in world.data:
            warnings.warn('path to nearest lambda or exit: O not in data!')
        goal = 'O'
    else:
        goal = '\\'
    
    result= next(enumerate_paths_to_goals(world, start=world.robot, walkable=' .!\\', goals=goal),
                 None)
    return result
    

def interesting_actions(world):
    '''
    receive preprocessed world
    
    return a few number of significantly varying actions
    '''

    world = World(world)

    data = world.data
    width = world.width
        
    if data[world.robot-width] in '*@' and data[world.robot+width] not in 'O':
        data[world.robot+width] = '#'
        # never go down when under a rock!
    
    actions = []
    
    t = path_to_nearest_lambda_or_lift(world)
    if t is not None:
        idx, path = t
        actions.append((9, idx, path))
        
    
    eatable = ' .!\\'
    
    for i in range(world.width, len(data)):
        if data[i-width] in '*@' and data[i] in eatable:
            data[i] = '_'
        if data[i] in '*@':
            right = data[i-1] in eatable and data[i+1] == ' '
            left = data[i+1] in eatable and data[i-1] == ' '
            if right:
                data[i-1] = '>'
            if left:
                data[i+1] = '<'
        
    #world.show()
        
    walkable = ' .!\\<>_'
    
    interesting = '_<>\\ABCDEFGHI'
    for idx, path in enumerate_paths_to_goals(world, world.robot, walkable, interesting):
        priority = 0
        if data[idx] in 'ABCDEFGHI':
            priority = 1
        if data[idx] == '>':
            if data[idx+1] == '@':
                priority = 4
            path += 'R'
        if data[idx] == '<':
            if data[idx-1] == '@':
                priority = 4
            path += 'L'
        if data[idx] == '_' and data[idx-width] == '@':
            priority = 8
        if not actions or actions[0][2] != path:
            actions.append((priority, idx, path))

    #for a in actions:
    #    print a, data[a[1]]
        
    interesting = []
    if actions != []:
        a = max(actions)
        interesting.append(a)
        actions.remove(a)
        
        for _ in range(3):
            if actions == []:
                break
            def dist_to_others(a):
                _, idx, _ = a
                xy = world.index_to_coords(idx)
                return min(dist(xy, world.index_to_coords(i[1])) for i in interesting)
            a = max(actions, key=dist_to_others)
            interesting.append(a)
            actions.remove(a)

    #print '---'
    #for a in interesting:
    #    print a, data[a[1]], world.index_to_coords(a[1])
        
    return [a[2] for a in interesting]
  
                
if __name__ == '__main__':

    from preprocessor import preprocess_world
    
    #world = World.from_file('../data/sample_maps/trampoline3.map')
    
    world = World.from_file('../data/maps_manual/horo2.map')
    
    world.show()
    
    #print path_to_nearest_lambda_or_lift(world)
    
    print interesting_actions(preprocess_world(world))
    
    
    
    
    