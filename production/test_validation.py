from time import sleep

from game import validate as local_validate
from webvalidator import validate


def main():
    tests = [
             
        ('flood1', 'LLLLDDDDDWWWWUUUWWWWWW'), # surface barely in time
        ('flood1', 'LLLLDDDDDWWWWWWWWWWWW'), # drowning
        ('flood1', 'W'*100), # passive drowning
             
        ('contest1', 'LDRDDULULLDD'), # complete solution
        ('contest8', 'WWWRRRLLLWWWA'), # abort or death?
        ('contest2', 'RRUDRRULURULLLLDDDL'), # OPTIMAL solution
        
        # write your own tests, especially for interesting cases
        ]
    
    for i, test in enumerate(tests):
        if i > 0:
            sleep(1) # no need to sleep too much because we cache anyway
            
        print '{}% {}'.format(100*(i+1)//len(tests), test),
        local = local_validate(*test)
        web = validate(*test)
        if local == web:
            print 'ok (score {})'.format(local[0])
        else:
            print 'FAIL !!!!!!!'
            print 'local:'
            print local[0]
            print local[1]
            print 'theirs:'
            print web[0]
            print web[1]


if __name__ == '__main__':
    main()