import sys, subprocess, time, signal

def run(what, infile, limit):
	proc = subprocess.Popen(what, stdin=infile, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	secs_passed = 0
	while secs_passed < limit:
		if not proc.poll():
			secs_passed += 1
			time.sleep(1)
		else:
			break
	if proc.poll():
		print 'finished OK'
	else:
		print 'not finished, sending SIGINT'
		proc.send_signal(signal.SIGINT)
		time.sleep(10)
		if proc.poll():
			print 'finished after SIGINT'
		else:
			print 'not finished after SIGINT, sending SIGKILL'
			proc.send_signal(signal.SIGKILL)
			print 'FAIL'
			sys.exit()
	print 'getting output'
	stdout, stderr = proc.communicate()
	if len(stderr) != 0:
		print 'warning: stderr not empty'
		print 'contents of stderr:'
		print stderr
		print '---'
	for i, ch in enumerate(stdout):
		if ch not in 'ULDRAW':
			print 'warning:', i+1,'th character in stdout is not in ULDRAW'
	print 'contents of stdout:'
	print stdout

def main(argv):
	run(('python', './manager.py'), open('../data/sample_maps/contest1.map'), 10)


if __name__ == '__main__':
	main(sys.argv)
