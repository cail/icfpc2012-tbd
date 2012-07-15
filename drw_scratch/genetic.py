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
        
    def insert(self, index, destination):
        self.genes.insert(index, ('move', destination))
    
    def remove(self, index):
        self.genes.pop(index)

    def copy(self):
        new_instance = Candidate()
        new_instance.genes = self.genes[:]
        return new_instance
    
    def __len__(self):
        return len(self.genes)
        
        
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
        landmark_symbols = ['\\', 'L'] + map(chr, range(ord('A'), ord('A')+9))
        self.landmarks = [i for i, c in enumerate(world.data) if c in landmark_symbols]
        
        self.cache = {}
        self.mutations_generator = WeightedRandomGenerator(*zip(*MUTATIONS))

    def random_destination(self, near=None):
        while True:
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
        if mutation == 'insert':
            if random.random() < SHORT_MOVE_CHANCE:
                # TODO: FIX
                last_destination = candidate.genes[index - 1][1] \
                    if index > 0 else self.world.robot  
                candidate.insert(index, self.random_destination(near=last_destination))
            else:
                candidate.insert(index, self.random_destination())
        elif mutation == 'wait':
            pass
#            new_value = candidate.waits[index] + random.choice([+1, -1])
#            if new_value < 0: new_value = 1
#            candidate.waits[index] = new_value
        elif mutation == 'remove':
            candidate.remove(index)
        else:
            assert False, 'Mutation not implemented: %s' % mutation
        return candidate

    def fitness(self, candidate):
        world = World(self.world)
        world_hash = world.get_hash()
        for gene in candidate.genes:
            gene_type, gene_value = gene
            destination = gene_value
#            if wait > 0:
#                world = world.apply_commands('W' for _ in xrange(wait))
#                if world.terminated:
#                    break
#                world_hash = world.get_hash()
            cache_key = (world_hash, world.robot, destination)
            cached = (cache_key in self.cache)
            if cached:
                commands, world_hash = self.cache[cache_key]
                world = world.apply_commands(commands)
            else:
                commands = pathfinder.commands_to_reach(world, destination)
                world = world.apply_commands(commands)
                world_hash = world.get_hash()
                self.cache[cache_key] = (commands, world_hash)
            if world.terminated:
                break
        return world.score
    
    def compile(self, candidate):
        world = World(self.world)
        compiled = []
        for (wait, destination) in itertools.izip(candidate.waits, candidate.actions):
            for _ in xrange(wait):
                compiled.append('W')
                world = world.apply_command('W')
                if world.terminated:
                    return ''.join(compiled)
            commands = pathfinder.commands_to_reach(world, destination)
            for c in commands:
                compiled.append(c)
                world = world.apply_command(c)
                if world.terminated:
                    return ''.join(compiled)
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
#        print 'Fitness: max %d, average %d' % (scores[0], sum(scores)/float(len(scores)))
        
        num_best = int(POPULATION_SIZE * SELECTED_FOR_BREEDING)
        best = candidates[:num_best]
        best_scores = scores[:num_best]
        min_score = min(best_scores)
        if min_score < 0:
            weights = [score - min_score for score in best_scores]
        else:
            weights = best_scores
        random_candidate = WeightedRandomGenerator(candidates, weights)
        elite = [candidate.copy() for candidate in candidates[:NUM_ELITE]]
        leader = candidates[0].copy()
        
        next_generation = []
        while len(next_generation) < POPULATION_SIZE:
            parent1 = random_candidate.next()
            parent2 = random_candidate.next()
#            parent1 = random.choice(best)
#            parent2 = random.choice(best)
            while parent2 != parent1:
#                parent2 = random.choice(best)
                parent2 = random_candidate.next()

            
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
    
    def solve(self, timeout, local_timeout=10):
        start_time = time.time()
        timed_out = False
        best_leader, best_leader_score = None, None
        while not timed_out:
            population = [self.generate_candidate(3) for _ in xrange(POPULATION_SIZE)]
            last_improvement_time = start_time
            previous_iteration_score = None
            for i in itertools.count():
                (population, leader) = self.step(population)
                leader_score = self.fitness(leader)
                if (previous_iteration_score is None) or (leader_score > previous_iteration_score):
                    last_improvement_time = time.time()
                previous_iteration_score = leader_score 
                print "Iteration %d: %d" % (i, leader_score)
                if time.time() - start_time > timeout:
                    timed_out = True
                    break
                if time.time() - last_improvement_time > local_timeout:
                    break
            if (best_leader is None) or (leader_score > best_leader_score):
                print "New global best: %d" % leader_score
                best_leader = leader
                best_leader_score = leader_score
        return self.compile(best_leader)


POPULATION_SIZE = 300
SELECTED_FOR_BREEDING = 0.1
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.7
MUTATION_ATTEMPTS = 4 # stir things up a bit
LANDMARK_GENE_CHANCE = 0.3 # generates genes that makes us go to interesting places
NUM_ELITE = 3 # top N candidates are copied to the new generation unchanged 
MUTATIONS = [('insert', 2), ('wait', 2), ('remove', 2), ('fuzz', 0)] # weighted mutations
SHORT_MOVE_DISTANCE = 3
SHORT_MOVE_CHANCE = 0.3

if __name__ == '__main__':
    timeout = 20
    assert(len(sys.argv) >= 2)
    map_path = sys.argv[1]
    if len(sys.argv) > 2:
        timeout = int(sys.argv[2])
    print map_path
    world = World.from_file(map_path)
    solver = GeneticSolver(world)
    print solver.solve(timeout)