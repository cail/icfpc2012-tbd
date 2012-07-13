from world_definitions import Fields, Robot

import random

def generate_one_random(m, n, properties):
    result = '';
    mode = ''
    try:
        mode = properties['mode']
    except KeyError:
        pass
    if mode  == 'chaotic':
        has_robot = False
        for i in range(m):
            for j in range(n):
                if (not has_robot and ((random.randint(0, m*n-1) == 1) 
                        or (i*j == (m-1)*(n-1)))):
                    result += Robot
                    has_robot = True
                else:
                    result += random.choice(Fields[1:-1])
            result += '\n'
        result += '\n'
    return result

def generate_some_random(amount, m, n):
    return [ generate_one_random(m, n, {'mode' : 'chaotic'}) for i in range(amount) ]

def load_from_folder(path):
    pass

if __name__ == '__main__':
    assert(generate_some_random(0, 0, 0) == [])
    assert(len(generate_some_random(3, 1, 1)) == 3)
    assert(len(generate_one_random(4, 6, {'mode' :'chaotic'})) == 4*(6+1)+1)
    assert(generate_one_random(4,6,{}) == '')
