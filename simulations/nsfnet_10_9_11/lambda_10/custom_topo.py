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
		s0 = self.addSwitch('s0', dpid='0000000000000001', cls=OVSSwitch)
		s1 = self.addSwitch('s1', dpid='0000000000000002', cls=OVSSwitch)
		s2 = self.addSwitch('s2', dpid='0000000000000003', cls=OVSSwitch)
		s3 = self.addSwitch('s3', dpid='0000000000000004', cls=OVSSwitch)
		s4 = self.addSwitch('s4', dpid='0000000000000005', cls=OVSSwitch)
		s5 = self.addSwitch('s5', dpid='0000000000000006', cls=OVSSwitch)
		s6 = self.addSwitch('s6', dpid='0000000000000007', cls=OVSSwitch)
		s7 = self.addSwitch('s7', dpid='0000000000000008', cls=OVSSwitch)
		s8 = self.addSwitch('s8', dpid='0000000000000009', cls=OVSSwitch)
		s9 = self.addSwitch('s9', dpid='000000000000000a', cls=OVSSwitch)
		
		h0 = self.addHost('h0')
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')
		h5 = self.addHost('h5')
		h6 = self.addHost('h6')
		h7 = self.addHost('h7')
		h8 = self.addHost('h8')
		h9 = self.addHost('h9')
		
		self.addLink(s4, h4, bw=10)
		self.addLink(s9, h9, bw=10)
		self.addLink(s5, h5, bw=10)
		self.addLink(s8, h8, bw=10)
		self.addLink(s1, h1, bw=10)
		self.addLink(s0, h0, bw=10)
		self.addLink(s6, h6, bw=10)
		self.addLink(s2, h2, bw=10)
		self.addLink(s7, h7, bw=10)
		self.addLink(s3, h3, bw=10)
		self.addLink(s4, s9, bw=0.04, max_queue_size=32)
		self.addLink(s1, s2, bw=0.01, max_queue_size=32)
		self.addLink(s2, s4, bw=0.1, max_queue_size=32)
		self.addLink(s0, s1, bw=0.04, max_queue_size=32)
		self.addLink(s7, s8, bw=0.01, max_queue_size=32)
		self.addLink(s8, s9, bw=0.01, max_queue_size=32)
		self.addLink(s3, s4, bw=0.1, max_queue_size=32)
		self.addLink(s4, s7, bw=0.01, max_queue_size=32)
		self.addLink(s4, s5, bw=0.1, max_queue_size=32)
		self.addLink(s2, s8, bw=0.04, max_queue_size=32)
		self.addLink(s0, s9, bw=0.1, max_queue_size=32)
		self.addLink(s5, s6, bw=0.1, max_queue_size=32)
		self.addLink(s2, s3, bw=0.1, max_queue_size=32)
		self.addLink(s6, s7, bw=0.01, max_queue_size=32)
		# END build

# Keep this for compatibility with --custom flag
topos = { 'customtopo': ( lambda: customtopo() ) }