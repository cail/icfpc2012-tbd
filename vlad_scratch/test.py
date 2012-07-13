

from webvalidator import validate
from game import Map, play, validate as my_validate

    

#def double_validate(map_number, route, graceful=True):
#    my = my_validate(map_number, route)
#    if not graceful or 
#    pass


if __name__ == '__main__':
    
    args = 'flood1', 'LLLLDDDDDWWWWUWWW'
    my = my_validate(*args)
    
    print 'my:'
    print my[0]
    print my[1]
    print '---'
    
    #exit()
    
    web = validate(*args)
    print 'theirs:'
    print web[0]
    print web[1]
    assert my == web, (my, web)
    
    
    