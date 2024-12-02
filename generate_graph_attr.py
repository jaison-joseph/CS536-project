import json
import os
import argparse

def load_topo_json(file_path):
    """Load and parse the topo.json file."""
    try:
        with open(file_path, 'r') as f:
            topo = json.load(f)
        return topo
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON - {file_path}\n{e}")
        exit(1)

def load_port_matrix(file_path):
    """Load and parse the port_matrix.txt file."""
    port_matrix = []
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                # Remove whitespace and split by comma
                row = line.strip().split(',')
                # Convert to integers
                try:
                    row = [int(x) for x in row]
                except ValueError:
                    print(f"Error: Non-integer value found in port_matrix.txt at line {line_number}")
                    exit(1)
                port_matrix.append(row)
        return port_matrix
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        exit(1)

def assign_node_ids(topo):
    """
    Assign unique IDs to switches and hosts.
    Switches: s0 to s11 => IDs 0 to 11
    Hosts: h0 to h11 => IDs 12 to 23
    """
    node_ids = {}
    current_id = 0

    # Assign IDs to switches
    for i in range(topo['number_switches']):
        switch = f's{i}'
        node_ids[switch] = current_id
        current_id += 1

    # Assign IDs to hosts
    for i in range(topo['number_hosts']):
        host = f'h{i}'
        node_ids[host] = current_id
        current_id += 1

    return node_ids

def generate_graph_attr(topo, port_matrix, node_ids, output_file):
    """Generate the graph_attr.txt file based on topo and port_matrix."""
    try:
        with open(output_file, 'w') as f:
            # Write graph attributes
            f.write('graph [\n')
            f.write('  directed 1\n')
            f.write('  multigraph 1\n')

            # Write nodes
            for node, id_ in node_ids.items():
                if node.startswith('s'):
                    f.write('  node [\n')
                    f.write(f'    id {id_}\n')
                    f.write(f'    label "{node[1:]}"\n')
                    f.write('  ]\n')
            f.write('\n')

            # Write edges
            for edge in topo['network_edges']:
                source, target, bw_mbps = edge

                # Validate source and target exist
                if source not in node_ids:
                    print(f"Warning: Source node '{source}' not defined in node_ids. Skipping edge.")
                    continue
                if target not in node_ids:
                    print(f"Warning: Target node '{target}' not defined in node_ids. Skipping edge.")
                    continue

                source_id = -1
                target_id = -1

                # Determine port number
                port = 0  # Default port

                # Check if both source and target are switches and within the first 8 switches (s0 to s7)
                if source.startswith('s') and target.startswith('s'):
                    source_id = node_ids[source]
                    target_id = node_ids[target]
                    src_index = int(source[1:])
                    tgt_index = int(target[1:])
                    if src_index < len(port_matrix) and tgt_index < len(port_matrix[src_index]):
                        port = port_matrix[src_index][tgt_index]
                    else:
                        port = -1  # Default if out of port_matrix bounds

                    # Convert bandwidth from Mbps to kbps and format as string
                    bw_kbps = int(bw_mbps * 1000)
                    bw_str = f'"{bw_kbps}kbps"'

                    # Write edge block
                    f.write('  edge [\n')
                    f.write(f'    source {source_id}\n')
                    f.write(f'    target {target_id}\n')
                    f.write('    key 0\n')
                    f.write(f'    port {port}\n')
                    f.write('    weight 1\n')
                    f.write(f'    bandwidth {bw_str}\n')
                    f.write('  ]\n')
            f.write(']\n')
        print(f'graph_attr.txt has been generated successfully as "{output_file}".')
    except IOError as e:
        print(f"Error: Unable to write to file - {output_file}\n{e}")
        exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate graph_attr.txt from topo.json and port_matrix.txt.")
    parser.add_argument('simulation_name', type=str, help="Name of the simulation directory under 'simulations/'")
    args = parser.parse_args()

    # File paths
    cwd = os.getcwd()
    simulation = os.path.join(cwd, "simulations", args.simulation_name)

    # Validate simulation directory
    if not os.path.isdir(simulation):
        print(f"Error: Simulation directory '{simulation}' does not exist.")
        exit(1)

    topo_json_path = os.path.join(simulation, 'topo.json')
    port_matrix_path = os.path.join(simulation, 'port_matrix.txt')
    output_graph_attr = os.path.join(simulation, 'graph_attr.txt')

    # Load files
    topo = load_topo_json(topo_json_path)
    port_matrix = load_port_matrix(port_matrix_path)

    # Assign unique IDs to nodes
    node_ids = assign_node_ids(topo)

    # Generate graph_attr.txt
    generate_graph_attr(topo, port_matrix, node_ids, output_graph_attr)

if __name__ == '__main__':
    main()
