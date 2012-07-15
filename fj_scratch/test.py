import sys
from test_emulators import validate, validate_custom, run_interactively, time_execution_print
from test_emulators import world_classes, official_map_file_name
from test_emulators import World, VorberWorld, DictWorld

validate('contest8', 'RRRRRRRULD', [VorberWorld, World])

print 'yo'

sys.exit()

test_suite = [
#            ('contest6', 'RUULRRRRRRRRRRUUULLLLLLLDLLLUUUUUURULURR'),
            ('contest8', 'RRRRRRRULD'),
            
            ]
time_execution_print(World, test_suite)
time_execution_print(World, test_suite)
time_execution_print(DictWorld, test_suite)
time_execution_print(DictWorld, test_suite)
time_execution_print(VorberWorld, test_suite)
time_execution_print(VorberWorld, test_suite)

#from test_emulators import validate, validate_custom, world_classes

#world_classes.remove(VorberWorld)
#validate_custom('../data/maps_manual/push2.map', 'LLWDDLWDWDWDDLLUURLRRUUUUUULLLLLLLLRRRRRRRRRRR'
#                , world_classes)

#map_name = 'flood1'
#path = run_interactively(VorberWorld.from_file(official_map_file_name(map_name)))

#path = run_interactively(DictWorld.from_file('../data/maps_manual/push2.map'), 'LLWDDLWDWDWDDL')

print 'yo'