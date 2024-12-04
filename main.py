import networkx as nx
import random
import os
import json
import argparse
from random import choice
from itertools import combinations

from main_extension import *

# for the network topology, these are the link options inMbps
bandwidth_options = [0.01, 0.04, 0.1]

bandwidths = []

onosConfigFileName = "onos_config.json"
topoFileName = "topo.json"
mininetConfigFileName = "custom_topo.py"
hopsScriptFileName = 'get_hops.sh'
sortedLinksFileName = 'sorted_links.txt'
hopsScriptOutputFileName = 'paths.txt'

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='Generate network topology and ONOS configuration')
    
    # Add arguments
    
    parser.add_argument('num_nodes', type=int, help='Number of nodes (switches and hosts both)')
    
    parser.add_argument('connectivity_type', type=str, choices=['nsfnet', 'geant2', 'germany50'],
                        help='Type of network connectivity (nsfnet, geant2, or germany50)')
    
    parser.add_argument('topo_file_path', type=str,
                        help=f'path where the topology file {topoFileName} should be written to')
    
    parser.add_argument('onos_config_file_path', type=str,
                        help=f'path where the ONOS config file {onosConfigFileName} should be written to')
    
    parser.add_argument('mininet_config_file_path', type=str,
                        help=f'path where the mininet config file {mininetConfigFileName} should be written to')

    # not needed since we don't generate this script anymore
    parser.add_argument('hops_script_file_path', type=str, 
                        help=f'where the hops script {hopsScriptFileName} should be outputted to')
    
    parser.add_argument('-v', '--visualize', action='store_true', help='visualize the network topology.')
    
    # Parse arguments
    args = parser.parse_args()

    return args

