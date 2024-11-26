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

def run_setup(args, max_attempts=5):
    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        attempt += 1
        print(f"\nAttempt {attempt} of {max_attempts}")

        # Clean up before each attempt (including first one to ensure clean state)
        cleanup()

        try:
            # Create new tmux session
            print("Create new tmux session")
            subprocess.run(['tmux', 'new-session', '-d', '-s', 'onos_session'])
            cwd = os.getcwd()

            # Rest of your window creation and setup code...
            # Window 1: Generate network config and test script
            print("Window 1: Creating configuration files...")
            subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
            subprocess.run([
                'tmux', 'send-keys', '-t', 'onos_session:0', 
                f"cd {cwd} && python3 main.py {args.num_switches} {args.num_hosts} {args.connectivity_type} && python3 main_extension.py", 
                'C-m'
            ])
            time.sleep(4)

            # Window 2: Controller
            print("Window 2: Starting controller...")
            subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
            subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:1', f'cd {cwd} && make controller', 'C-m'])
            time.sleep(55)

            # Window 3: Mininet
            print("Window 3: Starting Mininet...")
            subprocess.run(['tmux', 'new-window', '-t', 'onos_session'])
            subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', f'cd {cwd} && make mininet', 'C-m'])
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
            subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:4', f'cd {cwd} && make netcfg', 'C-m'])
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

                # Continue with test execution
                print("Running tests...")
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'py execfile(\'test.py\')', 'C-m'])
                time.sleep(3)
                subprocess.run(['tmux', 'send-keys', '-t', 'onos_session:2', 'py run_tests(net)', 'C-m'])
                time.sleep(200)
            else:
                print("Mininet CLI not ready, will retry...")
                continue

        except Exception as e:
            print(f"Error during setup: {e}")
            if attempt < max_attempts:
                print("Will retry after cleanup...")
                continue

    if not success:
        print(f"Failed to set up network after {max_attempts} attempts")
        return False

    # Attach to the tmux session
    subprocess.run(['tmux', 'attach-session', '-t', 'onos_session'])
    return True

if __name__ == "__main__":
    args = getCommandLineArgs()
    run_setup(args, 7)