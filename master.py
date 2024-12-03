# master.py

import subprocess
import time
import os
import argparse

from main import mininetConfigFileName, topoFileName, onosConfigFileName, hopsScriptFileName, sortedLinksFileName
from main_extension import testFileName
from parse_flow_files import portMatrixFileName
from get_graph_attr import graphAttrFileName

flowsScript = 'get_flows.sh'
flowsScriptOutputFileName = 'flows.txt'

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='Generate network topology and ONOS configuration')
    
    # Add arguments
    parser.add_argument(
        'num_nodes', type=int, 
        help='Number of nodes (switches and hosts both)'
    )
    
    parser.add_argument(
        'connectivity_type', type=str, choices=['nsfnet', 'geant2', 'germany50'],
        help='Type of network connectivity (nsfnet, geant2, or germany50)'
    )

    parser.add_argument(
        'num_runs', type=int, 
        help='Number of times the simulation should be run.'
    )

    parser.add_argument(
        'test_duration', type=int, 
        help='time for which the simulation/test should run IN SECONDS'
    )

    parser.add_argument(
        'output_stats_frequency', type=int, 
        help='the frequency at which the network statistics should be reported from the raw data IN MILLISECONDS'
    )

    parser.add_argument(
        'traffic_intensity_low', type=int, 
        help='traffic intensity (as described in RouteNet)'
    )

    parser.add_argument(
        'traffic_intensity_high', type=int, 
        help='traffic intensity (as described in RouteNet)'
    )

    args = parser.parse_args()
    return args

def cleanup():
    """Clean up mininet container and tmux session"""
    print("Cleaning up environment...")
    # Kill the tmux session
    subprocess.run(['tmux', 'kill-session', '-t', 'onos_session'], stderr=subprocess.DEVNULL)
    time.sleep(1)
    # Remove all containers
    subprocess.run('./clear.sh', shell=True, stderr=subprocess.DEVNULL)
    time.sleep(1)

def check_mininet_cli_ready():
    """Check if mininet CLI is ready by looking for 'mininet>' prompt"""
    try:
        # Capture the output of the tmux pane
        result = subprocess.run(
            ['tmux', 'capture-pane', '-t', 'onos_session:2', '-p'],
            capture_output=True,
            text=True
        )
        # Check if the last non-empty line ends with 'mininet>'
        lines = [line for line in result.stdout.split('\n') if line.strip()]
        
        return lines and lines[-1].strip().endswith('mininet>')
    except Exception as e:
        print(f"Error checking mininet CLI: {e}")
        return False

def runner(args):
    rootSimulationDir = f"simulations/{args.connectivity_type}_{args.num_nodes}_{args.traffic_intensity_low}_{args.traffic_intensity_high}/"
    if not os.path.isdir(rootSimulationDir):
        os.makedirs(rootSimulationDir)
    for trafficIntensity in range(args.traffic_intensity_low, args.traffic_intensity_high + 1):
        cleanup()
        for runNum in range(1, args.num_runs + 1):
            
            print('-----' * 15)
            simulationDir = os.path.join(rootSimulationDir, f"lambda_{trafficIntensity}/")
            if not os.path.isdir(simulationDir):
                os.mkdir(simulationDir)

            runDir = os.path.join(simulationDir, f"run_{runNum}/")
            if not os.path.isdir(runDir):
                os.mkdir(runDir)
            
            rawDir = os.path.join(runDir, "raw_data")
            if not os.path.isdir(rawDir):
                os.mkdir(rawDir)

            decodedDir = os.path.join(runDir, "decoded_data")
            if not os.path.isdir(decodedDir):
                os.mkdir(decodedDir)
            
            calculated_args = {
                'topo_file_path': simulationDir,
                'onos_config_file_path': simulationDir,
                'mininet_config_file_path': simulationDir,
                'flows_script': flowsScript,
                'flows_script_output_file_path': simulationDir,
                'port_matrix_file_path': simulationDir,
                'test_file_path': simulationDir,
                'raw_file_path': rawDir,
                'decoded_file_path': decodedDir,
                'graph_attr_path': simulationDir
            }
            # mn_stratum is mininet
            calculated_args["mn_stratum_topo_file"] = \
                os.path.join(calculated_args["mininet_config_file_path"], mininetConfigFileName)
            calculated_args["onos_config_file"] = \
                os.path.join(calculated_args["onos_config_file_path"], onosConfigFileName)
            calculated_args["topo_file"] = \
                os.path.join(calculated_args["topo_file_path"], topoFileName)
            calculated_args["test_file"] = \
                os.path.join(calculated_args["test_file_path"], testFileName)
            calculated_args["flows_script_output_file"] = \
                os.path.join(calculated_args["flows_script_output_file_path"], flowsScriptOutputFileName)
            calculated_args["sorted_links_file"] = \
                os.path.join(calculated_args["mininet_config_file_path"], sortedLinksFileName)

            if runNum == 1:
                subprocess.run([
                    'python3', 'main.py',
                    f'{args.num_nodes}', f'{args.connectivity_type}', f'{calculated_args["topo_file_path"]}',
                    f'{calculated_args["onos_config_file_path"]}', f'{calculated_args["mininet_config_file_path"]}'
                ])
                time.sleep(1)
                subprocess.run([
                    'python3', 'main_extension.py', 
                    f'{args.test_duration}', f'{args.output_stats_frequency}', f'{trafficIntensity}', 
                    f'{calculated_args["topo_file"]}', f'{calculated_args["test_file_path"]}', 
                    f'{calculated_args["raw_file_path"]}', f'{calculated_args["decoded_file_path"]}'
                ])
                #  just cleanup after a set of runs
                while not setup_ONOS_and_mininet(args, calculated_args, runNum, 7):
                    cleanup()
            else:
                print(f"updating {calculated_args['test_file']} for run number {runNum}")
                subprocess.run([
                    'sed', '-i', f's/run_{runNum-1}/run_{runNum}/g', f"{calculated_args['test_file']}"
                ])
            
            run_setup_openflow_switches(args, calculated_args, runNum)
            # run_setup(args, calculated_args, runNum, 7)
            # run_setup_only_print(args, calculated_args)