def newNetworkGen(G: nx.classes.graph.Graph, hosts: list, switches: list):
    # divide into sub-networks of hosts
    buckets = [switches[i:i+4] for i in range(0, len(switches), 3)]
    # for each bucket, ensure it is connected
    for b in buckets:
        countdown = max(len(b) - 1, 1)
        visited = set()
        for x, y in combinations(b, 2):
            if x not in visited or y not in visited:
                visited.add(x)
                visited.add(y)
                G.add_edge(x, y)
                countdown -= 1
                if countdown <= 0:
                    break
    # ensure the buckets are connected
    countdown = max(len(buckets) - 3, 1) # tweak me (- 2)
    lk = {i: b for i, b in enumerate(buckets)}
    countdown = max(len(b) - 1, 1)
    visited = set()
    for x, y in combinations(list(lk.keys()), 2):
        if x not in visited or y not in visited:
            visited.add(x)
            visited.add(y)
            G.add_edge(random.choice(lk[x]), random.choice(lk[y]))

    for _ in range(2):
        #  get switches that have <= 1 switch neighbor
        singles = [node for node in switches if len(list(G.neighbors(node))) <= 1]

        # pair up singles
        for i in range(len(singles)//2):
            s1 = random.choice(singles)
            singles.remove(s1)
            s2 = random.choice(singles)
            singles.remove(s2)
            G.add_edge(s1, s2)
        
        # if there's an odd one out 
        for s in singles:
            connectionOptions = set(switches) - set(list(G.neighbors(s))) - set([s])
            print(f"connection options for {s} are: {connectionOptions}")
            G.add_edge(s, random.choice(list(connectionOptions)))

def create_backbone_network(num_nodes, connectivity_type='nsfnet'):
    """
    Create a backbone network topology.
    
    Args:
        num_nodes: Number of switches & hots in backbone (we treat a combination of a switch and host as a 'node' in our mininet + ONOS setup)
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
    switches = [f's{i}' for i in range(num_nodes)]
    G.add_nodes_from(switches)
    
    # Add hosts (labeled h0, h1, etc)
    hosts = [f'h{i}' for i in range(num_nodes)]
    G.add_nodes_from(hosts)
    
    # Create backbone connectivity between switches based on type
    if connectivity_type == 'nsfnet':
        if len(hosts) > 10:
            newNetworkGen(G, hosts, switches)
        else:
            # Sparse connectivity (~2-3 connections per switch)
            # First create a ring topology to ensure connectivity
            for i in range(num_nodes):
                G.add_edge(f's{i}', f's{(i+1)%num_nodes}')
            # Add some random additional links
            extra_links = num_nodes // 2
            while extra_links > 1:
                s1 = random.choice(switches)
                s2 = random.choice(switches)
                if s1 != s2 and not G.has_edge(s1, s2):
                    G.add_edge(s1, s2)
                    extra_links -= 1
                
    elif connectivity_type == 'geant2':
        # Medium connectivity (~3-4 connections per switch)
        # Create base mesh
        for i in range(num_nodes):
            for j in range(i+1, min(i+4, num_nodes)):
                G.add_edge(f's{i}', f's{j}')
        # Add some random additional links
        extra_links = num_nodes
        while extra_links > 1:
            s1 = random.choice(switches)
            s2 = random.choice(switches)
            if s1 != s2 and not G.has_edge(s1, s2):
                G.add_edge(s1, s2)
                extra_links -= 1
                
    elif connectivity_type == 'germany50':
        # Dense connectivity (~4-5 connections per switch)
        # Create initial mesh
        for i in range(num_nodes):
            for j in range(i+1, min(i+5, num_nodes)):
                G.add_edge(f's{i}', f's{j}')
        # Add random additional links
        extra_links = num_nodes * 2
        while extra_links > 1:
            s1 = random.choice(switches)
            s2 = random.choice(switches)
            if s1 != s2 and not G.has_edge(s1, s2):
                G.add_edge(s1, s2)
                extra_links -= 1
    
    # Connect hosts to switches
    # Each host connects to one switch
    for host, switch in zip(hosts, switches):
        G.add_edge(host, switch)
    
    return G

def generate_get_hops_script(num_switches: int, hopsScriptFilePath: str):
    fullFileName = os.path.join(hopsScriptFilePath, hopsScriptFileName)
    with open(fullFileName, 'w+') as f:
        f.write("#!/bin/bash\n\n")
        for s in range(num_switches):
            others = set(range(num_switches))
            others.remove(s)
            for o in others:
                # curl -X GET http://localhost:8181/onos/v1/paths/of:0000000000000001/of:000000000000000a -u onos:rocks
                # op = f'echo "(s{s}, s{o}): $(curl -X GET http://localhost:8181/onos/v1/paths/device:s{s}/device:s{o} -u onos:rocks)" >> {hopsScriptOutputFileName}'
                op = f'echo "(s{s}, s{o}): $(curl -X GET http://localhost:8181/onos/v1/paths/{generate_openflow_id(16, s+1)}/{generate_openflow_id(16, o+1)} -u onos:rocks)" >> {hopsScriptOutputFileName}'
                f.write(op)
                f.write('\n')
                # f.write("echo >> paths.txt\n")


# Example usage:
def default_usage():
    # Create NSF-like network (14 nodes)
    G_nsf = create_backbone_network(14, 'nsfnet')
    print("NSF-like network:")
    print(f"Nodes: {G_nsf.number_of_nodes()}")
    print(f"Edges: {G_nsf.number_of_edges()}")
    
    # Create GEANT2-like network (24 nodes)
    G_geant = create_backbone_network(24, 'geant2')
    print("\nGEANT2-like network:")
    print(f"Nodes: {G_geant.number_of_nodes()}")
    print(f"Edges: {G_geant.number_of_edges()}")
    
    # Create Germany50-like network (50 nodes)
    G_germany = create_backbone_network(50, 'germany50')
    print("\nGermany50-like network:")
    print(f"Nodes: {G_germany.number_of_nodes()}")
    print(f"Edges: {G_germany.number_of_edges()}")
    

def foo():
    # Create NSF-like network (14 switches)
    G_nsf = create_backbone_network(14, 'nsfnet')
    print(type(G_nsf))
    print("NSF-like network:")
    print(f"Nodes: {G_nsf.number_of_nodes()}")
    print(f"Edges: {G_nsf.number_of_edges()}")
    
    # Create GEANT2-like network (24 switches)
    G_geant = create_backbone_network(24, 'geant2')
    print("\nGEANT2-like network:")
    print(f"Nodes: {G_geant.number_of_nodes()}")
    print(f"Edges: {G_geant.number_of_edges()}")
    
    # Create Germany50-like network (50 switches)
    G_germany = create_backbone_network(50, 'germany50')
    print("\nGermany50-like network:")
    print(f"Nodes: {G_germany.number_of_nodes()}")
    print(f"Edges: {G_germany.number_of_edges()}")

    # draw(G_nsf)
    print(list(G_nsf.nodes()))
    print(list(G_nsf.edges()))

def generateTopologyFile(num_nodes: int, outputTopoFilePath: str):

    assert len(bandwidths) > 0, "please call call_mininet_generator before calling generateTopologyFile"
    
    # Create the topology dictionary
    topology = {
        "number_hosts": num_nodes,
        "number_switches": num_nodes,
        "network_edges": bandwidths
    }
    
    # Ensure cfg directory exists
    os.makedirs("cfg", exist_ok=True)
    
    # Save to JSON file
    outputFileName = os.path.join(outputTopoFilePath, topoFileName)
    with open(outputFileName, "w") as f:
        json.dump(topology, f, indent=2)

def generate_ONOS_config(num_nodes: int, onosConfigFilePath: str):
    devices = {}
    
    for i in range(1, num_nodes + 1):
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
    
    # Save to JSON file

    onosFullFileName = os.path.join(onosConfigFilePath, onosConfigFileName)
    with open(onosFullFileName, "w") as f:
        json.dump(config, f, indent=2)

def call_mininet_generator(num_nodes: int, G: nx.classes.graph.Graph, mininetConfigFilePath: str, host_to_switch_bandwidth = 10):
    
    setNumberOfHosts(num_nodes)
    setNumberOfSwitches(num_nodes)

    for x, y in G.edges():
        t1 = x[0]
        v1 = x[1:]
        t2 = y[0]
        v2 = y[1:]
        if t1 == t2 == 's':
            bw = choice(bandwidth_options)
        else:
            bw = host_to_switch_bandwidth
        addLink(t1, int(v1), t2, int(v2), bw)
        bandwidths.append([x, y, bw])

    outputFileName = os.path.join(mininetConfigFilePath, mininetConfigFileName)

    # note that the logic to limit queue size is in the definition of  generateMininetTopologyFile
    sortedLinks = generateMininetTopologyFile(outputFileName) 

    with open(os.path.join(mininetConfigFilePath, sortedLinksFileName), 'w+') as f:
        for l in sortedLinks:
            f.write(str(l))
            f.write('\n')

def draw(G_nsf: nx.classes.graph.Graph):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,8))
    pos = nx.spring_layout(G_nsf)
    nx.draw(G_nsf, pos, with_labels=True, 
            node_color=['lightblue' if node.startswith('s') else 'lightgreen' for node in G_nsf.nodes()],
            node_size=500)
    plt.title("NSF-like Network Topology")
    plt.show()

def main():
    print("main from main called")
    # Set up argument parser
    args = getCommandLineArgs()

    # Generate the network
    G = create_backbone_network(args.num_nodes, args.connectivity_type)
    
    # generate mininet topology file
    # call_mininet_generator(num_nodes: int, G: nx.classes.graph.Graph, outputFilePath: str, host_to_switch_bandwidth = 10)
    call_mininet_generator(args.num_nodes, G, args.mininet_config_file_path)

    # Generate topology and ONOS config
    generateTopologyFile(args.num_nodes, args.topo_file_path)
    generate_ONOS_config(args.num_nodes, args.onos_config_file_path)

    # with openflow and OVS switches, we just get all the flows
    generate_get_hops_script(args.num_nodes, args.hops_script_file_path)
    
    print(f"Generated topology with {args.num_nodes} hosts and {args.num_nodes} switches using {args.connectivity_type} connectivity")
    finalTopoFileName = os.path.join(args.topo_file_path, topoFileName)
    finalOnosConfigFileName = os.path.join(args.onos_config_file_path, onosConfigFileName)
    finalMininetConfigFileName = os.path.join(args.mininet_config_file_path, mininetConfigFileName)
    print(f"Files created: {finalTopoFileName}, {finalOnosConfigFileName}, {finalMininetConfigFileName}")

    if args.visualize:
        draw(G)

def debug():
    # Generate topology and ONOS config
    num_nodes = 6
    connectivity_type = 'nsfnet'
    G = create_backbone_network(num_nodes, connectivity_type)
    
    # generate ONOS config file
    generate_ONOS_config(num_nodes, 'cfg')

    # generate mininet topology file
    call_mininet_generator(num_nodes, G, '')

    # generate the config json file
    generateTopologyFile(args.num_nodes, 'cfg')
    
    print(f"Generated topology with {num_nodes} hosts and {num_nodes} switches using {connectivity_type} connectivity")
    print("Files created: cfg/topo.json, cfg/onos_config.json, 'custom-topo.py")


if __name__ == "__main__":
    main()
    # debug()