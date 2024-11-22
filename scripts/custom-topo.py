from mininet.topo import Topo
from mininet.link import TCLink

class customtopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        
        # Add links with specific bandwidth (in Mbps)
        self.addLink(h1, s1, bw=10)
        self.addLink(s1, s2, bw=5)
        self.addLink(s2, h2, bw=10)