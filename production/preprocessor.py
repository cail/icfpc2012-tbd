from world import World
from mask_errors import failsafe


def reachability_step(width, data):
    '''
    Overapproximate set of spaces where robot can possibly be
    '''
    
    reachable = [False]*len(data)
    tasks = set([data.index('R')])
    
    auto_empty = [False]*len(data)
    # cells that can become empty even without robot intervention
    for i in reversed(range(len(data)-width)):
        cell = data[i]
        if cell == ' ':
            auto_empty[i] = True
        elif cell in '*@':
            if auto_empty[i+width]:
                # fall down
                auto_empty[i] = True
            elif data[i+width] in '^*@' and\
                 auto_empty[i+width-1] and data[i-1] in ' *@':
                # fall left
                auto_empty[i] = True
            elif data[i+width] in '^*@\\' and\
                 auto_empty[i+width+1] and data[i+1] in ' *@':
                # fall right
                auto_empty[i] = True
                
    neighbors = [+1, -1, -width-1, -width, -width+1, +width]
    
    portals = '123456789ABCDEFGHI'
    
    while tasks:
        i = tasks.pop()
        assert not reachable[i]
     
        r = False
        
        cell = data[i]
        if cell == 'R':
            r = True
        elif auto_empty[i] or cell in ' .!\\W':
            if reachable[i-1] or reachable[i+1] or\
               reachable[i+width] or reachable[i-width]:
                r = True
        elif cell in portals:
            # TODO: less conservative portals reachability
            r = True
            reachable[i] = True
            for j in range(len(data)):
                if data[j] in portals:
                    if not reachable[j]:
                        tasks.add(j)
        elif cell in '*@':
            if reachable[i+width]:
                # dig under
                r = True
            elif reachable[i-1] and (reachable[i+1] or auto_empty[i+1]):
                # push right
                r = True
            elif reachable[i+1] and (reachable[i-1] or auto_empty[i-1]):
                # push left
                r = True
            elif data[i+width] in '*@^\\' and\
                 (reachable[i+1] or auto_empty[i+1]) and\
                 (reachable[i+width+1] or auto_empty[i+width+1]):
                # fall right
                r = True
            elif data[i+width] in '*@^' and\
                 (reachable[i-1] or auto_empty[i-1]) and\
                 (reachable[i+width-1] or auto_empty[i+width-1]):
                # fall left
                r = True
                
        if r:
            reachable[i] = True
            for delta in neighbors:
                if not reachable[i+delta]:
                    tasks.add(i+delta)
            
    return reachable


def stone_reachability_step_(width, data):
    '''
    Overapproximate set of places where can possibly be a stone
    '''
    
    result = [False]*len(data)
    
    def make_reachable(i):
        if data[i] not in '#^LO':
            result[i] = True
    
    for i in range(width, len(data)-width, width):
        for j in range(i, i+width):
            #if data[j] == '*':
            if data[j] in '*@' or result[j-width]: # this is ridiculously imprecise, but otherwise it's incorrect
                make_reachable(j-1)
                make_reachable(j)
                make_reachable(j+1)
            if result[j-width]:
                make_reachable(j)
        
        # push to the right            
        for j in range(i, i+width):
            if result[j] and\
               data[j+width] not in 'R ':
                make_reachable(j+1)
        
        #push to the left            
        for j in reversed(range(i, i+width)):
            if result[j] and\
               data[j+width] not in 'R ':
                make_reachable(j-1)
                
    return result


def stone_reachability_step(width, data):
    '''
    Overapproximate set of places where can possibly be a stone
    '''
    
    r = [False]*len(data)
    
    for i in range(width, len(data)-width, width):
        for j in range(i, i+width):
            cell = data[j]
            if cell in '*@':
                r[j] = True
                if data[j-1] == 'R' and data[j+1] == ' ':
                    r[j+1] = True
                if data[j+1] == 'R' and data[j-1] == ' ':
                    r[j-1] = True
            if cell not in '#^LO' and \
               (r[j-width-1] or r[j-width] or r[j-width+1]):
                r[j] = True
            
        # push to the right
        for j in range(i, i+width):
            if r[j] and not r[j+1] and \
               data[j-1] not in '#^' and \
               data[j+width] not in 'R ' and data[j+1] not in '#^LO':
                r[j+1] = True
                
        # push to the left
        for j in range(i+width-1, i-1, -1):
            if r[j] and not r[j-1] and \
               data[j+1] not in '#^' and \
               data[j+width] not in 'R ' and data[j-1] not in '#^LO':
                r[j-1] = True
    
    return r


def preprocess_world(world):
    result = preprocess_world_(world)
    if result is not None:
        return result
    return world

@failsafe(default=None)
def preprocess_world_(world):
    '''
    return simplified version of the world
    
    THEOREM. Set of optimal solutions does not change.
    
    (actually, it's a lie, but the only counterexample 
    we can think of is pretty contrived, so...)
    '''    
    
    world = world.__class__(world)
    
    width = world.width
    data = world.data
    
    reachable = reachability_step(width, data)
    
    for i in range(width, len(data)):
        if not reachable[i]:
            cell = data[i]
            if cell in '*@':
                data[i] = '^'
            elif cell not in 'LO':
                data[i] = '#'

    lift = world.lift
    if not (reachable[lift-1] or
            reachable[lift+1] or
            reachable[lift-width] or
            reachable[lift+width]):
        world.total_lambdas = -1e10
        # so now it's impossible to collect all lambdas
        # (because collected_lambdas can't be equal total_lambdas)
         
    stone_reachable = stone_reachability_step(width, data)
    for i in range(width, len(data)):
        cell = data[i]
        if cell == '.':
            if not stone_reachable[i-width] and not stone_reachable[i]:
                data[i] = ' '
        elif cell == '^':
            if not stone_reachable[i-width]:
                data[i] = '#'
        
    return world