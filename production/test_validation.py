from time import sleep

from game import validate as local_validate
from webvalidator import validate


def main():
    tests = [
        ('contest1', 'LDRDDULULLDD'), # complete solution
        ('contest8', 'WWWRRRLLLWWWA'), # abort or death?
        
        # write your own tests, especially for interesting cases
        ]
    
    for i, test in enumerate(tests):
        if i > 0:
            sleep(60)
        print '{}% {}'.format(100*(i+1)//len(tests), test),
        local = local_validate(*test)
        web = validate(*test)
        if local == web:
            print 'ok'
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