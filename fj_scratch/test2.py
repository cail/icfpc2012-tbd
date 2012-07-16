from genetic import GeneticSolver
import world as world_module
from world import World
import time

t_start = time.time()
timeout = 30
map_path = '../data/sample_maps/contest10.map'
world = World.from_file(map_path)
solver = GeneticSolver(world)
print solver.solve(timeout)

print 'yo {:0.1f}'.format(world_module.application_counter / (time.time() - t_start))