import networkx as nx
import random
import matplotlib.pyplot as plt
import os
import json
import argparse
from random import choice

from main_extension import *

# for the network topology, these are the link options inMbps
bandwidth_options = [0.01, 0.04, 0.1]

bandwidths = []

def create_backbone_network(num_switches, num_hosts, connectivity_type='nsfnet'):
    """
    Create a backbone network topology.
    
    Args:
        num_switches: Number of switches in backbone
        num_hosts: Number of hosts to connect to switches
        connectivity_type: Type of backbone connectivity 
            - 'nsfnet': Sparse connectivity like NSF network
            - 'geant2': Medium connectivity like GEANT2
            - 'germany50': Dense connectivity like Germany50
    
    Returns:
        G: NetworkX graph representing the topology
    """
    # Create empty graph
    G = nx.Graph()
    
    # Add switches (labeled s0, s1, etc)
    switches = [f's{i}' for i in range(num_switches)]
    G.add_nodes_from(switches)
    
    # Add hosts (labeled h0, h1, etc)
    hosts = [f'h{i}' for i in range(num_hosts)]
    G.add_nodes_from(hosts)
    
    # Create backbone connectivity between switches based on type
    if connectivity_type == 'nsfnet':
        # Sparse connectivity (~2-3 connections per switch)
        # First create a ring topology to ensure connectivity
        for i in range(num_switches):
            G.add_edge(f's{i}', f's{(i+1)%num_switches}')
        # Add some random additional links
        extra_links = num_switches // 2
        while extra_links > 1:
            s1 = random.choice(switches)
            s2 = random.choice(switches)
            if s1 != s2 and not G.has_edge(s1, s2):
                G.add_edge(s1, s2)
                extra_links -= 1
                
    elif connectivity_type == 'geant2':
        # Medium connectivity (~3-4 connections per switch)
        # Create base mesh
        for i in range(num_switches):
            for j in range(i+1, min(i+4, num_switches)):
                G.add_edge(f's{i}', f's{j}')
        # Add some random additional links
        extra_links = num_switches
        while extra_links > 1:
            s1 = random.choice(switches)
            s2 = random.choice(switches)
            if s1 != s2 and not G.has_edge(s1, s2):
                G.add_edge(s1, s2)
                extra_links -= 1
                
    elif connectivity_type == 'germany50':
        # Dense connectivity (~4-5 connections per switch)
        # Create initial mesh
        for i in range(num_switches):
            for j in range(i+1, min(i+5, num_switches)):
                G.add_edge(f's{i}', f's{j}')
        # Add random additional links
        extra_links = num_switches * 2
        while extra_links > 1:
            s1 = random.choice(switches)
            s2 = random.choice(switches)
            if s1 != s2 and not G.has_edge(s1, s2):
                G.add_edge(s1, s2)
                extra_links -= 1
    
    # Connect hosts to switches
    # Each host connects to one switch
    for i, host in enumerate(hosts):
        # Connect to random switch
        switch = random.choice(switches)
        G.add_edge(host, switch)
    
    return G

def draw(G_nsf: nx.classes.graph.Graph):
    plt.figure(figsize=(12,8))
    pos = nx.spring_layout(G_nsf)
    nx.draw(G_nsf, pos, with_labels=True, 
            node_color=['lightblue' if node.startswith('s') else 'lightgreen' for node in G_nsf.nodes()],
            node_size=500)
    plt.title("NSF-like Network Topology")
    plt.show()

# Example usage:
def default_usage():
    # Create NSF-like network (14 switches)
    G_nsf = create_backbone_network(14, 10, 'nsfnet')
    print("NSF-like network:")
    print(f"Nodes: {G_nsf.number_of_nodes()}")
    print(f"Edges: {G_nsf.number_of_edges()}")
    
    # Create GEANT2-like network (24 switches)
    G_geant = create_backbone_network(24, 20, 'geant2')
    print("\nGEANT2-like network:")
    print(f"Nodes: {G_geant.number_of_nodes()}")
    print(f"Edges: {G_geant.number_of_edges()}")
    
    # Create Germany50-like network (50 switches)
    G_germany = create_backbone_network(50, 40, 'germany50')
    print("\nGermany50-like network:")
    print(f"Nodes: {G_germany.number_of_nodes()}")
    print(f"Edges: {G_germany.number_of_edges()}")
    
    # Visualize one of the networks
    plt.figure(figsize=(12,8))
    pos = nx.spring_layout(G_nsf)
    nx.draw(G_nsf, pos, with_labels=True, 
            node_color=['lightblue' if node.startswith('s') else 'lightgreen' for node in G_nsf.nodes()],
            node_size=500)
    plt.title("NSF-like Network Topology")
    plt.show()

