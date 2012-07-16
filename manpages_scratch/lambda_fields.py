import logging
from world import World
from heapq import heappush, heappop
from vorber_world import VorberWorld

class LambdaFields:
    # fields: [(int LambdaCoordinate, [int] LambdaField)]
        # list of individual fields produced by each lambda
        # LambdaCoordinate is the 1d coordinate of lambda in the world
        # LambdaField is the list of effects that the field has on each of the cells
        # remember that world[0,0] is the bottom left row :D
    __slots__ = [ 'fields'
                 ,'world' 
    ]
 
    @property
    def brightness(self):
        return 25+len(self.world.data)
 
    def __init__(self, world):
        self.world = world
        fields = []
        for field_source in world.enumerate_lambdas_index():
            fields.append((field_source, self.calculate_field(field_source, world)))
        self.fields = fields
   
    def calculate_field(self, source, world):
        # list of length of world's data filled with large enough number
        field = [10 * len(world.data)] * len(world.data)
        # the lambda ray source
        field[source] = 0
        # very mutable front, emulated with heapq
        front = []
        heappush(front, (0, source))
        #logic for wave distribution
        while front:
            t, x = heappop(front)
            for ix in self.incident_cells(x, world):
                # boundaries
                if not (0 <= ix < len(world.data)):
                    continue 
                # already visited
                if field[ix] <= t:
                    continue
                # another brick in the wall
                if world.data[ix] == '#':
                    continue
                passing_time = self.wave_passing_time(world.data[ix], t)
                field_potential = (passing_time, ix)
                # been there. did better.
                if passing_time < field[ix]:
                    field[ix] = passing_time
                    heappush(front, field_potential)
        return field
    
    # cells that are to be considered incident to the given cell 
    def incident_cells(self, x, world):
        return [ix for ix in [x+1, x-1, x+world.width, x-world.width]]
    
    # speed of lambda waves in the medium
    def wave_passing_time(self, cell, time):
        if cell == '*':
            time+=2
        else:
            time+=1
        return time
    
    def full_superposition(self):
        full_sup = [0] * len(self.world.data)
        for i in range(0, len(self.world.data)):
            for ffs in self.fields:
                full_sup[i] += ffs[1][i]
        return full_sup
    
    def superposition(self, index):
        result = 0
        for ffs in self.fields:
            result += ffs[1][index]
        return result
    
if __name__ == '__main__':
    import pprint
    logging.basicConfig(level=logging.DEBUG)
    #world = World.from_file('../data/maps_manual/the_best.map')
    #world = World.from_file('../data/maps_manual/lambda_wave1.map')
    world = World.from_file('../data/maps_manual/tricky.map')
    vorber_world = VorberWorld.from_file('../data/maps_manual/tricky.map')
    lambda_fields = LambdaFields(world)
    index = 0
    for i in range(0, len(world.data) / world.width):
        print
        for ii in range(0, world.width):
            field_potential = 0
            for ffs in lambda_fields.fields:
                source, potentials = ffs
                field_potential += potentials[index]
            print field_potential,
            index+=1               
    print
    trp = vorber_world.trampolines
    pprint.pprint(trp['A'])
    pprint.pprint(lambda_fields.superposition(34))
    print(lambda_fields.world.width)
    #pprint.pprint(lambda_fields.full_superposition(lambda_fields))
    #pprint.pprint(lambda_fields.fields)
    world.show()