def ppprint(x):
    print(" ".join(x))

def setup_ONOS_and_mininet(args, calculated_args, run_number, max_attempts = 5):
    # Create new tmux session
    print("Create new tmux session")
    subprocess.run(['tmux', 'new-session', '-d', '-s', 'onos_session'])
    cwd = os.getcwd()
    
    # window 0: at home dir
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])

    # Window 1: Controller
    print("Window 1: Starting controller...")
    # window 1: ONOS w/ logs
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', f'cd {cwd} && make controller', 'C-m'])
    time.sleep(70)

    # window 2: mininet CLI
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])

    # window 3: for entering ONOS container to get flows
    subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])

    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        attempt += 1
        print(f"\nAttempt {attempt} of {max_attempts}")

        # remove any existing mn-stratum container
        subprocess.run([
            'tmux', 'send-keys', '-t', 'onos_session:0',
            'docker rm -f mn-stratum', 'C-m'])


        # Window 2: Mininet
        print("Window 2: Starting Mininet...")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', \
            f'cd {cwd} && make mininet MN_STRATUM_TOPO_FILE={calculated_args["mn_stratum_topo_file"]}', 'C-m'
        ])
        time.sleep(args.num_nodes * 2)

        # Run pingall twice
        print("Running first pingall...")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
        time.sleep(args.num_nodes * 2)
        print("Running second pingall...")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
        time.sleep(args.num_nodes * 2)

        # Check if mininet CLI is ready
        if not check_mininet_cli_ready():
            print("Mininet CLI not ready, will retry...")
            continue
        
        print("Mininet CLI is ready!")
        success = True

    if not success:
        print(f"Failed to set up network after {max_attempts} attempts")
        return False

    # Attach to the tmux session
    # subprocess.run(['tmux', 'attach-session', '-t', 'onos_session'])
    return True

def run_setup_openflow_switches(args, calculated_args, run_number):
    attempt = 0
    success = False

    # Continue with test execution
    print("Running tests...")
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', \
        f'py execfile(\'{calculated_args["test_file"]}\')', 'C-m'
    ])
    time.sleep(1)
    subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'py run_tests(net)', 'C-m'])
    # itgrecv start + itgsend + itgrecv kill + itgdec
    itgSendDuration = args.test_duration
    # we don't wait for the test script to finish execution
    # instead, we calculate the time taken to start ITGRecv processes & execute the ITGSend commands
    # then, we execute the script to get the flows
    # ONOS is very quick to remove flows once they are inactive; so we want to query 
    # ONOS just before the ITGSend commands are done executing
    time.sleep(itgSendDuration)

    # get flows on the last run
    if run_number == args.num_runs:

        # Window 4: Handle get_flows script
        print("Window 4: Handle get_flows script")
        
        # Make the script executable
        print("Make the get_flows.sh executable")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 
                        'chmod', '+x', calculated_args["flows_script"], 'C-m'])
        
        # Copy and execute get_flows script
        print("Copy and execute get_flows script")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 
                    f'docker cp {calculated_args["flows_script"]} onos:/root/onos/get_flows.sh', 'C-m'])
        time.sleep(0.1)
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 
                    'docker exec onos chmod +x /root/onos/get_flows.sh', 'C-m'])
        time.sleep(0.1)
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 
                    'docker exec onos /root/onos/get_flows.sh', 'C-m'])
        time.sleep(args.num_nodes)
        
        # Copy results back
        print("Copy results back")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 
                f'docker cp onos:/root/onos/paths.txt {calculated_args["flows_script_output_file"]}', 'C-m'])
        time.sleep(2)

        # get the port matrix from the output of the get_flows script
        print("get the port matrix from the output of the get_flows script")

        get_port_matrix_args = f'{args.num_nodes} ' + \
                f'{calculated_args["flows_script_output_file"]} {calculated_args["port_matrix_file_path"]}'
        
        subprocess.run([
            'tmux', 'send-keys', '-t', 'onos_session:0',
            f'python3 parse_flow_files.py {get_port_matrix_args}', 'C-m'])

        print(f"generate the graph attr file: {graphAttrFileName}")

        get_graph_attr_args = f'{calculated_args["topo_file"]} ' + \
                f'{calculated_args["sorted_links_file"]} {calculated_args["graph_attr_path"]}'
        
        subprocess.run([
            'tmux', 'send-keys', '-t', 'onos_session:0',
            f'python3 get_graph_attr.py {get_graph_attr_args}', 'C-m'])
    
    # test_duration * 2 : for ITGSend
    # 10                : for killing of ITGRecv processes
    # 5                 : starting of ITGRecv processes
    time.sleep(args.test_duration * 2 + 10 + 5)
    while (not check_mininet_cli_ready()):
        print("waiting for test script to finish")
        time.sleep(1)

if __name__ == "__main__":
    args = getCommandLineArgs()
    runner(args)