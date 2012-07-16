import random
import itertools
import sys
import time
import bisect

from world import World
import pathfinder

# mutations:
# - add/remove waits between actions
# - add/remove action

# will need primitives for pushing boulders
# (treating a boulder like an empty destination 
# space does nothing more often than not)


class Candidate(object):
    __slots__ = [
        'genes',
    ]
    
    def __init__(self, destinations=None):
        if destinations:
            self.genes = [('move', destination) for destination in destinations]
        else:
            self.genes = []
        
    def insert(self, index, gene):
        self.genes.insert(index, gene)
    
    def remove(self, index):
        self.genes.pop(index)

    def copy(self):
        new_instance = Candidate()
        new_instance.genes = self.genes[:]
        return new_instance
    
    def __len__(self):
        return len(self.genes)
        
class TimeOut(Exception):
    pass

def crossover(candidate1, candidate2):
    while True: # quick fix to avoid empty offspring
        index1 = random.randrange(len(candidate1))
        index2 = random.randrange(len(candidate2))
        
        offspring = Candidate()
        offspring.genes = candidate1.genes[:index1] + candidate2.genes[index2:]
        if len(offspring) > 0:
            return offspring    

class WeightedRandomGenerator(object):
    def __init__(self, elements, weights):
        self.elements = elements 
        self.totals = []
        running_total = 0

        for w in weights:
            running_total += w
            self.totals.append(running_total)

    def next(self):
        rnd = random.random() * self.totals[-1]
        return self.elements[bisect.bisect_right(self.totals, rnd)]

    def __call__(self):
        return self.next()

