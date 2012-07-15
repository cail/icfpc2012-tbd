import logging
from world import World
from heapq import heappush, heappop

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
        # very functional way of getting incident vertices 
        incidental_cells = lambda x: [ix for ix in [x+1, x-1, x+world.width, x-world.width]]
        
        #logic for wave distribution
        while front:
            t, x = heappop(front)
            for ix in incidental_cells(x):
                # boundaries
                if not (0 <= ix < len(world.data)):
                    continue 
                # already visited
                if field[ix] <= t:
                    continue
                # another brick in the wall
                if world.data[ix] == '#':
                    continue
                passing_time = self.cell_wave_passing_time(world.data[ix], t)
                field_potential = (passing_time, ix)
                # been there. did better.
                if passing_time < field[ix]:
                    field[ix] = passing_time
                    heappush(front, field_potential)
        return field
    
    def cell_wave_passing_time(self, cell, time):
        if cell == '*':
            time+=2
        else:
            time+=1
        return time
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    #world = World.from_file('../data/maps_manual/the_best.map')
    world = World.from_file('../data/maps_manual/lambda_wave1.map')
    lambda_fields = LambdaFields(world)
    world.show()