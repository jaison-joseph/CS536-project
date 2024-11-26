# look at the comments above the "if __name__ == '__main__':" line

import datetime
from collections import defaultdict
import json
from random import uniform

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

# for the traffic matrix
trafficIntensity = 11

testDuration = 15
defaultTestBandwidth = 1

def read_topo_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        
    num_hosts = data['number_hosts']
    num_switches = data['number_switches']
    network_edges = data['network_edges']
    
    return num_hosts, num_switches, network_edges

def getTraficMatrixEntry():
	assert numHosts > 1
	# TM(Si, Dj) = U(0.1, 1) * TI / (N-1)
	u = uniform(0.1, 1.0)  
	# or with numpy: u = np.random.uniform(0.1, 1.0)
	tm_value = u * trafficIntensity / (numHosts-1)
	return tm_value

# will output code to test connection between hosts clientHostNum and host serverHostNum
# will setup an iperf3 server at host serverHostNum
def addPairToTest(clientHostNum: int, serverHostNum: int, bw = -1):
	assert 0 <= clientHostNum < numHosts
	assert 0 <= serverHostNum < numHosts
	if bw == -1:
		bw = defaultTestBandwidth
	assert bw > 0
	assert clientHostNum != serverHostNum
	pair = (clientHostNum, serverHostNum, bw)
	for p in pairs:
		assert not(p[0] == clientHostNum and p[1] == serverHostNum), "duplicate test pair"
	targets.add(serverHostNum)
	pairs.add(pair)

	lk[serverHostNum] += 1

def getIperfCommands():
	res = []
	
	assert len(targets) > 0
	assert len(pairs) > 0
	
	res.append("# start iperf servers")
	for t in targets:
		res.append(f"print('starting {lk[t]} iperf server(s) @ {t}')")
		for i in range(lk[t]):
			res.append(f"h{t}.cmd('iperf3 -s -p {5100 + i}&')")
	res.append("")

	res.append("# wait for servers to start")
	res.append("print('wait for servers to start')")
	res.append("time.sleep(2)")
	res.append("")

	res.append("# run iperf clients")
	res.append("print('run iperf clients')")
	for c, s, bw in pairs:
		# res.append(f"h{c} iperf3 -c h{s} -u -l 1000 -t 15 -i 1")
		res.append(f"print('launching {c} -> {s} iperf')")
		# res.append(f"h{c}.cmd('nohup iperf3 -c 10.0.0.{s} -u -l 10000 -t 15 -p {5100 + lk[s]} -i 1 > {outputFilePrefix}_{c}_{s}.txt 2>&1 &')")
		res.append(f"h{c}.cmd('nohup iperf3 -c 10.0.0.{s} -u -b {bw}M -t {testDuration} -p {5100 + lk[s]} -i 1 --verbose  --json > {outputFilePrefix}_{c}_{s}.txt 2>&1 &')")
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
	res.append(f"time.sleep({testDuration * 2})")
	res.append("")

	res.append("# Kill iperf servers")
	res.append("print('Kill iperf servers')")
	for t in targets:
		res.append(f"h{t}.cmd('killall iperf3')")
	res.append("")

	return res

