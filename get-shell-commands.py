import datetime
from collections import defaultdict

# we use numbers in [1, numHosts + 1] to identify each host in the code
numHosts = 4
numSwitches = 4
indentLevel = 2

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

# timestamp_number-of-hosts_number-of-switches
outputFilePrefix = f"logs/{str(datetime.datetime.now()).replace(' ', '-')}" + \
					f"_{str(numHosts)}_{str(numSwitches)}"

targets = set()
pairs = set()

lk = defaultdict(int)

# will output code to test connection between hosts h{x+1} and host h{y+1}
# will setup an iperf3 server at host h{y+1}
def testPair(clientHostNum: int, serverHostNum: int):
	assert 1 <= clientHostNum <= numHosts + 1
	assert 1 <= serverHostNum <= numHosts + 1
	assert clientHostNum != serverHostNum
	targets.add(serverHostNum)
	pairs.add((clientHostNum, serverHostNum))

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

def getFunction():
	testPair(1, 2)
	testPair(3, 2)
	testPair(4, 2)
	
	testPair(2, 1)
	testPair(3, 1)
	testPair(4, 1)

	testPair(1, 4)
	testPair(2, 4)
	testPair(3, 4)

	testPair(1, 3)
	testPair(2, 3)
	testPair(4, 3)

	res = []
	commands = getCommands()
	for line in fileStart:
		res.append(f"{line}\n")
	for line in commands:
		res.append(f"{'	' * indentLevel}{line}\n")
	for line in fileEnd:
		res.append(f"{line}\n")
	return res

def replace_test_section(lines, new_content, output_file="custom-topo-with-tests.py"):
	start_marker = "# START run_tests"
	end_marker = "# END run_tests"
		
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
	new_lines = lines[:start_idx] + [start_marker + "\n\n"] + \
				[new_content if not new_content.endswith('\n') else new_content] + \
				["\n" + end_marker + "\n"] + lines[end_idx + 1:]
		
	# Write to output file
	with open(output_file, 'w') as f:
		f.writelines(new_lines)

if __name__ == '__main__':
	# replace_test_section(
	# 	open('custom-topo-with-tests.py').readlines(),
	# 	"".join(getFunction())
	# )
	with open('test.py', 'w+') as f:
		for l in getFunction():
			f.write(l)

# py execfile('test.py')
# py run_tests(net)