

from dual_world import DualWorld
from localvalidator import validate as local_validate
from webvalidator import validate

    

#def double_validate(map_number, route, graceful=True):
#    my = my_validate(map_number, route)
#    if not graceful or 
#    pass


if __name__ == '__main__':
    
    args = 'contest1', 'LLLLDDDDDWWWWUWWW'
    my = local_validate(DualWorld, *args)
    
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
    print "they are the same"
    
    
    