import datetime
from collections import defaultdict

# we use numbers in [1, numHosts + 1] to identify each host in the code
numHosts = 0
numSwitches = 0

# timestamp_number-of-hosts_number-of-switches
outputFilePrefix = f"logs/{str(datetime.datetime.now()).replace(' ', '-')}" + \
					f"_{str(numHosts)}_{str(numSwitches)}"

# targets and pairs are for the testing file bookkeeping
targets = set()
pairs = set()

# topology file bookkeeping
links = set()

# testing file bookkeeping
lk = defaultdict(int)

# will output code to test connection between hosts h{x+1} and host h{y+1}
# will setup an iperf3 server at host h{y+1}
def addPairToTest(clientHostNum: int, serverHostNum: int):
	assert 1 <= clientHostNum <= numHosts + 1
	assert 1 <= serverHostNum <= numHosts + 1
	assert clientHostNum != serverHostNum
	pair = (clientHostNum, serverHostNum)
	assert pair not in pairs, "duplicate pair"
	targets.add(serverHostNum)
	pairs.add(pair)

	lk[serverHostNum] += 1

def getCommands():
	res = []
	
	assert len(targets) > 0
	assert len(pairs) > 0
	
	res.append("# start iperf servers")
	for t in targets:
		res.append(f"print('starting {lk[t]} iperf server(s) @ {t}')")
		for i in range(1, lk[t] + 1):
			res.append(f"h{t}.cmd('iperf3 -s -p {5100 + i}&')")
	res.append("")

	res.append("# wait for servers to start")
	res.append("print('wait for servers to start')")
	res.append("time.sleep(2)")
	res.append("")

	res.append("# run iperf clients")
	res.append("print('run iperf clients')")
	for c, s in pairs:
		# res.append(f"h{c} iperf3 -c h{s} -u -l 1000 -t 15 -i 1")
		res.append(f"print('launching {c} -> {s} iperf')")
		# res.append(f"h{c}.cmd('nohup iperf3 -c 10.0.0.{s} -u -l 10000 -t 15 -p {5100 + lk[s]} -i 1 > {outputFilePrefix}_{c}_{s}.txt 2>&1 &')")
		res.append(f"h{c}.cmd('nohup iperf3 -c 10.0.0.{s} -u -b 1M -t 15 -p {5100 + lk[s]} -i 1 > {outputFilePrefix}_{c}_{s}.txt 2>&1 &')")
		# cmd = f"h{c}.cmd('nohup ( (date > {outputFilePrefix}_{c}_{s}.txt) " + \
		# "&& " + \
		# f"(iperf3 -c 10.0.0.{s} -u -b 20M -t 15 -p {5100 + lk[s]} -i 1 >> {outputFilePrefix}_{c}_{s}.txt) " + \
		# "&& " + \
		# f"(date >> {outputFilePrefix}_{c}_{s}.txt)) 2>&1 &')"
		# res.append(cmd)
		lk[s] -= 1
	res.append("")

	assert all(x == 0 for x in lk.values()), list(lk.values())
	
	res.append("# wait for iperf clients to finish")
	res.append("print('wait for iperf clients to finish')")
	res.append("time.sleep(30)")
	res.append("")

	res.append("# Kill iperf servers")
	res.append("print('Kill iperf servers')")
	for t in targets:
		res.append(f"h{t}.cmd('killall iperf3')")
	res.append("")

	return res

def getTestFile():
	assert numHosts > 0
	assert numSwitches > 0
	hostLineLhs = ", ".join(["h"+str(i) for i in range(1, numHosts + 1)])
	hostLineRhs = ", ".join(["'h"+str(i)+"'" for i in range(1, numHosts + 1)])

	fileStart = [
		"def run_tests(net):",
		"	from datetime import datetime",
		"	# Create logs directory if it doesn't exist",
		"	if not os.path.exists('logs'):",
		"		os.makedirs('logs')",
		"",
		"	# Get current timestamp for log files",
		"	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')",
		"",
		"",	
		"	# Get host objects",
		f"	{hostLineLhs} = net.get({hostLineRhs})",
		"",
		"	try:"
	]


	fileEnd = [
		"	except Exception as e:",
		"		print(e)"
	]

	indentLevel = 2

	res = []
	commands = getCommands()
	for line in fileStart:
		res.append(f"{line}\n")
	for line in commands:
		res.append(f"{'	' * indentLevel}{line}\n")
	for line in fileEnd:
		res.append(f"{line}\n")
	return res

