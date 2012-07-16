import sys, time
import world
from test_emulators import validate, validate_custom, run_interactively, time_execution_print
from test_emulators import world_classes, official_map_file_name
from test_emulators import World, VorberWorld, DictWorld#, WorldFast

#validate('contest8', 'RRRRRRRULD', [VorberWorld, World])
#print 'yo'
#sys.exit()

world10_commands = '''
UUUUUUUULLUULLLUUUUUUUUUUULLLLLLLLLLLLRRRRRRRRRRRRDDDDDDDDDDDRRRDDRRDDDDDDDDUUUUUUUULLUULLLUUUUUURRRRRUA
UUUULLLLULLLLLLLDLLLUULLUUUUUUUUUULLLLLLLULUURRRRRRRDDDRRRRRRRDRRRRRDDDDDRRRDDRRDDDDDA
UUUUUUUULLLLLLLLLLLLLUULUUULLLLLLLLLUULLRDDDDDLLDDDDRRRDDRRRD
UUUUUUUULLUULLLUUUUUUUUUUULLLLLLLLLLLRRRRRRDDDDDDRRRRDDDDDDDDDRRRDDRRDDLLLLDDLLLLLLLLLLLUULLLLLLLLLA
ULLLLLDLLLLLLLLLLLULRDRRRRRRRRRRRUURRLLDDLLUUULLLLLLA
UUUUUUUULLUULLLUUUUUUUUUDDDDDDDDDDDLDDRRDDRRRDDLLLA
UUUUUUUULLLLLLLLLLLLLUULUUULLLLLLLLLUULLLURRRRRRRRRRRUUUURRRRRRDDA
UUUUUUUULLUULLLUULLLLLLLDDLLLLLLLLDD
ULLLLLDLLLLLLLLLLLUUUULLLRUUUUUURRRRRRURRURRDDUUURRURRRRRRA
UUUUUUUULLUULLLUUUUULLLLLUURRRUDLLLDDRRRRRDDDDDRRRDDRRDDDDDUUUUULLUULLLUUUUULLLLLULLLLLLLUUUULLULLLLDA
UUUUUUUULLLLLLLLLLLLLUULLLLLLDDDDUUUUUUURUUUUUA
UUUUUUUULLUULLLUUUUUUUUUULLLLLLLLLDDDDDDDDDDDDLLDDRRDDDUUULLUUA
UUUUUUUULLUULLRRDDRRDDDUUULLUULLLUUUUULLLLLULLLLLLA
A
ULLLLLDLLUUULLLLLLLUUULLUUURRUUUUUUULLLLLLLLLULUUA
UUUUULLLLLLLLLLDDDDUUUUURUULLLLLA
UUUUUUUULLLLLLLLLLLLLUULUUULLLLLLLLLUULLLRRRDDRRRRRRRDDDDDDDRRRRRRRRRRRRRRRDA
ULLDUULLLRRRRRDDDA
UUUUUUUULLUULLLUUUUUUUUUUURRLLLLLLLLLLLLLLDDDDDDDDDDDDDDDDDDDDDUUUUUUUUUUUUUUUUUUULLLLA
UULLLLLDDLLLLLLLLLLLUUUULLLLLLLUULLLUUUURUURUUUUUUUURA
'''.split()

test_suite = [
            ('contest6', 'RUULRRRRRRRRRRUUULLLLLLLDLLLUUUUUURULURR'),
            ('contest8', 'RRRRRRRULD'),
            ]
test_suite.extend(('contest10', cmd) for cmd in world10_commands)

t_start = time.time()
#time_execution_print(World, test_suite, chunk_size = 100)
#time_execution_print(World, test_suite, chunk_size = 100)


#time_execution_print(WorldFast, test_suite, chunk_size = 1)
#time_execution_print(WorldFast, test_suite, chunk_size = 1)

#time_execution_print(DictWorld, test_suite, chunk_size = 1)
#time_execution_print(DictWorld, test_suite, chunk_size = 1)
#time_execution_print(VorberWorld, test_suite, chunk_size = 1)
#time_execution_print(VorberWorld, test_suite, chunk_size = 1)


#world_classes.remove(VorberWorld)
#validate_custom('../data/maps_manual/push2.map', 'LLWDDLWDWDWDDLLUURLRRUUUUUULLLLLLLLRRRRRRRRRRR'
#                , world_classes)

#map_name = 'flood1'
#path = run_interactively(VorberWorld.from_file(official_map_file_name(map_name)))

path = run_interactively(World.from_file(official_map_file_name('horock1')))
validate('horock1', path, [World, VorberWorld])

print 'yo {:0.1f}'.format(world.application_counter / (time.time() - t_start))