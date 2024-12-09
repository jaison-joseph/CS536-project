import os
import random
import networkx as nx
import pickle
import numpy as np
import tarfile
from tqdm import tqdm

import torch
import pandas as pd
# from pathlib import Path
import glob

DATASET_PATH = './dataset/'
DATA_NAME = 'nsfnet'


def process_graph(filename):
    G = nx.read_gml(filename, destringizer=int)
    n_node = G.number_of_nodes()
    for i in range(n_node):  # i: src
        for j in range(n_node):  # j: dst
            if j in G[i]:
                G[i][j][0]['bandwidth'] = G[i][j][0]['bandwidth'].replace("kbps", "")
    return G, n_node


def create_routing_matrix(G, n_node, routing_file, edges):
    """
    MatrixPath : NxN Matrix
            Matrix where each cell [i,j] contains the path to go from node
            i to node j.
    """
    connections = {}
    max_path_len = 0
    for src in G:
        connections[src] = {}
        for dst in G[src].keys():
            port = G[src][dst][0]['port']
            connections[src][port] = dst
    R = np.loadtxt(routing_file, delimiter=',', dtype=str)
    R = R[:, :-1]
    R = R.astype(int)
    MatrixPath = np.empty((n_node, n_node), dtype=object)
    for src in range(n_node):
        for dst in range(n_node):
            node = src
            path = []
            path_len = 0
            while not node == dst:
                port = R[node][dst]
                next_node = connections[node][port]
                path.append(edges.index((node, next_node)) + 1)
                node = next_node
                path_len += 1
            MatrixPath[src][dst] = path
            if path_len > max_path_len:
                max_path_len = path_len
    return MatrixPath, max_path_len


def create_link_cap(G):
    edges = list(map(lambda x: (x[0], x[1]), G.edges))
    link_cap = [0]
    for e in edges:
        bandwidth = G[e[0]][e[1]][0]['bandwidth']
        link_cap.append(int(bandwidth))
    return edges, link_cap


def mask(MatrixPath, max_path_len, n_node):
    n_path = n_node * (n_node - 1)
    Paths = np.zeros((n_path, max_path_len), dtype=int)
    # mask = np.zeros((n_path, max_path_len), dtype=int)
    ind = 0
    row = []
    col = []
    link_idx = []
    for i in range(n_node):
        for j in range(n_node):
            if not i == j:
                path_len = len(MatrixPath[i][j])
                Paths[ind][:path_len] = MatrixPath[i][j]
                row.extend([ind for _ in range(path_len)])
                col.extend([i for i in range(path_len)])
                link_idx.extend(MatrixPath[i][j])
                ind += 1
    return Paths, row, col, link_idx


def get_result(line, n_node, offset):
    sources = []
    destinations = []
    traffic = []
    delay = []
    jitter = []
    pktloss = []
    for i in range(n_node):
        for j in range(n_node):
            if not i == j:
                sources.append(i)
                destinations.append(j)
                traffic.append(float(line[(i * n_node + j) * 3]))
                delay.append(float(line[offset + (i * n_node + j) * 7]))
                jitter.append(float(line[offset + (i * n_node + j) * 7 + 6]))
                pktloss.append(float(line[(i * n_node + j) * 3 + 2]) / float(line[(i * n_node + j) * 3 + 1]))

    return traffic, delay, jitter, {"source": sources, "destination": destinations,
                                    "traffic": traffic, "delay": delay, "jitter": jitter,
                                    "packet_loss": pktloss}


def make_pt(dir_list, dir_path, pt_path, G, n_node, edges, link_cap):
    for dirname in tqdm(dir_list):
        pt_file = dirname + '.pt'
        routing_file = open(os.path.join(dir_path, dirname) + "/Routing.txt", "rb")
        df = pd.read_csv(os.path.join(dir_path, dirname) + "/simulationResults.csv")
        MatrixPath, max_path_len = create_routing_matrix(G, n_node, routing_file, edges)
        MatrixPath, row, col, link_idx = mask(MatrixPath, max_path_len, n_node)
        sample_list = []

        for sim_id in df['simid'].unique():
            traffic = df['traffic'][df['simid'] == sim_id].tolist()
            delay = df['delay'][df['simid'] == sim_id].tolist()
            jitter = df['jitter'][df['simid'] == sim_id].tolist()
            pktloss = df['packet_loss'][df['simid'] == sim_id].tolist()
            sample = {
                'package': torch.FloatTensor(traffic),
                'bandwidth': torch.FloatTensor(link_cap),
                'path': torch.LongTensor(MatrixPath),
                'row': torch.LongTensor(row),
                'col': torch.LongTensor(col),
                'link_idx': torch.LongTensor(link_idx),
                'delay': torch.FloatTensor(delay),
                'jitter': torch.FloatTensor(jitter),
                'packet_loss': torch.FloatTensor(pktloss),
            }
            sample_list.append(sample)
        with open(os.path.join(pt_path, pt_file), 'wb') as f:
            pickle.dump(sample_list, f)


def process(path, data_name, eval_rate):
    dir_path = f"{path}/{data_name}"
    graph_file = f"{dir_path}/graph_attr.txt"
    pt_path = f"{dir_path}/process"
    if not os.path.exists(pt_path):
        os.mkdir(pt_path)

    pt_train = f"{pt_path}/train"
    pt_eval = f"{pt_path}/eval"
    if not os.path.exists(pt_train):
        os.mkdir(pt_train)
    if not os.path.exists(pt_eval):
        os.mkdir(pt_eval)

    G, n_node = process_graph(graph_file)
    edges, link_cap = create_link_cap(G)

    # Specify the pattern to match directories
    pattern = dir_path + '/results_*/'
    # Use glob to list directories
    tar_files = [os.path.basename(os.path.normpath(d)) for d in glob.glob(pattern)]

    evaling = int(len(tar_files) * eval_rate)
    random.shuffle(tar_files)
    train_file, eval_file = tar_files[evaling:], tar_files[:evaling]

    print('# process training data...')
    make_pt(train_file, dir_path, pt_train, G, n_node, edges, link_cap)
    print('# process evaling data...')
    make_pt(eval_file, dir_path, pt_eval, G, n_node, edges, link_cap)


process(DATASET_PATH, DATA_NAME, 1)
