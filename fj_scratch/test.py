from test_emulators import validate, validate_custom, world_classes, run_interactively, official_map_file_name
from test_emulators import World, VorberWorld, DictWorld

#validate_custom('../data/maps_manual/evade.map', 'DLDWRWDRUWDWWRUWDLRWLLWDULWUWDLRDUDDLRWRUUDD'
#                , world_classes)

map_name = 'flood1'
path = run_interactively(DictWorld.from_file(official_map_file_name(map_name)))
validate(map_name, path, world_classes)
print 'yo'