class GeneticSolver(object):
    def __init__(self, world):
        self.world = world
        landmark_symbols = ['\\', 'L', '!', '@'] + map(chr, range(ord('A'), ord('A')+9))
        self.landmarks = [i for i, c in enumerate(world.data) if c in landmark_symbols]
        
        self.cache = {}
        self.mutations_generator = WeightedRandomGenerator(*zip(*MUTATIONS))
        
        self.best, self.best_score = None, None

    def random_destination(self, near=None):
        while True:
            if time.time() > self.deadline:
                raise TimeOut
            if near is None:
                if random.random() < LANDMARK_GENE_CHANCE:
                    i = random.choice(self.landmarks)
                else:
                    i = random.randrange(len(self.world.data))
            else:
                # Warning: this could conceivably go into infinite loop
                i = random.randrange(len(self.world.data))
                if pathfinder.distance(self.world, i, near) > SHORT_MOVE_DISTANCE:
                    continue
            if self.world.data[i] != '#':
                return i
        
    def generate_candidate(self, length=5):
        return Candidate([self.random_destination() for _ in xrange(length)])
    
    def mutate(self, candidate):
        mutation = self.mutations_generator.next()
        if len(candidate) == 1:
            while mutation == 'remove':
                mutation = self.mutations_generator.next()
                
        index = random.randrange(len(candidate))
        if mutation == 'insert_short_move':
            last_destination = None
            for i in xrange(index - 1, -1, -1):
                if candidate.genes[i][0] == 'move':
                    last_destination = candidate.genes[i][1]
                    break
            if last_destination == None:
                last_destination = self.world.robot
            gene = ('move', self.random_destination(near=last_destination))
            candidate.insert(index, gene)
        elif mutation == 'insert_long_move':
            gene = ('move', self.random_destination())
            candidate.insert(index, gene)
        elif mutation == 'insert_wait':
            candidate.insert(index, ('wait', None))
        elif mutation == 'remove':
            candidate.remove(index)
        else:
            assert False, 'Mutation not implemented: %s' % mutation
        return candidate

    def fitness(self, candidate):
        world = World(self.world)
        world_hash = world.get_hash()
        for gene in candidate.genes:
            if time.time() > self.deadline:
                raise TimeOut
            gene_type, gene_value = gene
            if gene_type == 'wait':
                world = world.apply_command('W')
                if world.terminated:
                    break
                world_hash = world.get_hash()
            elif gene_type == 'move':
                destination = gene_value
                cache_key = (world_hash, world.robot, destination)
                cached = (cache_key in self.cache)
                if cached:
                    commands, world_hash = self.cache[cache_key]
                else:
                    commands = pathfinder.commands_to_reach(world, destination)

                #world = world.apply_commands(commands)

                for c in commands:
                    direction = [-world.width, world.width, -1, 1, 0]['UDLRA'.index(c)]
                    if world.data[world.robot + direction] == 'W' and world.razors > 0:
                        world = world.apply_command('S')
                        if world.terminated: break
                    world = world.apply_command(c)
                    if world.terminated: break

                if not cached:
                    world_hash = world.get_hash()
                    self.cache[cache_key] = (commands, world_hash)
                if world.terminated: break
            else:
                assert False, "Unrecognized gene: %s" % gene_type
        return world.score
    
    def compile(self, candidate):
        world = World(self.world)
        compiled = []
        for gene in candidate.genes:
            gene_type, gene_value = gene
            if gene_type == 'wait':
                world = world.apply_command('W')
                compiled.append('W')
                if world.terminated: break
            elif gene_type == 'move':
                destination = gene_value
                commands = pathfinder.commands_to_reach(world, destination)
                for c in commands:
                    direction = [-world.width, world.width, -1, 1, 0]['UDLRA'.index(c)]
                    if world.data[world.robot + direction] == 'W' and world.razors > 0:
                        world = world.apply_command('S')
                        compiled.append('S')
                        if world.terminated: break
                    world = world.apply_command(c)
                    compiled.append(c)
                    if world.terminated: break
            else:
                assert False, "Unrecognized gene: %s" % gene_type
            if world.terminated:
                break

        if not world.terminated:
            compiled.append('A')
        return ''.join(compiled)
    
    def evaluate_and_sort(self, population):
        scored_candidates = [(self.fitness(candidate), candidate) for candidate in population]
        scored_candidates.sort(reverse=True)
        scores = [score for (score, candidate) in scored_candidates]
        candidates = [candidate for (score, candidate) in scored_candidates]
        return (scores, candidates)
    
    def step(self, population):
        scores, candidates = self.evaluate_and_sort(population)
        num_best = int(POPULATION_SIZE * SELECTED_FOR_BREEDING)
        best = candidates[:num_best]
        elite = [candidate.copy() for candidate in candidates[:NUM_ELITE]]
        leader = candidates[0].copy()
        
        next_generation = []
        while len(next_generation) < POPULATION_SIZE:
            parent1 = random.choice(best)
            parent2 = random.choice(best)
            while parent2 != parent1:
                parent2 = random.choice(best)
            
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2)
            else:
                child = parent1.copy()
                for _ in xrange(MUTATION_ATTEMPTS):
                    if random.random() < MUTATION_RATE:
                        child = self.mutate(child)
            next_generation.append(child)
        
        next_generation.extend(elite)
        return (next_generation, leader)
    
    def solve(self, running_time=150, convergence_time=10, verbose=False):
        ''' Make multiple attempts at solving the map, returning the best solution.
        
            The function will run for running_time seconds. Population is discarded
            if no improvement has been observed for convergence_time seconds. '''
        start_time = time.time()
        timed_out = False
        
        self.best, self.best_score = 'A', None
        
        self.deadline = start_time + running_time
                
        try:
            while True:
                population = [self.generate_candidate(INITIAL_LENGTH) \
                              for _ in xrange(POPULATION_SIZE)]
                last_improvement_time = time.time()
                last_improvement_iteration = 0
                
                previous_iteration_score = None
                
                for i in itertools.count():
                    (population, leader) = self.step(population)
                    leader_score = self.fitness(leader)
                    if (previous_iteration_score is None) or \
                        (leader_score > previous_iteration_score):
                        last_improvement_time = time.time()
                        last_improvement_iteration = i
                    previous_iteration_score = leader_score 
                    if verbose:
                        print "Iteration %d: %d" % (i, leader_score)
                    if convergence_time > 0 and \
                        (time.time() - last_improvement_time > convergence_time):
                        break
                    if i - last_improvement_iteration > 100:
                        break
                    if (self.best_score is None) or (leader_score > self.best_score):
                        if verbose:
                            print "New global best: %d" % leader_score
                        self.best = self.compile(leader)
                        self.best_score = leader_score
        except TimeOut:
            pass
        return self.best

    def get_best(self):
        if self.best_score == None:
            return (0, 'A')
        else:
            #return (self.best_score, self.compile(self.best))
            return (self.best_score, self.best)

INITIAL_LENGTH = 3
POPULATION_SIZE = 300
SELECTED_FOR_BREEDING = 0.1
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.7
MUTATION_ATTEMPTS = 10 # stir things up a bit
LANDMARK_GENE_CHANCE = 0.3 # generates genes that makes us go to interesting places
NUM_ELITE = 3 # top N candidates are copied to the new generation unchanged 
MUTATIONS = [('insert_long_move', 10), ('insert_short_move', 10),\
              ('insert_wait', 5), ('remove', 20),] # weighted mutations
SHORT_MOVE_DISTANCE = 3

def solve(world, running_time):
    solver = GeneticSolver(world)
    return solver.solve(running_time=running_time)
    

if __name__ == '__main__':
    running_time = 20
    assert(len(sys.argv) >= 2)
    map_path = sys.argv[1]
    arguments = {}
    if len(sys.argv) > 2:
        arguments['running_time'] = int(sys.argv[2])
    if len(sys.argv) > 3:
        arguments['convergence_time'] = int(sys.argv[3])
        
    world = World.from_file(map_path)
    solver = GeneticSolver(world)
    print solver.solve(verbose=True, **arguments)