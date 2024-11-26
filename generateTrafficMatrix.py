import json
from sys import maxsize

gatewaySwitchLk = {}
bandwidthLk = {}
hopsLk = {}

def read_topo_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        
    num_hosts = data['number_hosts']
    num_switches = data['number_switches']
    network_edges = data['network_edges']
    
    return num_hosts, num_switches, network_edges

'''
[
    ('s0', 's3'), 
    [
        [('s0', 's1'), ('s1', 's3')], 
        [('s0', 's2'), ('s2', 's3')]
    ]
]
'''
def read_hops_txt(filename):
    content = open(filename, 'r').read()
    # Split content into lines and process each line
    paths = {}
    
    for line in content.strip().split('\n'):
        # Extract source-destination pair and json data
        pair_str, json_str = line.split(': ', 1)
        src, dst = pair_str.strip('()').split(', ')
        
        # Parse JSON data
        data = json.loads(json_str)
        
        # Extract hops for all paths between this pair
        path_hops = []
        for path in data['paths']:
            hops = []
            for link in path['links']:
                # Extract source and destination devices
                src_device = link['src']['device'].replace('device:', '')
                dst_device = link['dst']['device'].replace('device:', '')
                hops.append((src_device, dst_device))
            path_hops.append(hops)
            
        # Store in dictionary
        paths[(src, dst)] = path_hops

    return paths

# tuple of 2 strings, strings 1 & 2 must be hosts/switch identifiers
def getBandwidth(entry):
    assert len(entry) == 2
    assert type(entry[0]) is str
    assert type(entry[1]) is str
    if entry[0] == entry[1]:
        return maxsize
    if entry not in bandwidthLk:
        return bandwidthLk[tuple(reversed(entry))]
    return bandwidthLk[entry]

def getHops(entry):
    assert len(entry) == 2
    assert type(entry[0]) is str
    assert type(entry[1]) is str
    if entry[0] == entry[1]:
        return []
    if entry not in bandwidthLk:
        return hopsLk[tuple(reversed(entry))]
    return hopsLk[entry]


def generateTrafficMatrix(numHosts):
    arr = []
    for i in range(numHosts):
        row = []
        for j in range(numHosts):
            if j == i:
                row.append(-1)
                continue
            sourceHostLabel = f"h{i}"
            destHostLabel = f"h{j}"
            # we get the switch that each host is connected to because for some reason
            # ONOS doesn't recognize the host devices in the curl requests
            sourceHostGatewaySwitch = gatewaySwitchLk[sourceHostLabel]
            destHostGatewaySwitch = gatewaySwitchLk[destHostLabel]
            
            # there can be more than 1 path between 2 switches
            # so, we get the average of all of them, assuming ONOS does ECMP
            hopBandwidths = []
            for path in getHops((sourceHostGatewaySwitch, destHostGatewaySwitch)):
                hopBandwidths.append(min(getBandwidth(h) for h in path))
            # assert len(hopBandwidths) > 0 # no hops are there between s2 and s2
            hopBandwidths.append(0) # for the case where hopBandwidths is empty
            
            row.append(min(
                getBandwidth((sourceHostLabel, sourceHostGatewaySwitch)), # host -> switch bandwidth
                getBandwidth((destHostLabel, destHostGatewaySwitch)), # host -> switch bandwidth
                sum(hopBandwidths) / len(hopBandwidths) # ECMP: average of the bandwidth of the options
            ))
        arr.append(row.copy())
    
    return arr


def runner():
    numHosts, numSwitches, edges = read_topo_json('cfg/topo.json')
    
    # populate bandwidth lookup table
    for n1, n2, bw in edges:
        bandwidthLk[(n1, n2)] = bw
    
    # get the gateway switch for each host
    for h in range(numHosts):
        hostLabel = f"h{h}"
        entry = next((x for x in edges if x[0] == hostLabel or x[1] == hostLabel))
        gatewaySwitch = entry[0] if entry[1] == hostLabel else entry[0]
        gatewaySwitchLk[hostLabel] = gatewaySwitch

    # get the hops between any 2 pairs of switches
    hops = read_hops_txt('hops.txt')
    for x, path_list in hops.items():
        hopsLk[x] = path_list

    matrix = generateTrafficMatrix(numHosts)

    with open('traffic-matrix.json', 'w') as f:
        json.dump(matrix, f, indent=2)

if __name__ == "__main__":
    runner()