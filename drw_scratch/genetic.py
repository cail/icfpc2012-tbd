import random
import itertools
import sys

from world import World
import pathfinder

# mutations:
# - add/remove waits between actions
# - add/remove action


# will need primitives for pushing boulders
# (treating a boulder like an empty destination 
# space does nothing more often than not)

# TODO: some kind of caching for paths

class Candidate(object):
    __slots__ = [
        'actions',
        'waits'
    ]
    
    def __init__(self, destinations=None):
        if destinations:
            self.actions = destinations
        else:
            self.actions = []
        self.waits = [0] * len(self.actions)
        
    def mutate_wait(self):
        index = random.randrange(len(self.waits))
        new_value = self.waits[index] + random.choice([+1, -1])
        if new_value < 0: new_value = 1
        self.waits[index] = new_value
    
    def mutate_insert(self, destination):
        index = random.randrange(len(self.actions))
        self.actions.insert(index, destination)
        self.waits.insert(index, 0)
    
    def mutate_remove(self):
        index = random.randrange(len(self.actions))
        self.actions.pop(index)
        self.waits.pop(index)
    
    def copy(self):
        new_instance = Candidate()
        new_instance.actions = self.actions[:]
        new_instance.waits = self.waits[:]
        return new_instance
        
        
def crossover(candidate1, candidate2):
    while True: # quick fix to avoid empty offspring
        index1 = random.randrange(len(candidate1.actions))
        index2 = random.randrange(len(candidate2.actions))
        
        offspring = Candidate()
        offspring.actions = candidate1.actions[:index1] + candidate2.actions[index2:]
        offspring.waits = candidate1.waits[:index1] + candidate2.waits[index2:]
        if len(offspring.actions) > 0:
            return offspring    

class GeneticSolver(object):
    def __init__(self, world):
        self.world = world

    def random_destination(self):
        while True:
            i = random.randrange(len(self.world.data))
            if self.world.data[i] != '#':
                return i
        
    def generate_candidate(self, length=5):
        # TODO: favor actions that take us to landmarks (lambdas, lift, trampolines)
        return Candidate([self.random_destination() for i in xrange(length)])
    
    def mutate(self, candidate):
        r = random.random()
        if r < 0.5 if len(candidate.actions) > 1 else 0.75: # quick fix to avoid empty candidates
            candidate.mutate_insert(self.random_destination())
        elif r > 0.75:
            candidate.mutate_wait()
        else:
            candidate.mutate_remove()
        return candidate

    def fitness(self, candidate):
        world = World(self.world)
        source = world.robot
        for (wait, destination) in itertools.izip(candidate.waits, candidate.actions):
            for i in xrange(wait):
                world, final_score = world.apply_command('W')
                if final_score is not None:
                    return final_score
            path = pathfinder.plot_path(world, destination)
            if path == None:
                return 0
            commands = pathfinder.path_to_commands(path)
            for c in commands:
                world, final_score = world.apply_command(c)
                if final_score is not None:
                    return final_score
        final_score = world.get_score_abort()
        return final_score
    
    def step(self, population):
        scored_candidates = [(self.fitness(candidate), candidate) for candidate in population]
        scored_candidates.sort()
        scored_candidates.reverse()
        
        scores = [fitness for (fitness, candidate) in scored_candidates]
        print 'Fitness: max %d, average %d' % (scores[0], sum(scores)/float(len(scores)))
        
        best = [candidate for (fitness, candidate) in \
                scored_candidates[:int(POPULATION_SIZE * SELECTED_FOR_BREEDING)]]
        
        golden = [candidate.copy() for candidate in best[:3]]
        
        next_generation = []
        while len(next_generation) < POPULATION_SIZE:
            parent1 = random.choice(best)
            parent2 = random.choice(best)
            while parent2 != parent1:
                parent2 = random.choice(best)
            
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2)
            else:
                child = random.choice([parent1, parent2])
            
            for i in xrange(MUTATION_ATTEMPTS):
                if random.random() < MUTATION_RATE:
                    child = self.mutate(child)
            next_generation.append(child)
        
        next_generation.extend(golden)
        return next_generation
    
    def solve(self):
        population = [self.generate_candidate(3) for i in xrange(POPULATION_SIZE)]
        while True:
            population = self.step(population)



POPULATION_SIZE = 300
SELECTED_FOR_BREEDING = 0.2
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.7
MUTATION_ATTEMPTS = 4 # stir things up a bit

if __name__ == '__main__':
    assert(len(sys.argv) == 2)
    map_name = sys.argv[1]
    print map_name
    world = World.from_file('../data/sample_maps/%s.map' % map_name)
    solver = GeneticSolver(world)
    solver.solve()