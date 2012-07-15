from test_emulators import validate, validate_custom, world_classes, run_interactively, official_map_file_name
from test_emulators import World, VorberWorld, DictWorld

#from test_emulators import validate, validate_custom, world_classes

world_classes.remove(VorberWorld)
validate_custom('../data/maps_manual/push2.map', 'LLWDDLWDWDWDDLLUURLRRUUUUUULLLLLLLLRRRRRRRRRRR'
                , world_classes)

#map_name = 'flood1'
#path = run_interactively(VorberWorld.from_file(official_map_file_name(map_name)))

#path = run_interactively(DictWorld.from_file('../data/maps_manual/push2.map'), 'LLWDDLWDWDWDDL')

print 'yo'