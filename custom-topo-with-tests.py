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
        
        # self.addLink(s1, s2, bw=10)
        # self.addLink(s1, s3, bw=15)
        # self.addLink(s2, s4, bw=20)
        # self.addLink(s3, s4, bw=5)
        self.addLink(s1, s2, bw=5)
        self.addLink(s1, s3, bw=5)
        self.addLink(s2, s4, bw=5)
        self.addLink(s3, s4, bw=5)

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

# START run_tests

# END run_tests

# Keep this for compatibility with --custom flag
topos = { 'customtopo': ( lambda: customtopo() ) }