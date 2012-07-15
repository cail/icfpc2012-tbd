import world_definitions as objects

import random
import os

official_worlds_folder = '../../data/sample_maps'
our_custom_world_folder = '../../data/maps_manual'

print_generated_maps = False

def create_chaotic(height, width, properties):
    assert width*height >= 2
    result = ''
    has_robot = False
    has_lift = False
    last = width*height
    for i in range(1,height+1):
        for j in range(1,width+1):
            if (not has_robot and ((random.randint(0, last-1) == 0) 
                    or (i*width+j == last))):
                result += objects.Robot
                has_robot = True
            else:
                if (not has_lift and ((random.randint(0, last-1) == 0) 
                        or (i*width+j == last-1))):
                    result += objects.Lift
                    has_lift = True
                else:
                    result += random.choice(objects.Fields[2:-1])
        result += '\n'
    if ('flooding' in properties and ( (random.random() < properties['flooding']))):
        result += '\nWaterproof %d\n' % random.randint(0, height)
        result += 'Flooding %d\n' % random.randint(0, height)
        result += 'Water %d\n' % random.randint(0, height)
    assert has_robot
    return result

def create_balanced(height, width, properties):
    world = [ [ 0 for _ in range(width) ] for _ in range(height) ]
    def put_obj(obj):
        while True:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if world[y][x] == 0:
                break
        world[y][x] = obj
    put_obj(objects.Robot)
    put_obj(objects.Lift)
    lambda_count = int(height*width*properties['lambdas'])
    for _ in range(lambda_count):
        put_obj(objects.Lambda)
    stone_count = int(height*width*properties['stones'])
    for _ in range(stone_count):
        put_obj(objects.Stone)
    wall_count = int(height*width*properties['walls'])
    for _ in range(wall_count):
        put_obj(objects.Wall)
    earth_to_empty = properties['earth_to_empty']
    for y in range(height):
        for x in range(width):
            if world[y][x] == 0:
                if random.random() > earth_to_empty:
                    world[y][x] = objects.Empty
                else:
                    world[y][x] = objects.Earth
    result = '\n'.join([ ''.join(world_line) for world_line in world ])
    return result

def create_maze(height, width, rooms):
    # stub
    
    return ''

random_generator_table = {
    'chaotic' : create_chaotic, 
    'balanced' : create_balanced,
    'maze' : create_maze
}

random_counter = 0 # utility, to differentiated generated maps by numbers

def create_one_random(height, width, properties):       
    global random_counter

    try:
        mode = properties['mode']
        generator = random_generator_table[mode]
    except KeyError:
        return {
            'name' : 'malformed.%d' % random_counter,
            'source' : '',
        }    
    
    random_counter += 1
    world = generator(height, width, properties)
    
    if print_generated_maps:
        print 'random.%s.%d' % (mode, random_counter)
        print world
        print '____'
        
    return {
        'name' : 'random.%s.%d' % (mode, random_counter),
        'source' : world,
        'width' : width,
        'height' : height
    }

def create_some_random(amount, height, width):
    return [
            create_one_random(height, width, {'mode' : 'chaotic'}) 
            for _ in range(amount) 
    ]

def load_from_folder(path):
    files = os.listdir(path)
    results = [
        {
        'name' : file_path,
        'source' : open("%s/%s" % (path, file_path), "r").read(),
        } for file_path in files 
    ]
    for result in results:
        s = result['source'].split()
        result['height'] = len(s)
        result['width'] = len(s[0])
    return results


def load_official_worlds():
    return load_from_folder(official_worlds_folder)

def load_official_basic_worlds():
    return [ world for world in load_from_folder(official_worlds_folder)
            if world['name'].startswith('contest') ]
    
def load_official_flood_worlds():
    return [ world for world in load_from_folder(official_worlds_folder)
            if world['name'].startswith('flood') ]    
    
def load_official_portal_worlds():
    return [ world for world in load_from_folder(official_worlds_folder)
            if world['name'].startswith('trampoline') ]    

def load_our_worlds():
    return [ world for world in load_from_folder(our_custom_world_folder)
            if world['name'].endswith('.map') ]
    
if __name__ == '__main__':
    assert(create_some_random(0, 0, 0) == [])
    assert(len(create_some_random(3, 2, 2)) == 3)
    world = create_one_random(4, 6, {'mode' :'chaotic'})
    assert(len(world['source']) == 4*(6+1))
    assert(world['width'] == 6)
    assert(create_one_random(4,6,{})['source'] == '')
    world = create_one_random(50, 50, {
        'mode' : 'balanced',
        'lambdas' : 0.05,
        'stones' : 0.4,
        'walls' : 0.0,
        'earth_to_empty' : 1 
    })
    print world['source']
    world = create_one_random(15, 15, {'mode' :'maze'})
    print world['source']
