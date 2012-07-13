from game import Map
import sys

def main(argv):
	if len(argv) != 2:
		print 'USAGE:'
		print argv[0],'level'
		exit()

	m = Map.load(argv[1])
	while not m.done:
		m.show()
		c = raw_input('>')
		print 'res:', m.execute(c)
	m.show()

if __name__ == '__main__':
	main(sys.argv)
