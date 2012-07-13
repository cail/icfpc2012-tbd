import httplib, urllib
import re

server = 'undecidable.org.uk';
path = '/~edwin/cgi-bin/weblifter.cgi';
headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

def validate(map, route):
    '''Validate route with official web validator.
    
    Return tuple (score, map).
    '''
    assert(map in xrange(1, 11))
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()