from mininet.topo import Topo
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import setLogLevel
import time
import os

class customtopo(Topo):
    def build(self):
        # Your existing topology code here
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        
        self.addLink(s1, s2, bw=10)
        self.addLink(s1, s3, bw=15)
        self.addLink(s2, s4, bw=20)
        self.addLink(s3, s4, bw=5)

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

# START run_tests

def run_tests(net):
	from datetime import datetime
	# Create logs directory if it doesn't exist
	if not os.path.exists('logs'):
		os.makedirs('logs')

	# Get current timestamp for log files
	timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')


	# Get host objects
	h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

	try:       
        # start iperf servers
        h2.cmd('iperf3 -s &')
        h3.cmd('iperf3 -s &')
        
        # wait for servers to start
        time.sleep(2)
        
        # run iperf clients
        h2.cmd('iperf3 -c h3 -u -l 1000 -t 15 -i 1 > logs/2024-11-21-00:00:58.422208_4_4_2_3.txt')
        h1.cmd('iperf3 -c h2 -u -l 1000 -t 15 -i 1 > logs/2024-11-21-00:00:58.422208_4_4_1_2.txt')
        h4.cmd('iperf3 -c h3 -u -l 1000 -t 15 -i 1 > logs/2024-11-21-00:00:58.422208_4_4_4_3.txt')
        
        # wait for iperf clients to finish
        time.sleep(15)
        
        # Kill iperf servers
        h2.cmd('killall iperf3')
        h3.cmd('killall iperf3')
        
    except Exception as e:
        print(e)

# END run_tests

if __name__ == '__main__':
    setLogLevel('info')
    run_tests()

# Keep this for compatibility with --custom flag
topos = { 'customtopo': ( lambda: customtopo() ) }