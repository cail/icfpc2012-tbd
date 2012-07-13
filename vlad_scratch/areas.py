'''
Area is a dict (x, y) -> char

Walls are not represented (so use area.get((x, y), '#') instead of area[x, y])

Area can have portals (character 'P')
'''


def filter_walls(area):
    return {k: v for k, v in area.items() if v != '#'}


def bounding_box(area):
    '''Return (min_x, min_y, max_x, max_y)
    
    As usual, max is not inclusive
    '''
    xs = [x for x, _ in area]
    ys = [y for _, y in area]
    
    return (min(xs), min(ys), max(xs)+1, max(ys)+1)


def area_to_string(area):
    x1, y1, x2, y2 = bounding_box(area)
    
    lines = []
    for y in reversed(range(y1, y2)):
        lines.append(''.join(area.get((x, y), '#') for x in range(x1, x2)))
        
    return '\n'.join(lines)


if __name__ == '__main__':
    area = {(1, 1): ' ', (2, 3): '*'}
    print bounding_box(area)
    print area_to_string(area)