# failed attempt at controlling the terminals
# mininet crashes

import subprocess
import time
import os

def run_setup():
    # Install tmux if not already installed
    # subprocess.run(['sudo', 'apt-get', 'update', '-y'])
    # subprocess.run(['sudo', 'apt-get', 'install', '-y', 'tmux'])
    
    # Get current working directory
    cwd = os.getcwd()
    
    # Create new tmux session
    print("Create new tmux session")
    subprocess.run(['tmux', 'new-session', '-d', '-s', 'onos_session'])
    
    # Window 1: Controller
    print("Window 1: Controller")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:0', f'cd {cwd} && make controller' , 'C-m'])
    time.sleep(15)
    
    # Window 2: Mininet
    print("Window 2: Mininet")
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', f'cd {cwd} && make mininet', 'C-m'])
    time.sleep(10)
    
    # Window 3: ONOS CLI
    print("Window 3: ONOS CLI")
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', f'cd {cwd} && make cli', 'C-m'])
    time.sleep(5)
    # Send password
    print("Send password")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'rocks', 'C-m'])
    time.sleep(5)
    
    # Window 4: NetCFG
    print("Window 4: NetCFG")
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', f'cd {cwd} && make netcfg', 'C-m'])
    time.sleep(5)

	# Activate fwd
    print("Activate fwd")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'app activate fwd', 'C-m'])
    time.sleep(2)
    
    # Run pingall in mininet
    print("Run pingall in mininet")
    # subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', 'pingall', 'C-m'])
    time.sleep(10)
    print("Run pingall in mininet")
    # subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', 'pingall', 'C-m'])
    time.sleep(10)
    
    # Attach to the tmux session
    subprocess.run(['tmux', 'attach-session', '-t', 'onos_session'])

if __name__ == "__main__":
    run_setup()