from simple_settings import settings

# simple example
print settings['login name']


# more complicated example

import time

LAST_ACCESS_TIME_KEY = 'online_validator.last_access_time'
MIN_TIME_BETWEEN_ACCESSES = 5 * 60 # 5 minutes, I like to live on the edge.

current_time = time.time()
last_access_time = float(settings.get_value(LAST_ACCESS_TIME_KEY, 0.0))
wait_interval = MIN_TIME_BETWEEN_ACCESSES - (current_time - last_access_time) 
assert wait_interval <= 0, "Wait %f more seconds" % wait_interval
settings[LAST_ACCESS_TIME_KEY] = current_time
print 'accessing!'
