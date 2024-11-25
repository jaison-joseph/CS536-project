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
    # Activate fwd
    print("Activate fwd")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'app activate fwd', 'C-m'])
    time.sleep(2)
    
    # Window 4: NetCFG
    print("Window 4: NetCFG")
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', f'cd {cwd} && make netcfg', 'C-m'])
    time.sleep(10)
    
    # Run pingall in mininet
    print("Run pingall in mininet")
    # subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', 'pingall', 'C-m'])
    time.sleep(60)
    print("Run pingall in mininet")
    # subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', 'pingall', 'C-m'])
    time.sleep(60)
    print("Run pingall in minine (3rd time's the charm)")
    # subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', 'pingall', 'C-m'])
    time.sleep(60)
    
    # Window 5: Handle get-hops script
    print("Window 5: Handle get-hops script")
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    # Create get-hops.sh content
    #     print("Create get-hops.sh content")
    #     get_hops_content = '''#!/bin/bash
    # echo "(s1, s2): $(paths device:s1 device:s2)" >> paths.txt
    # echo "(s1, s3): $(paths device:s1 device:s3)" >> paths.txt
    # echo "(s1, s4): $(paths device:s1 device:s4)" >> paths.txt
    # echo "(s1, s5): $(paths device:s1 device:s5)" >> paths.txt
    # '''
    #     with open('get-hops.sh', 'w') as f:
    #         f.write(get_hops_content)
    
    # Make the script executable
    print("Make the get-hops.sh executable")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', 
                    'chmod', '+x', 'get-hops.sh', 'C-m'])
    
    # Copy and execute get-hops script
    print("Copy and execute get-hops script")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', 
                   'docker cp get-hops.sh onos:/root/onos/get-hops.sh', 'C-m'])
    time.sleep(1)
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', 
                   'docker exec onos chmod +x /root/onos/get-hops.sh', 'C-m'])
    time.sleep(1)
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', 
                   'docker exec onos /root/onos/get-hops.sh', 'C-m'])
    time.sleep(2)
    
    # Copy results back
    print("Copy results back")
    output_path = "/home/ubuntu/assignment0/public/assignments/temp-test/CS536-project/hops.txt"
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', 
                   f'docker cp onos:/root/onos/paths.txt {output_path}', 'C-m'])
    
    # Attach to the tmux session
    subprocess.run(['tmux', 'attach-session', '-t', 'onos_session'])

if __name__ == "__main__":
    run_setup()