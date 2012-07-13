import httplib, urllib
import re

server = 'undecidable.org.uk';
path = '/~edwin/cgi-bin/weblifter.cgi';
headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

def validate(map, route, graceful=False):
    '''Validate route with official web validator.
    Graceful imposes a minimum time between uses.
    
    Return tuple (score, map).
    '''
    assert map in xrange(1, 11), "Invalid map number"
    if graceful:
        assert_enough_time_elapsed()
    
    params = urllib.urlencode({'mapfile': 'contest' + str(map), 'route': route})
    conn = httplib.HTTPConnection(server)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    if response.status != 200:
        raise Exception('Server returned "%d %s"' % (response.status, response.reason))
    print parse_response(response.read())
    conn.close()

def parse_response(data):
    match = re.match('.*<pre>(.*)\n</pre>.*Score: (.*?)<br>', data, flags=re.DOTALL)
    if not match:
        raise Exception('Can\'t parse server response')
    map = match.group(1)
    score = int(match.group(2))
    return (score, map)

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
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

