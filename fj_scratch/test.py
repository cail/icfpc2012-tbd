from test_emulators import validate, validate_custom, world_classes, run_interactively, official_map_file_name
from test_emulators import World, VorberWorld, DictWorld

#validate_custom('../data/maps_manual/evade.map', 'DLDWRWDRUWDWWRUWDLRWLLWDULWUWDLRDUDDLRWRUUDD'
#                , world_classes)

map_name = 'flood1'
path = run_interactively(VorberWorld.from_file(official_map_file_name(map_name)))

print 'yo'