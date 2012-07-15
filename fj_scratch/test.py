
import sys

from webvalidator import validate

score, map = validate('contest1', 'LDRDDULULLDDL')
print score, '\n', map 
sys.exit()


    
#m = Map.load('test.map')
#while not m.done:
#    m.show()
#    c = raw_input('>')
#    print 'res:', m.execute(c.upper())
#m.show()