def getDitgCommands():
	res = []
	
	assert len(targets) > 0
	assert len(pairs) > 0
	
	res.append("# start ditg servers")
	for t in targets:
		res.append(f"print('starting ditg server @ {t}')")
		res.append(f"h{t}.cmd('nohup ITGRecv &')")
	res.append("")

	res.append("# wait for servers to start")
	res.append("print('wait for servers to start')")
	res.append("time.sleep(2)")
	res.append("")

	res.append("# run iperf clients")
	res.append("print('run iperf clients')")
	for c, s, bw in pairs:
		# res.append(f"h{c} iperf3 -c h{s} -u -l 1000 -t 15 -i 1")
		res.append(f"print('launching {c} -> {s} ITGSend')")
		# res.append(f"h{c}.cmd('nohup iperf3 -c 10.0.0.{s} -u -l 10000 -t 15 -p {5100 + lk[s]} -i 1 > {outputFilePrefix}_{c}_{s}.txt 2>&1 &')")
		res.append(f"h{c}.cmd('nohup ITGSend -a 10.0.0.{s+1} -T UDP -Fs cfg/ditg_packet_sizes.txt -C {bw:.5f} -t {testDuration * 1000} -x {outputFilePrefix}_{c}_{s}.txt 2>&1 &')")
		lk[s] -= 1
	res.append("")

	assert all(x == 0 for x in lk.values()), list(lk.values())
	
	res.append("# wait for ITGSend to finish")
	res.append("print('wait for ITGSend to finish')")
	res.append(f"time.sleep({testDuration * 2})")
	res.append("")

	res.append("# Kill ITGRecv servers")
	res.append("print('Kill ITGRecv servers')")
	for t in targets:
		res.append(f"h{t}.cmd('killall ITGRecv')")
	res.append("")

	return res

def getTestFile(target = 'iperf3'):
	targetOptions = ['iperf3', 'ditg']
	assert numHosts > 0, "please make a call to setNumberOfHosts first"
	assert numSwitches > 0, "please make a call to setNumberOfSwitches first"
	assert target in targetOptions, f"invalid target option, should be one of {targetOptions}"
	hostLineLhs = ", ".join(["h"+str(i) for i in range(numHosts)])
	hostLineRhs = ", ".join(["'h"+str(i)+"'" for i in range(numHosts)])

	fileStart = [
		"def run_tests(net):",
		"	from datetime import datetime",
		"	# Create logs directory if it doesn't exist",
		"	if not os.path.exists('logs'):",
		"		os.makedirs('logs')",
		"",
		"	# Get current timestamp for log files",
		"	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')",
		# "	timestamp = str(datetime.now()).replace(' ', '_')",
		"",
		"",	
		"	# Get host objects",
		f"	{hostLineLhs} = net.get({hostLineRhs})",
		"",
		"	try:"
	]


	fileEnd = [
		"	except Exception as e:",
		"		print(e)",
		"",
		"# this file is executed from the mininet shell; this is how to use it:",
		"# mininet> py execfile('test.py')",
		"# mininet> py run_tests(net)"
	]

	indentLevel = 2

	res = []
	if target == 'iperf3':
		commands = getIperfCommands()
	elif target == 'ditg':
		commands = getDitgCommands()
	
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

def setTestDuration(x: int):
	assert x > 0
	global testDuration
	testDuration = x

def setTestBandwidth(x: int):
	assert x > 0
	global defaultTestBandwidth
	defaultTestBandwidth = x

# add a link between 2 network entities (hosts/switches)
# t1: 'h' (host) or 's': switch
# x1: a number in the range [0, number of hosts) if t1 == 'h' or [0, number of switches) if t1 == 's'
# t2: 'h' (host) or 's': switch
# x2: a number in the range [0, number of hosts) if t1 == 'h' or [0, number of switches) if t1 == 's'
# bw: bandwidth of the link, in mbps (0 if you want to leave it unspecified)
# if you have a link from host 1 to host 2 already, you can't establish another link from host 2 to host 1
def addLink(t1: str, x1: int, t2: str, x2: int, bw: int = 0):
	assert t1 in ['h', 'H', 's', 'S']
	assert t2 in ['h', 'H', 's', 'S']

	t1 = t1.lower()
	if t1 == 'h':
		assert 0 <= x1 < numHosts
	else:
		assert 0 <= x1 < numSwitches

	t2 = t2.lower()
	if t2 == 'h':
		assert 0 <= x2 < numHosts
	else:
		assert 0 <= x2 < numSwitches

	assert bw >= 0

	p1, p2 = f"{t1}{x1}", f"{t2}{x2}"
	assert p1 != p2
	for p in links:
		if p[0] == p1 and p[1] == p2:
			raise AssertionError
		if p[0] == p2 and p[1] == p1:
			raise AssertionError
	
	pair = (p1, p2) if bw == 0 else (p1, p2, bw)
	links.add(pair)

