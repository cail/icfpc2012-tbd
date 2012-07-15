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
from itertools import chain
from worlds import load_official_basic_worlds,\
    load_official_flood_worlds, load_our_worlds

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
    try:
        score = interpretator(world['source'], commands)
    except:        
        print 'Commands: ', commands
        print 'Map: '
        print '_____'
        print world['source']
        print '-----'
        score = None
    
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
    
def test_all_random():
    properties = {'mode' : 'chaotic', 'flooding' : 'true' }
    
    count_fuzzy = 10
    max_height_fuzzy = 50
    max_width_fuzzy = 50
    
    fuzzy = [ 
        worlds.create_one_random(random.randint(5, max_height_fuzzy),
                                 random.randint(5, max_width_fuzzy),
                                 properties
                                )
        for _ in range(count_fuzzy) 
    ]
    
    properties = {
        'mode' : 'balanced',
        'lambdas' : 0.05,
        'stones' : 0.3,
        'walls' : 0.0,
        'earth_to_empty' : 1.0 
    }
    
    count_balanced = 3
    height_balanced = 300
    width_balanced = 300
    
    balanced1 = [ 
        worlds.create_one_random(height_balanced,
                                 width_balanced,
                                 properties
                                )
        for _ in range(count_balanced) 
    ]
    
    return test_world_list(chain(
        fuzzy, balanced1
    ))
        
def test_all_official():
    return test_world_list(worlds.load_official_worlds())
    
def test_basic_official():
    return test_world_list(worlds.load_official_basic_worlds())

def test_flood_official():
    return test_world_list(worlds.load_official_flood_worlds())
    
def test_our_worlds():
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
    for world_name, world_stats in stats:
        print '{:20}'.format(world_name),
        for solver_name in solver_names:
            print '{:10}'.format(world_stats['stats_per_solver'][solver_name]['score']),
        print                    
        
    
if __name__ == '__main__':
    import sys
    seed = random.randint(0, sys.maxint)
    print 'Using seed', seed 
    random.seed(seed)
    
    random_stats = test_all_random()
    predef_stats = test_world_list(chain(
        load_official_basic_worlds(),
        load_official_flood_worlds(),
        load_our_worlds()
    )) 

    print_as_table(random_stats.items())
    print_as_table(predef_stats.items())    

    # uncomment to print detailed data including solutions
    
    import json
    open("random_stats.json", "w").write(json.dumps(random_stats, indent=4, sort_keys = False))
    open("predef_stats.json", "w").write(json.dumps(predef_stats, indent=4, sort_keys = False))