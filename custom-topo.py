from mininet.topo import Topo
from mininet.link import TCLink

class customtopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        
        # Add links with specific bandwidth (in Mbps)
		# I think that because we specify explicit bandwidths here, we need to specify these ports in netcfg.json, config is used by ONOS
        # Add links without 'bw' parameters
		# might need a max_queue_size=32 option to each addLink because this is set in the paper
        self.addLink(s1, s2, bw=10)
        self.addLink(s1, s3, bw=15)
        self.addLink(s2, s4, bw=20)
        self.addLink(s3, s4, bw=5)

        # Connect hosts to switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

# Add this line at the end of the file
topos = { 'customtopo': ( lambda: customtopo() ) }