def replace_test_section(
	lines, new_content, 
	start_marker, end_marker, 
	output_file
):
	# start_marker = "# START build"
	# end_marker = "# END build"
		
	# Find the start and end indices
	start_idx = -1
	end_idx = -1
		
	for i, line in enumerate(lines):
		if start_marker in line:
			start_idx = i
		elif end_marker in line:
			end_idx = i
			break
		
	if start_idx == -1 or end_idx == -1:
		raise ValueError("Could not find START and END markers for run_tests section")
		
	# Create new content list
	new_lines = lines[:start_idx + 1] + \
				[new_content if not new_content.endswith('\n') else new_content] + \
				lines[end_idx:]
		
	# Write to output file
	with open(output_file, 'w') as f:
		f.writelines(new_lines)

def generateTestFile():
	with open('test.py', 'w+') as f:
		for l in getTestFile():
			f.write(l)

def setNumberOfHosts(x: int):
	assert x > 0
	global numHosts
	numHosts = x

def setNumberOfSwitches(x: int):
	assert x > 0
	global numSwitches
	numSwitches = x

# add a link between 2 network entities (hosts/switches)
# t1: 'h' (host) or 's': switch
# x1: a number in the range [1, number of hosts] if t1 == 'h' or [1, number of switches] if t1 == 's'
# t2: 'h' (host) or 's': switch
# x2: a number in the range [1, number of hosts] if t1 == 'h' or [1, number of switches] if t1 == 's'
# bw: bandwidth of the link, in mbps (0 if you want to leave it unspecified)
def addLink(t1: str, x1: int, t2: str, x2: int, bw: int = 0):
	assert t1 in ['h', 'H', 's', 'S']
	assert t2 in ['h', 'H', 's', 'S']

	t1 = t1.lower()
	if t1 == 'h':
		assert 1 <= x1 <= numHosts
	else:
		assert 1 <= x1 <= numSwitches

	t2 = t2.lower()
	if t2 == 'h':
		assert 1 <= x2 <= numHosts
	else:
		assert 1 <= x2 <= numSwitches

	assert bw >= 0

	p1, p2 = f"{t1}{x1}", f"{t2}{x2}"
	assert p1 != p2
	for p in links:
		if p[0] == p1 and p[1] == p2:
			raise AssertionError
		if p[0] == p2 and p[1] == p1:
			raise AssertionError
	
	pair = (p1, p2) if bw == 0 else (p1, p2, f"bw={bw}")
	links.add(pair)

def generateTopologyFile():
	assert numHosts > 0
	assert numSwitches > 0
	lines = open('custom-topo.py', 'r').readlines()

	new_content = [
		f"s{i} = self.addSwitch('s{i}')" for i in range(1, numHosts + 1)
	] + \
	[''] + \
	[
		f"h{i} = self.addHost('h{i}')" for i in range(1, numHosts + 1)
	] + \
	[''] + \
	[
		f"self.addLink{p}" for p in links
	]

	indentLevel = 2

	indent = '\t' * indentLevel
	new_content = ''.join(f"{indent}{line}\n" for line in new_content)

	start_marker = '# START build'
	end_marker = '# END build'
	output_file = 'custom-topo.py'

	replace_test_section(
		lines, new_content, 
		start_marker, end_marker, 
		output_file
	)	

if __name__ == '__main__':
	# replace_test_section(
	# 	open('custom-topo-with-tests.py').readlines(),
	# 	"".join(getTestFile())
	# )

	setNumberOfHosts(4)
	setNumberOfSwitches(4)

	addLink('s', 1, 's', 2, 5)
	addLink('s', 1, 's', 3, 5)
	addLink('s', 2, 's', 4, 5)
	addLink('s', 3, 's', 4, 5)

	addLink('h', 1, 's', 1)
	addLink('h', 2, 's', 2)
	addLink('h', 3, 's', 3)
	addLink('h', 4, 's', 4)

	generateTopologyFile()

	addPairToTest(1, 2)
	addPairToTest(3, 2)
	addPairToTest(4, 2)
	
	addPairToTest(2, 1)
	addPairToTest(3, 1)
	addPairToTest(4, 1)

	addPairToTest(1, 4)
	addPairToTest(2, 4)
	addPairToTest(3, 4)

	addPairToTest(1, 3)
	addPairToTest(2, 3)
	addPairToTest(4, 3)

	generateTestFile()
	

# to use the output file "test.py":
# py execfile('test.py')
# py run_tests(net)