
import json
import os
import argparse

portMatrixFileName = 'port_matrix.txt'

from main_extension import read_topo_json

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='Generate network topology and ONOS configuration')
    
    # Add arguments
    
    parser.add_argument('topo_file', type=str,
    help='full path + name of the json file generated by main.py')
    
    parser.add_argument('hops_file_name', type=str,
                        help='Path to (including file) of the output of running the get_hops.sh script in ONOS')
    
    parser.add_argument('port_matrix_file_path', type=str,
                        help=f'path where the matrix file {portMatrixFileName} should be written to')

    # Parse arguments
    args = parser.parse_args()

    return args

def main(topoFile: str, hopsFileName: str, portMatrixFilePath: str):
    # try:
        numHosts, numSwitches, edges = read_topo_json(topoFile)
        matrix = [[-1 for _ in range(numHosts)] for i in range(numHosts)]
        with open(hopsFileName, 'r') as f:
            for l in f.readlines():
                sourceDest, paths = l.strip().split(": ")
                source, dest = sourceDest[1:-1].split(", ")
                source, dest = int(source[1:]), int(dest[1:])
                paths = json.loads(paths.strip())['paths']
                paths.sort(key = lambda x: x['cost'])
                port = paths[0]['links'][0]['src']['port']
                matrix[source][dest] = int(port) - 1 # to work with the model; port numbers start with 0
            
            outputFileName = os.path.join(portMatrixFilePath, portMatrixFileName)
            with open(outputFileName, "w+") as fOut:
                for row in matrix:
                    fOut.write(str(row)[1:-1].replace(" ", ''))
                    fOut.write('\n')
    # except Exception as e:
    #     print(f"Error generating port matrix: {e}")
    #     return

# main("simulations/nsfnet_4_11/run_1/topo.json", "hops.txt", "matrix.txt")

if __name__ == '__main__':
    args = getCommandLineArgs()
    main(args.topo_file, args.hops_file_name, args.port_matrix_file_path)