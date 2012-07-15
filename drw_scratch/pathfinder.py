import itertools

def commands_to_reach(world, destination):
    path = plot_path(world, destination)
    if path is None:
        return None
    return path_to_commands(path)

def plot_path(world, destination):
    ''' Find a path to destination in world.
        Walls and boulders are impassable. '''
    start = world.robot
    closedset = set()
    openset = set([start])
    came_from = {}
    
    g_score = {}
    f_score = {}
    g_score[start] = 0
    f_score[start] = g_score[start] + distance(world, start, destination)
    
    while openset:
        score, current = argmin(lambda point: f_score[point], openset)
        if current == destination:
            return reconstruct_path(came_from, destination)
        openset.remove(current)
        closedset.add(current)
        
        for neighbor in neighbors(world, current):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in openset or tentative_g_score < g_score[neighbor]: 
                openset.add(neighbor)
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + distance(world, neighbor, destination)
    return None # not reachable

def neighbors(world, i):
    coords_to_index = lambda (x,y): len(world.data)-(y+2)*world.width+x+1

    x, y = world.index_to_coords(i)
    
    result = [coords_to_index(coords) for coords in [(x+1, y), (x-1,y), (x,y+1), (x,y-1)]]
    result = [j for j in result if world.data[j] not in ['#', '*']]
    return result 

def distance(world, i, j):
    x1, y1 = world.index_to_coords(i)
    x2, y2 = world.index_to_coords(j)
    return abs(x2-x1) + abs(y2-y1)

def reconstruct_path(came_from, destination):
    path = [destination]
    last_node = destination
    while last_node in came_from:
        last_node = came_from[last_node]
        path.append(last_node)
    path.reverse()
    return path

def path_to_commands(path):
    commands = []
    point = path[0]
    for next_point in path[1:]:
        if next_point == point + 1:
            commands.append('R')
        elif next_point == point - 1:
            commands.append('L')
        elif next_point > point:
            commands.append('D')
        else:
            commands.append('U')
        point = next_point
    return commands

argmin = lambda funct, items: min(itertools.izip(itertools.imap(funct, items), items))