def foo():
    # Create NSF-like network (14 switches)
    G_nsf = create_backbone_network(6, 6, 'nsfnet')
    print(type(G_nsf))
    print("NSF-like network:")
    print(f"Nodes: {G_nsf.number_of_nodes()}")
    print(f"Edges: {G_nsf.number_of_edges()}")
    
    # Create GEANT2-like network (24 switches)
    G_geant = create_backbone_network(24, 20, 'geant2')
    print("\nGEANT2-like network:")
    print(f"Nodes: {G_geant.number_of_nodes()}")
    print(f"Edges: {G_geant.number_of_edges()}")
    
    # Create Germany50-like network (50 switches)
    G_germany = create_backbone_network(50, 40, 'germany50')
    print("\nGermany50-like network:")
    print(f"Nodes: {G_germany.number_of_nodes()}")
    print(f"Edges: {G_germany.number_of_edges()}")

    # draw(G_nsf)
    print(list(G_nsf.nodes()))
    print(list(G_nsf.edges()))

def generateTopologyJson(num_switches: int, num_hosts: int, ):

    assert len(bandwidths) > 0, "please call call_mininet_generator before calling generateTopologyJson"
    
    # Create the topology dictionary
    topology = {
        "number_hosts": num_hosts,
        "number_switches": num_switches,
        "network_edges": bandwidths
    }
    
    # Ensure cfg directory exists
    os.makedirs("cfg", exist_ok=True)
    
    # Save to JSON file
    with open("cfg/topo.json", "w") as f:
        json.dump(topology, f, indent=2)

def generate_ONOS_config(num_switches: int):
    devices = {}
    
    for i in range(1, num_switches + 1):
        device_key = f"device:s{i - 1}"
        devices[device_key] = {
            "basic": {
                "managementAddress": f"grpc://127.0.0.1:{50000 + i}?device_id=1",
                "driver": "stratum-bmv2",
                "pipeconf": "org.onosproject.pipelines.basic"
            }
        }
    
    config = {
        "devices": devices
    }
    
    # Ensure cfg directory exists
    os.makedirs("cfg", exist_ok=True)
    
    # Save to JSON file
    with open("cfg/onos_config.json", "w") as f:
        json.dump(config, f, indent=2)

def call_mininet_generator(num_switches: int, num_hosts: int, G: nx.classes.graph.Graph, fileName = 'custom-topo.py'):
    
    setNumberOfHosts(num_hosts)
    setNumberOfSwitches(num_switches)

    for x, y in G.edges():
        t1 = x[0]
        v1 = x[1:]
        t2 = y[0]
        v2 = y[1:]
        bw = choice(bandwidth_options)
        addLink(t1, int(v1), t2, int(v2), bw)
        bandwidths.append([x, y, bw])

    generateMininetTopologyFile()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate network topology and ONOS configuration')
    
    # Add arguments
    parser.add_argument('num_hosts', type=int, help='Number of hosts')
    parser.add_argument('num_switches', type=int, help='Number of switches')
    parser.add_argument('connectivity_type', type=str, choices=['nsfnet', 'geant2', 'germany50'],
                        help='Type of network connectivity (nsfnet, geant2, or germany50)')
    parser.add_argument('-v', '--visualize', action='store_true', help='visualize the network topology.')
    
    # Parse arguments
    args = parser.parse_args()

	# Generate the network
    G = create_backbone_network(args.num_switches, args.num_hosts, args.connectivity_type)
    
    # generate mininet topology file
    call_mininet_generator(args.num_switches, args.num_hosts, G, 'custom-topo.py')

    # Generate topology and ONOS config
    generateTopologyJson(args.num_switches, args.num_hosts)
    generate_ONOS_config(args.num_switches)
    
    print(f"Generated topology with {args.num_hosts} hosts and {args.num_switches} switches using {args.connectivity_type} connectivity")
    print("Files created: cfg/topo.json, cfg/onos_config.json, 'custom-topo.py")

    if args.visualize:
        draw(G)

def debug():
    # Generate topology and ONOS config
    num_switches = 6
    num_hosts = 6
    connectivity_type = 'nsfnet'
    G = generateTopologyJson(num_switches, num_hosts, connectivity_type)
    generate_ONOS_config(num_switches)

    # generate mininet topology file
    call_mininet_generator(num_switches, num_hosts, G, 'custom-topo.py')
    
    print(f"Generated topology with {num_hosts} hosts and {num_switches} switches using {connectivity_type} connectivity")
    print("Files created: cfg/topo.json, cfg/onos_config.json, 'custom-topo.py")


if __name__ == "__main__":
    main()
    # debug()