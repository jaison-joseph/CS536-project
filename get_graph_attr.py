
from main_extension import read_topo_json
import os
import argparse

graphAttrFileName = 'graph_attr.txt'

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='Get the graph_attr.txt')
    
    # Add arguments
    
    parser.add_argument('topo_file', type=str,
    help='full path + name of the json topology file generated by main.py')
    
    parser.add_argument('sorted_links_file', type=str,
                        help='full path + name of the sortedLinks.txt file generated by main.py')
    
    parser.add_argument('graph_attr_path', type=str,
                        help=f'path where the graph attr file {graphAttrFileName} should be written to')

    # Parse arguments
    args = parser.parse_args()

    return args

header = \
'''graph [
  directed 1
  multigraph 1
'''

nodeEntry = \
'''  node [
    id nodeNum
    label "nodeNum"
  ]
'''

edgeEntry = \
'''  edge [
    source srcNodeNum
    target destNodeNum
    key 0
    port portNum
    weight 1
    bandwidth "bw"
  ]
'''

footer = \
''']
'''

portLk = {}

def updatePortLk(sortedLinksFile: str, numNodes: int):
	global portLk
	portCounter = {f"s{i}": 0 for i in range(numNodes)}
	for i in range(numNodes):
		portLk[f"s{i}"] = {}
	with open(sortedLinksFile, 'r') as f:
		for l in f:
			if len(l) < 2:
				continue
			n1, n2, bw = l.strip()[1:-1].split(", ")
			n1 = n1[1:-1]
			n2 = n2[1:-1]
			bw = float(bw)
			if n1 not in portLk or n2 not in portLk:
				assert n1 in portLk or n2 in portLk
				if n1 in portLk:
					portCounter[n1] += 1 
				else:
					portCounter[n2] += 1
			else:
				portLk[n1][n2] = portCounter[n1]
				portCounter[n1] += 1
				portLk[n2][n1] = portCounter[n2]
				portCounter[n2] += 1



def runner(topoFile: str, sortedLinksFile: str, graphAttrPath: str):
	global portLk
	numHosts, numSwitches, edges = read_topo_json(topoFile)
	updatePortLk(sortedLinksFile, numHosts)
	
	fName = os.path.join(graphAttrPath, graphAttrFileName)
	with open(fName, 'w+') as f:

		f.write(header)

		for n in range(numHosts):
			f.write(nodeEntry.replace('nodeNum', str(n)))
	
		for n1, n2, bw in edges:
			v1, v2 = n1[1:], n2[1:]
			if n1[0] == 'h' or n2[0] == 'h':
				continue
			
			s1 = edgeEntry.replace('srcNodeNum', v1).replace('destNodeNum', v2)
			s1 = s1.replace('portNum', str(portLk[n1][n2])).replace('bw', f"{int(bw*1000)}kbps")
			f.write(s1)

			s2 = edgeEntry.replace('srcNodeNum', v2).replace('destNodeNum', v1)
			s2 = s2.replace('portNum',  str(portLk[n2][n1])).replace('bw', f"{int(bw*1000)}kbps")
			f.write(s2)

		f.write(footer)
		

if __name__ == '__main__':
	args = getCommandLineArgs()
	runner(args.topo_file, args.sorted_links_file, args.graph_attr_path)