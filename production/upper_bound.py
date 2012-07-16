
from mask_errors import failsafe
from utils import dist
from salesman import salesman_lower_bound



@failsafe(default=10**10)
def upper_bound(state):
    '''
    Upper bound on total score
    
    We can assume that state is preprocessed and not aggressively preprocessed.
    Time passed is not taken into account, to get actual upper_bound,
    use upper_bound(state)-state.time
    '''
    
    collectable_lambdas = state.collected_lambdas+state.data.count('\\')+state.data.count('@')

    # TODO: take trampolines into account in max_dist calculation

    if collectable_lambdas == state.total_lambdas:
        max_dist = salesman_lower_bound(state, need_exit=True)
        return 75*state.total_lambdas-max_dist
    else:
        if state.total_lambdas < 0: # special negative value set by preprocessor:
            max_dist = 0
        else:
            max_dist = salesman_lower_bound(state, need_exit=False)
                    
        return 50*collectable_lambdas-max_dist
    
    
    