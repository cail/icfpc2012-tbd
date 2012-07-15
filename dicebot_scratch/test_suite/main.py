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
solver_list = [ solvers.fuzz_solver(), solvers.vlad_solver(),
                solvers.drw_solver(), solvers.predefined_solver() ]

# used in random-based map generators 
worlds.print_generated_maps = True

# END OF SETTINGS

# utility function to run any one test and store needed metrics
def run_test(world, solver, interpretator):
    time1 = time.time()
    commands = solver.solve(world['source'], world['name'])
    time_taken = time.time() - time1
    score = interpretator(world['source'], commands)
    
    return { 
            'score' : score,
            'time' : '{:f}'.format(time_taken),
            'solution_length' : len(commands) if commands else None,
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
                run_test(world, solver, default_interpreter) for solver in solver_list 
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

def test_flood_official():
    return test_world_list(worlds.load_official_flood_worlds())
    
def test_out_worlds():
    return test_world_list(worlds.load_our_worlds())    
    
    
'''
Pretty visualizer

            solver1   solver2
    
map1        score     score
map2        score     score

'''
def print_as_table(stats):
    solver_names = [ solver.name for solver in solver_list ]
    print '{:20}'.format(''),
    for solver_name in solver_names:
        print '{:>10}'.format(solver_name),
    print      
    for world_name, world_stats in stats.items():
        print '{:20}'.format(world_name),
        for solver_name in solver_names:
            print '{:10}'.format(world_stats['stats_per_solver'][solver_name]['score']),
        print                    
        
    
if __name__ == '__main__':
    import sys
    seed = random.randint(0, sys.maxint)
    print 'Using seed', seed 
    random.seed(seed)    
    stats = chain( 
        test_fuzzy(2, max_width = 20, max_height = 30, with_water = True),
        test_basic_official(),
        test_flood_official(),
        test_out_worlds()
    )
    print_as_table(stats)
    #print json.dumps(stats, indent=4, sort_keys = False)