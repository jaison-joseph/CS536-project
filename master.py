# failed attempt at controlling the terminals
# mininet crashes

import subprocess
import time
import os
import argparse

def getCommandLineArgs():
	parser = argparse.ArgumentParser(description='Generate network topology and ONOS configuration')
	
	# Add arguments
	parser.add_argument('num_hosts', type=int, help='Number of hosts')
	parser.add_argument('num_switches', type=int, help='Number of switches')
	parser.add_argument('connectivity_type', type=str, choices=['nsfnet', 'geant2', 'germany50'],
						help='Type of network connectivity (nsfnet, geant2, or germany50)')
	parser.add_argument('-v', '--visualize', action='store_true', help='visualize the network topology.')
	
	# Parse arguments
	args = parser.parse_args()

	return args

def run_setup(args):
	# Install tmux if not already installed
	# subprocess.run(['sudo', 'apt-get', 'update', '-y'])
	# subprocess.run(['sudo', 'apt-get', 'install', '-y', 'tmux'])
	
	# Get current working directory
	cwd = os.getcwd()
	
	# Create new tmux session
	print("Create new tmux session")
	subprocess.run(['tmux', 'new-session', '-d', '-s', 'onos_session'])

	# create the ONOS network config file (cfg/onos_config.json), mininet custom network file(custom-topo.py) and D-ITG test file(test.py)
	# Window 1: homedir: generate network config and test script
	print("Window 1: create the ONOS network config file (cfg/onos_config.json), mininet custom network file(custom-topo.py) and D-ITG test file(test.py)")
	subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
	subprocess.run([
		'tmux', 'send-keys', '-t', 'onos_session:0', 
		f"cd {cwd} && python3 main.py {args.num_switches} {args.num_hosts} {args.connectivity_type} && python3 main_extension.py", 
 		'C-m'
	])
	time.sleep(4)

	
	# Window 2: Controller
	print("Window 2: Controller")
	subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', f'cd {cwd} && make controller' , 'C-m'])
	time.sleep(15)
	
	# Window 3: Mininet
	print("Window 3: Mininet")
	subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', f'cd {cwd} && make mininet', 'C-m'])
	time.sleep(10)
	
	# Window 4: ONOS CLI
	print("Window 4: ONOS CLI")
	subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', f'cd {cwd} && make cli', 'C-m'])
	time.sleep(5)
	# Send password
	print("Send password")
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 'rocks', 'C-m'])
	time.sleep(5)
	
	# Window 5: NetCFG
	print("Window 5: NetCFG")
	subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', f'cd {cwd} && make netcfg', 'C-m'])
	time.sleep(5)


	# Activate fwd
	print("Activate fwd")
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 'app activate fwd', 'C-m'])
	time.sleep(2)
	
	# Run pingall in mininet
	print("Run pingall in mininet")
	# subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 'pingall', 'C-m'])
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
	time.sleep(10)
	print("Run pingall in mininet")
	# subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 'pingall', 'C-m'])
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
	time.sleep(10)

	# run the test.py from the mininet shell
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'py execfile(\'test.py\')', 'C-m'])
	time.sleep(3)
	subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'py run_tests(net)', 'C-m'])

	
	# Attach to the tmux session
	subprocess.run(['tmux', 'attach-session', '-t', 'onos_session'])

if __name__ == "__main__":
	args = getCommandLineArgs()
	run_setup(args)