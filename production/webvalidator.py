import httplib, urllib
import re
from ast import literal_eval
from os import path as os_path

from simple_settings import settings

server = 'undecidable.org.uk';
path = '/~edwin/cgi-bin/weblifter.cgi';
headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

response_cache_file_name = '../data/cached_responses.txt' 

def dump_all_cached_responses():
    prefix = 'online_validator.cached'
    data = []
    for _, k, v in settings.iter_all_db_values():
        if not k.startswith(prefix): continue
        data.append((k, v))
    data.sort()
    with open(response_cache_file_name, 'w') as f:
        for t in data:
            f.write('{!r}\n'.format(t))
    print '{} responses dumped'.format(len(data))

response_cache = None

def get_cached_response(key):
    global response_cache
    if response_cache is None:
        response_cache = {}
        if os_path.exists(response_cache_file_name):
            with open(response_cache_file_name) as f:
                for t in f:
                    k, v = literal_eval(t)
                    response_cache[k] = v
    return response_cache.get(key) 
            
            
def validate(map_name, route, delay_between_requests = 0):
    '''Validate route with official web validator.
    Nonzero delay_between_requests imposes a minimum time between uses.
    
    Return tuple (score, world).
    '''
    key = 'online_validator.cached("%s", "%s")' % (map_name, route)
    
    cached = get_cached_response(key) or settings.get_value(key, '')
    if cached:
        return literal_eval(cached)
    
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

