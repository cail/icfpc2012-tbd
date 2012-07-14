from reachability_tests import reachability_tests


def reachability_step(width, data):
    i = data.index('R')
    reachable = set([i])
    return data



def parse_test(s):
    lines = s.split('\n')
    assert lines[0] == ''
    del lines[0]
    assert all(len(lines[0]) == len(line) for line in lines)
    width = len(lines[0])
    data = sum(map(list, lines), [])
    return width, data

def data_to_string(width, data):
    lines = []
    for i in range(0, len(data), width):
        lines.append(''.join(data[i:i+width]))
    return '\n'.join(lines)

   
def test_processing_step(tests, step):
    for test, result in tests:
        print '-'*10
        print test
        width, data = parse_test(test)
        assert test == '\n'+data_to_string(width, data)
        
        
        reachable = step(width, data)
        
        print data_to_string(width, reachable)
        
        _, expected = parse_test(result)
        
        if expected != reachable:
            print 'fail, expected'
            print data_to_string(width, expected)
            
            
    
if __name__ == '__main__':
    test_processing_step(reachability_tests, reachability_step)
