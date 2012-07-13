import generator
import emulator
import solvers

import time

def test_all():
    results = { }
    count = 1
    for world in generator.generate_some_random( 3, 5, 5 ):
        for solver in solvers.enumerate_all():
            time1 = time.time()
            commands = solver.solve(world)
            time_taken = time.time() - time1
            score = emulator.interpret(world, commands)
            name = 'random.%s' % count
            results[name] = { }
            results[name][solver.name] = { 'score' : score, 'time' : time_taken };      
        count += 1  
    return results
    
def print_metrics(metrics):    
    i = 1
    for world_name,world_metric in metrics.iteritems():
        print 'World', world_name, ':'
        for solver_name, solver_metric in world_metric.iteritems():
            print '\tSolver ', solver_name
            print '\t\t score = ', solver_metric['score']
            if solver_metric['time'] < 1.0:
                print '\t\t time < 1.0'
            else:
                print '\t\t time = {:f}'.format(solver_metric['time'])
            print ''
        i += 1
            
if __name__ == '__main__':
    print_metrics( test_all() )
