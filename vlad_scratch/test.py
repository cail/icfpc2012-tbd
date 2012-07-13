

from webvalidator import validate
from game import Map, validate as my_validate

    

#def double_validate(map_number, route, graceful=True):
#    my = my_validate(map_number, route)
#    if not graceful or 
#    pass


if __name__ == '__main__':
    args = 1, 'LDRDDULULLDD'
    my = my_validate(*args)
    web = validate(*args)
    
    assert my == web, (my, web)
    
    
    