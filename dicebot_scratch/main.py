'''
Main tester script.
Provide several functions to solve a list of maps on list of algorithms and
    get some useful metrics to compare.

Check __main__ for examples, including commented out

All test runs provide results in following data-structure (json'ed output):
{
    "<map name>": {
        "meta": {
            "width": 0, 
            "height": 0
        }, 
        "stats_per_solver": {
            "<solver name>": {
                "solution_length": 0, 
                "score": null, 
                "solution": "", 
                "time": "0.000000"
            }
        }
    }
}
'''
import worlds
import emulator
import solvers

import random
import time
import json
from itertools import chain

# SETTINGS

# For now one of three:
#    emulator.interpret_main - latest one
#    emulator.interpret_dict - original Vlad's one
#    emulator.interpret - dual one
default_interpreter = emulator.interpret

# check solver.py for available ones
solver_list = [ solvers.fuzz_solver(), solvers.vlad_solver() ]

# used in random-based map generators 
worlds.print_generated_maps = True

# END OF SETTINGS

# utility function to run any one test and store needed metrics
def run_test(world_text, solver, interpretator):
    time1 = time.time()
    commands = solver.solve(world_text)
    time_taken = time.time() - time1
    score = interpretator(world_text, commands)
    
    return { 
            'score' : score,
            'time' : '{:f}'.format(time_taken),
            'solution_length' : len(commands),
            'solution' : commands
            }

def test_world_list(worlds):
    results = { }
    for world in worlds:
        results[world['name']] = {
            'meta' : {
                'width' : world['width'],
                'height' : world['height'],
#                commented out until really required, to omuch garbage in stdout
#                'source' : world['source']
            },
            'stats_per_solver' : { solver.name : 
                run_test(world['source'], solver, default_interpreter) for solver in solver_list 
            }
        }
    return results

def test_fuzzy(count, min_width = 5, max_width = 1000, min_height = 5, max_height = 1000, with_water = False):
    properties = {'mode' : 'chaotic'}
    if with_water:
        properties['flooding'] = 1 # portions of maps with water
    return test_world_list([ 
        worlds.create_one_random(random.randint(min_height, max_height),
                                 random.randint(min_width, max_width),
                                 properties
                                )
        for _ in range(count) 
    ])
    
def test_all_official():
    return test_world_list(worlds.load_official_worlds())
    
def test_basic_official():
    return test_world_list(worlds.load_official_basic_worlds())
    
def test_all():
    return test_world_list(chain( 
       worlds.create_some_random(amount = 3, height = 4, width = 5),
       worlds.load_official_worlds(),
       worlds.load_our_worlds()
    ))
    
if __name__ == '__main__':
    random.seed(42)
    #stats = test_fuzzy(2, max_width = 20, max_height = 30, with_water = True)
    stats = test_fuzzy(1, max_width = 5, max_height = 5, with_water = False)
    #stats = test_all_official()
    #stats = test_basic_official()
    print json.dumps(stats, indent=4, sort_keys = False)