import subprocess
import time
import os
import argparse

from main import mininetConfigFileName, topoFileName, onosConfigFileName, hopsScriptFileName, hopsScriptOutputFileName
from main_extension import testFileName
from get_port_matrix import portMatrixFileName

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
        'traffic_intensity', type=int, 
        help='traffic intensity (as described in RouteNet: in range [11, 16])'
    )

    args = parser.parse_args()
    return args

def cleanup():
    """Clean up mininet container and tmux session"""
    print("Cleaning up environment...")
    # Kill the tmux session
    subprocess.run(['tmux', 'kill-session', '-t', 'onos_session'], stderr=subprocess.DEVNULL)
    time.sleep(2)
    # Remove mininet container
    subprocess.run('./clear.sh', shell=True, stderr=subprocess.DEVNULL)
    time.sleep(3)

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
    simulationDir = f"simulations/{args.connectivity_type}_{args.num_nodes}_{args.traffic_intensity}/"
    if not os.path.isdir(simulationDir):
        os.makedirs(simulationDir)
    for runNum in range(1, args.num_runs + 1):
        print('-----' * 15)
        simulationDir = f"simulations/{args.connectivity_type}_{args.num_nodes}_{args.traffic_intensity}/"
        runDir = f"simulations/{args.connectivity_type}_{args.num_nodes}_{args.traffic_intensity}/run_{runNum}/"
        if not os.path.isdir(simulationDir):
            os.mkdir(simulationDir)
        if not os.path.isdir(runDir):
            os.mkdir(runDir)
        rawDir = os.path.join(runDir, "raw_data")
        decodedDir = os.path.join(runDir, "decoded_data")
        if not os.path.isdir(rawDir):
            os.mkdir(rawDir)
        if not os.path.isdir(decodedDir):
            os.mkdir(decodedDir)
        calculated_args = {
            'topo_file_path': simulationDir,
            'onos_config_file_path': simulationDir,
            'mininet_config_file_path': simulationDir,
            'hops_script_file_path': simulationDir,
            'hops_script_output_file_path': simulationDir,
            'port_matrix_file_path': simulationDir,
            'test_file_path': simulationDir,
            'raw_file_path': rawDir,
            'decoded_file_path': decodedDir
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
        calculated_args["hops_script"] = \
            os.path.join(calculated_args["hops_script_file_path"], hopsScriptFileName)
        calculated_args["hops_script_output_file"] = \
            os.path.join(calculated_args["hops_script_output_file_path"], hopsScriptOutputFileName)

        if runNum == 1:

            subprocess.run([
                'python3', 'main.py',
                f'{args.num_nodes}', f'{args.connectivity_type}', f'{calculated_args["topo_file_path"]}',
                f'{calculated_args["onos_config_file_path"]}', f'{calculated_args["mininet_config_file_path"]}', 
                f'{calculated_args["hops_script_file_path"]}'
            ])

            time.sleep(1)
            subprocess.run([
                'python3', 'main_extension.py', 
                f'{args.test_duration}', f'{args.output_stats_frequency}', f'{args.traffic_intensity}', 
                f'{calculated_args["topo_file"]}', f'{calculated_args["test_file_path"]}', 
                f'{calculated_args["raw_file_path"]}', f'{calculated_args["decoded_file_path"]}'
            ])

        else:
            
            print(f"updating {calculated_args['test_file']} for run number {runNum}")
            
            subprocess.run([
                'sed', '-i', f's/run_{runNum-1}/run_{runNum}/g', f"{calculated_args['test_file']}"
            ])
        
        run_setup(args, calculated_args, runNum, 7)
        # run_setup_only_print(args, calculated_args)

def ppprint(x):
    print(" ".join(x))

def run_setup_only_print(args, calculated_args, run_number, max_attempts = 5):
    
    # Create new tmux session
    print("Create new tmux session")
    # subprocess.run(['tmux', 'new-session', '-d', '-s', 'onos_session'])
    cwd = os.getcwd()

    # Rest of your window creation and setup code...
    # Window 1: Generate network config and test script
    print("Window 1: Creating configuration files...")

    # main_py_args = \
    #     f'{args.num_nodes} {args.connectivity_type} {calculated_args["topo_file_path"]} ' + \
    #     f'{calculated_args["onos_config_file_path"]} {calculated_args["mininet_config_file_path"]} ' + \
    #     f'{calculated_args["hops_script_file_path"]}'
    # main_extension_py_args = \
    #     f'{args.test_duration} {args.output_stats_frequency} {args.traffic_intensity} ' + \
    #     f'{calculated_args["topo_file"]} {calculated_args["test_file_path"]} ' + \
    #     f'{calculated_args["raw_file_path"]} {calculated_args["decoded_file_path"]}'
    
    # subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    # ppprint([
    #     'tmux', 'send-keys', '-t', 'onos_session:0', 
    #     f"cd {cwd} && python3 main.py {main_py_args} && python3 main_extension.py {main_extension_py_args}", 
    #     'C-m'
    # ])
    # time.sleep(4)

    # Window 2: Controller
    ppprint("Window 2: Starting controller...")
    # subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:1', f'cd {cwd} && make controller', 'C-m'])
    # time.sleep(55)

    # Window 3: Mininet
    ppprint("Window 3: Starting Mininet...")
    # subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:2',
        f'cd {cwd} && make mininet MN_STRATUM_TOPO_FILE={calculated_args["mn_stratum_topo_file"]}', 'C-m'
    ])
    # time.sleep(10)

    # Window 4: ONOS CLI
    ppprint("Window 4: Starting ONOS CLI...")
    # subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:3', f'cd {cwd} && make cli', 'C-m'])
    # time.sleep(5)
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:3', 'rocks', 'C-m'])
    # time.sleep(5)

    # Window 5: NetCFG
    ppprint("Window 5: Configuring network...")
    # subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:4',
        f'cd {cwd} && make netcfg ONOS_CONFIG_FILE={calculated_args["onos_config_file"]}', 'C-m'
    ])
    # time.sleep(5)

    # Activate fwd
    ppprint("Activating forwarding...")
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:3', 'app activate fwd', 'C-m'])
    # time.sleep(2)

    # Run pingall twice
    ppprint("Running first pingall...")
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    # time.sleep(10)
    ppprint("Running second pingall...")
    ppprint(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
    # time.sleep(10)

    # Check if mininet CLI is ready
    if True:
        ppprint("Mininet CLI is ready!")
        success = True

        # Continue with test execution
        ppprint("Running tests...")
        ppprint(['tmux', 'send-keys', '-t', 'onos_session:2',
            f'py execfile(\'{calculated_args["test_file"]}\')', 'C-m'
        ])
        # time.sleep(3)
        ppprint(['tmux', 'send-keys', '-t', 'onos_session:2', 'py run_tests(net)', 'C-m'])
        # time.sleep(200)
    else:
        ppprint("Mininet CLI not ready, will retry...")
        # continue



def run_setup(args, calculated_args, run_number, max_attempts=5):
    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        attempt += 1
        print(f"\nAttempt {attempt} of {max_attempts}")

        # Clean up before each attempt (including first one to ensure clean state)
        cleanup()

        # try:
        # Create new tmux session
        print("Create new tmux session")
        subprocess.run(['tmux', 'new-session', '-d', '-s', 'onos_session'])
        cwd = os.getcwd()

        # Rest of your window creation and setup code...
        # Window 1: Generate network config and test script
        # print("Window 1: Creating configuration files...")

        # main_py_args = \
        #     f'{args.num_nodes} {args.connectivity_type} {calculated_args["topo_file_path"]} ' + \
        #     f'{calculated_args["onos_config_file_path"]} {calculated_args["mininet_config_file_path"]} ' + \
        #     f'{calculated_args["hops_script_file_path"]}'

        # main_extension_py_args = \
        #     f'{args.test_duration} {args.output_stats_frequency} {args.traffic_intensity} ' + \
        #     f'{calculated_args["topo_file"]} {calculated_args["test_file_path"]} ' + \
        #     f'{calculated_args["raw_file_path"]} {calculated_args["decoded_file_path"]}'
        
        subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
        # subprocess.run([
        #     'tmux', 'send-keys', '-t', 'onos_session:0', 
        #     f"cd {cwd} && python3 main_extension.py {main_extension_py_args}", 
        #     'C-m'
        # ])

        # Window 2: Controller
        print("Window 2: Starting controller...")
        subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', f'cd {cwd} && make controller', 'C-m'])
        time.sleep(55)

        # Window 3: Mininet
        print("Window 3: Starting Mininet...")
        subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', \
            f'cd {cwd} && make mininet MN_STRATUM_TOPO_FILE={calculated_args["mn_stratum_topo_file"]}', 'C-m'
        ])
        time.sleep(10)

        # Window 4: ONOS CLI
        print("Window 4: Starting ONOS CLI...")
        subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', f'cd {cwd} && make cli', 'C-m'])
        time.sleep(5)
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 'rocks', 'C-m'])
        time.sleep(5)

        # Window 5: NetCFG
        print("Window 5: Configuring network...")
        subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', \
            f'cd {cwd} && make netcfg ONOS_CONFIG_FILE={calculated_args["onos_config_file"]}', 'C-m'
        ])
        time.sleep(5)

        # Activate fwd
        print("Activating forwarding...")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:3', 'app activate fwd', 'C-m'])
        time.sleep(2)

        # Run pingall twice
        print("Running first pingall...")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
        time.sleep(10)
        print("Running second pingall...")
        subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'pingall', 'C-m'])
        time.sleep(10)

        # Check if mininet CLI is ready
        if check_mininet_cli_ready():
            print("Mininet CLI is ready!")
            success = True

            if run_number == 1:

                # Window 6: Handle get_hops script
                print("Window 6: Handle get_hops script")
                subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
                
                # Make the script executable
                print("Make the get_hops.sh executable")
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:5', 
                                'chmod', '+x', calculated_args["hops_script"], 'C-m'])
                
                # Copy and execute get_hops script
                print("Copy and execute get_hops script")
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:5', 
                            f'docker cp {calculated_args["hops_script"]} onos:/root/onos/get_hops.sh', 'C-m'])
                time.sleep(1)
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:5', 
                            'docker exec onos chmod +x /root/onos/get_hops.sh', 'C-m'])
                time.sleep(1)
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:5', 
                            'docker exec onos /root/onos/get_hops.sh', 'C-m'])
                time.sleep(2)
                
                # Copy results back
                print("Copy results back")
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:5', 
                        f'docker cp onos:/root/onos/paths.txt {calculated_args["hops_script_output_file"]}', 'C-m'])
                time.sleep(2)

                # get the port matrix from the output of the get_hops script
                print("get the port matrix from the output of the get_hops script")

                get_port_matrix_args = f'{calculated_args["topo_file"]} ' + \
                        f'{calculated_args["hops_script_output_file"]} {calculated_args["port_matrix_file_path"]}'
                
                subprocess.run([
                    'tmux', 'send-keys', '-t', 'onos_session:0',
                    f'python3 get_port_matrix.py {get_port_matrix_args}', 'C-m'])

            # Continue with test execution
            print("Running tests...")
            subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', \
                f'py execfile(\'{calculated_args["test_file"]}\')', 'C-m'
            ])
            time.sleep(1)
            subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'py run_tests(net)', 'C-m'])
            time.sleep(args.test_duration * 1.7)
        else:
            print("Mininet CLI not ready, will retry...")
            continue

        # except Exception as e:
        #     print(f"Error during setup: {e}")
        #     if attempt < max_attempts:
        #         print("Will retry after cleanup...")
        #         continue

    if not success:
        print(f"Failed to set up network after {max_attempts} attempts")
        return False

    # Attach to the tmux session
    # subprocess.run(['tmux', 'attach-session', '-t', 'onos_session'])
    return True

if __name__ == "__main__":
    args = getCommandLineArgs()
    runner(args)