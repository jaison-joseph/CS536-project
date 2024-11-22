from mininet.net import Mininet
import time
import os

def run_iperf_test(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    
    # Start iperf server on h1
    h1.cmd('iperf3 -s &')
    time.sleep(2)  # Wait for server to start
    
    # Run client on h2 and capture output
    h2.cmd('iperf3 -c h1 -u -l 1000 -t 15 -i 1 > dump.txt')
    
    h1.cmd('killall iperf3')

# To use this in Mininet CLI:
# mininet> py execfile('hello.py')
# mininet> py run_iperf_test(net)