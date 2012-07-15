from world import World
from test_emulators import validate, validate_custom, world_classes, run_interactively, official_map_file_name

#validate_custom('../data/maps_manual/evade.map', 'DLDWRWDRUWDWWRUWDLRWLLWDULWUWDLRDUDDLRWRUUDD'
#                , world_classes)

map_name = 'contest8'
path = run_interactively(World.from_file(official_map_file_name(map_name)))
validate(map_name, path, world_classes)

print 'yo'