def generateMininetTopologyFile(fileName = 'custom-topo.py'):
	assert numHosts > 0, "please make a call to setNumberOfHosts first"
	assert numSwitches > 0, "please make a call to setNumberOfSwitches first"
	lines = open(fileName, 'r').readlines()

	new_content = [
		f"s{i} = self.addSwitch('s{i}')" for i in range(numSwitches)
	] + \
	[''] + \
	[
		f"h{i} = self.addHost('h{i}')" for i in range(numHosts)
	] + \
	[''] + \
	[
		f"self.addLink({p[0]}, {p[1]}, bw={p[2]})" \
		if len(p) == 3 else \
		f"self.addLink({p[0]}, {p[1]})" \
		for p in links
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

def autoGenerateTest(networkConfigFile = 'cfg/topo.json'):
	numHosts, numSwitches, edges = read_topo_json(networkConfigFile)

	setNumberOfHosts(numHosts)
	setNumberOfSwitches(numSwitches)

	for n1, n2, bw in edges:
		addLink(n1[0], int(n1[1:]), n2[0], int(n2[1:]), bw)

	# TODO:
	# for each pair of hosts to test, call addPairToTest
	# e.g. for testing connection between s1 & s2 & 100kbps, addPairToTest(1, 2, 0.1)
	# TM(Si, Dj) = U(0.1, 1) * TI / (N-1) 
	for i in range(numHosts):
		for j in range(numHosts):
			if i == j:
				continue
			addPairToTest(i, j, getTraficMatrixEntry())

	with open('test.py', 'w+') as f:
		for l in getTestFile('ditg'):
			f.write(l)

'''

	this file modifies custom-topo.py and test.py
	to use this file, you need to make the following function calls (ideally in this order):

	- setNumberOfHosts(x: int) # number of hosts in the topology
		if you set setNumberOfHosts to 5, then you reference them by a number in the range [0, 4]

	- setNumberOfSwitches(x: int) # number of switches in the topology
		- # you want to call these 2 functions first, before the other functions

	- addLink(t1, x, t2, y, bandwith)
		- t1 & t2: set it to 's' for switch or 'h' for host
		- x & y: int for the host/switch number
		- (optional) bandwidth: link speed limit in mbps
		- if you have a link from host 1 to host 2 already, you can't establish another link from host 2 to host 1

	- generateMininetTopologyFile()
		- you can make this call after all your calls to addLink()
		- this function modifies the custom-topo.py, used by mininet

	- setTestDuration(x)
		- the duration the tests should run for, in seconds
		- default value is 15 seconds, if this function is not called

	- setTestBandwidth(x)
		- the link speed each test pair of hosts should attempt to reach in mbps
		- default value is 1 mbps, if this function is not called

	- addPairToTest(x, y, bw)
		- add a pair of hosts to test the bandwidth of
		- x & y: int: value in [1, number-of-hosts + 1]
		- (optional) bw: the throughput this connection should attempt to reach in mbps
			- if not specified, it will default to the value of defaultTestBandwidth 

	- generateTestFile()
		- generate the test.py file

'''
def exampleUsage():
	# replace_test_section(
	# 	open('custom-topo-with-tests.py').readlines(),
	# 	"".join(getTestFile())
	# )

	setNumberOfHosts(4)
	setNumberOfSwitches(4)

	# for the topology file
	addLink('s', 1, 's', 2, 5)
	addLink('s', 1, 's', 3, 5)
	addLink('s', 2, 's', 4, 5)
	addLink('s', 3, 's', 4, 5)

	addLink('h', 1, 's', 1)
	addLink('h', 2, 's', 2)
	addLink('h', 3, 's', 3)
	addLink('h', 4, 's', 4)

	generateMininetTopologyFile()

	# for the test file
	setTestDuration(15)
	setTestBandwidth(1)

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
	# addPairToTest(4, 3, 2)
	addPairToTest(4, 3)

	generateTestFile()

if __name__ == '__main__':
	autoGenerateTest()
	

# to use the output file "test.py":
# py execfile('test.py')
# py run_tests(net)