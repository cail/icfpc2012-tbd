import httplib, urllib
import re

from simple_settings import settings

server = 'undecidable.org.uk';
path = '/~edwin/cgi-bin/weblifter.cgi';
headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

def validate(map_name, route, delay_between_requests = 0):
    '''Validate route with official web validator.
    Nonzero delay_between_requests imposes a minimum time between uses.
    
    Return tuple (score, world).
    '''
    key = 'online_validator.cached("%s", "%s")' % (map_name, route)
    
    cached = settings.get_value(key, '')
    if cached != '':
        return eval(cached)
    
    if delay_between_requests:
        wait_until_enough_time_elapsed(delay_between_requests)
    
    params = urllib.urlencode({'mapfile': map_name, 'route': route})
    conn = httplib.HTTPConnection(server)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    if response.status != 200:
        raise Exception('Server returned "%d %s"' % (response.status, response.reason))
    result = parse_response(response.read())
    conn.close()
    
    settings[key] = repr(result)
    
    return result


def parse_response(data):
    match = re.match('.*<pre>(.*)\n</pre>.*Score: (.*?)<br>', data, flags=re.DOTALL)
    if not match:
        raise Exception('Can\'t parse server response')
    world = match.group(1)
    score = int(match.group(2))
    return (score, world)

def wait_until_enough_time_elapsed(min_time_between_accesses):
    import time
    LAST_ACCESS_TIME_KEY = 'online_validator.last_access_time'
    last_access_time = float(settings.get_value(LAST_ACCESS_TIME_KEY, 0.0))
    wait_interval = min_time_between_accesses - (time.time() - last_access_time) 
    if wait_interval > 0:
        print 'Waiting %f seconds before before submitting request' % wait_interval
        time.sleep(wait_interval)
    settings[LAST_ACCESS_TIME_KEY] = time.time()
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

