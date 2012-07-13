# after one of us gets banned, this thing should be strategically inserted into the webvalidator

def assert_enough_time_elapsed():
    from simple_settings import settings
    import time
    LAST_ACCESS_TIME_KEY = 'online_validator.last_access_time'
    MIN_TIME_BETWEEN_ACCESSES = 60.0 # 1 minute, living on the edge!
    
    current_time = time.time()
    last_access_time = float(settings.get_value(LAST_ACCESS_TIME_KEY, 0.0))
    wait_interval = MIN_TIME_BETWEEN_ACCESSES - (current_time - last_access_time) 
    assert wait_interval <= 0, "Wait %f more seconds" % wait_interval
    settings[LAST_ACCESS_TIME_KEY] = current_time
    
assert_enough_time_elapsed()
