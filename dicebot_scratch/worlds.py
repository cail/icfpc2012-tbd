from world_definitions import Fields, Robot, Lift

import random
import os

random_counter = 0

def create_chaotic(height, width, properties):
    result = ''
    has_robot = False
    has_lift = False
    last = width*height
    for i in range(1,height+1):
        for j in range(1,width+1):
            if (not has_robot and ((random.randint(0, last-1) == 1) 
                    or (i*width+j == last))):
                result += Robot
                has_robot = True
            else:
                if (not has_lift and ((random.randint(0, last-1) == 1) 
                        or (i*width+j == last-1))):
                    result += Lift
                    has_lift = True
                else:
                    result += random.choice(Fields[2:-1])
        result += '\n'
    return result

random_generator_table = {
    'chaotic' : create_chaotic, 
}

def create_one_random(height, width, properties):       
    global random_counter

    try:
        mode = properties['mode']
        generator = random_generator_table[mode]
    except KeyError:
        return 'malformed.%d' % random_counter, ''    
    
    random_counter += 1
    return 'random.%s.%d' % (mode, random_counter), generator(height, width, properties)

def create_some_random(amount, height, width):
    return [ create_one_random(height, width, {'mode' : 'chaotic'}) for _ in range(amount) ]

def load_from_folder(path):
    files = os.listdir(path)
    return [ (file_path, open("%s/%s" % (path, file_path), "r").read()) for file_path in files ] 

official_worlds_folder = '../data/sample_maps'
our_custom_world_folder = '../data/maps_manual'

def load_official_worlds():
    return load_from_folder(official_worlds_folder)

def load_our_worlds():
    return load_from_folder(our_custom_world_folder)

if __name__ == '__main__':
    assert(create_some_random(0, 0, 0) == [])
    assert(len(create_some_random(3, 1, 1)) == 3)
    assert(len(create_one_random(4, 6, {'mode' :'chaotic'})[1]) == 4*(6+1)+1)
    assert(create_one_random(4,6,{})[1] == '')
