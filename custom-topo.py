from mininet.topo import Topo
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
import time
import os

class customtopo(Topo):
	def build(self):
		# START build
		s0 = self.addSwitch('s0')
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		
		h0 = self.addHost('h0')
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		
		self.addLink(s3, h2, bw=0.04)
		self.addLink(s3, h3, bw=0.1)
		self.addLink(s0, s2, bw=0.01)
		self.addLink(s2, s3, bw=0.04)
		self.addLink(s1, h1, bw=0.04)
		self.addLink(s1, s2, bw=0.1)
		self.addLink(s1, h0, bw=0.01)
		self.addLink(s0, s1, bw=0.04)
		self.addLink(s0, s3, bw=0.1)
		# END build

# Keep this for compatibility with --custom flag
topos = { 'customtopo': ( lambda: customtopo() ) }