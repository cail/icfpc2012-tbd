import sys
import random


def create_map(width, height):
    
    def rand_coords():
        return random.randrange(width), random.randrange(height)
    
    data = {}
    
    for x in range(width):
        for y in range(height):
            data[x, y] = random.choice(' .'*50+r'#*\\@W!ABCDEFGHI')
     
    unique = 'RL123456789'
    for c in unique:
        while True:
            xy = rand_coords()
            if data[xy] not in unique:
                data[xy] = c
                break
    #data[rand_coords()] = 'R'
   # 
    #while True:
    #    c = rand_coords()
    #    if data[c] != 'R':
    #        data[c] = 'L'
    #        break
    
    #print data
    result = ''
    
    for y in range(height):
        for x in range(width):
            result += data[x, y]
        result += '\n'
    result += \
"""
Growth {}
Razors {}
Water {}
Flooding {}
Waterproof {}
Trampoline A targets 1
Trampoline B targets 2
Trampoline C targets 3
Trampoline D targets 4
Trampoline E targets 5
Trampoline F targets 6
Trampoline G targets 7
Trampoline H targets 8
Trampoline I targets 9""".format(random.randrange(5, 200), 
                                 random.randrange(3),
                                 random.randrange(5),
                                 random.randrange(10),
                                 random.randrange(5, 10))
    return result
    
    
if __name__ == '__main__':
    random.seed(666)
    for i in range(20):
        with open('../data/stress/shit{}.map'.format(i), 'w') as fout:
            m = create_map(30+10*i, 30+10*i)
            #print m
            print>>fout, m