import itertools
import heapq

def commands_to_reach(world, destination, simple=False):
    if simple:
        return simple_solution(world, destination)
    else:
        path = plot_path(world, destination)
        commands = path_to_commands(path)
        return commands

def simple_solution(world, destination):
    source_coords = world.robot_coords
    destination_coords = world.index_to_coords(destination)
    dx = destination_coords[0] - source_coords[0]
    dy = destination_coords[1] - source_coords[1]
    result = ''
    # since we face the problem of flooding
    # it might be beneficial to always do
    # vertical movement first
    if dy >= 0:
        result += 'U' * dy
    else:
        result += 'D' * (-dy)
    if dx >= 0:
        result += 'R' * dx
    else:
        result += 'L' * (-dx)
    return result

def plot_path(world, destination):
    ''' Find a path to destination in world.
        Walls and boulders are impassable. '''
    start = world.robot
    
    g_score = {}
    f_score = {}
    g_score[start] = 0
    f_score[start] = g_score[start] + distance(world, start, destination)

    closedset = set()
    openset_heap = [(f_score[start], start)]
    openset = set([start])
    came_from = {}

    while openset:
        score, current = heapq.heappop(openset_heap)
        if score > f_score[current]:
            continue
        if current == destination:
            return reconstruct_path(came_from, destination)
        
        openset.remove(current)
        closedset.add(current)
        
        for neighbor in neighbors(world, current):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + 1

            if (neighbor not in openset) or tentative_g_score < g_score[neighbor]: 
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + distance(world, neighbor, destination)
                heapq.heappush(openset_heap, (f_score[neighbor], neighbor))
                openset.add(neighbor)
    return None # not reachable

def neighbors(world, i):
    result = [j for j in [i+1, i-1, i+world.width, i-world.width] if 0 <= j < len(world.data)]
    return [j for j in result if world.data[j] not in ['#', '@', '*']]

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
    if path is None:
        return 'A'
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

