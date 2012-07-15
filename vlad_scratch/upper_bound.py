
from utils import dist



def upper_bound(state):
    '''
    Upper bound on total score
    
    We can assume that state is preprocessed and not aggressively preprocessed.
    Time passed is not taken into account, to get actual upper_bound,
    use upper_bound(state)-state.time
    '''
    
    collectable_lambdas = state.collected_lambdas+sum(1 for _ in state.enumerate_lambdas())

    # TODO: take trampolines into account in max_dist calculation

    if collectable_lambdas == state.total_lambdas:
            
        if state.collected_lambdas == state.total_lambdas:
            max_dist = dist(state.robot_coords, state.lift_coords)
        else:
            max_dist = 0
            for xy in state.enumerate_lambdas():
                max_dist = max(max_dist, 
                               dist(state.robot_coords, xy)+dist(xy, state.lift_coords))
        return 75*state.total_lambdas-max_dist
    
    else:
        max_dist = 0
        for xy in state.enumerate_lambdas():
            max_dist = max(max_dist, 
                           dist(state.robot_coords, xy))
                    
        return 50*collectable_lambdas-max_dist
    
    
    