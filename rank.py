import numpy as np
import json

def save_dict_to_json(data_dict, file_path):
    """
    Save a Python dictionary as a JSON file.

    Parameters:
    data_dict (dict): The dictionary to save as JSON.
    file_path (str): The file path where the JSON file will be saved.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        print(f"Dictionary successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the dictionary: {e}")

def read_json_to_dict(file_path):
    """
    Reads a JSON file and returns its content as a dictionary.

    :param file_path: str, the path to the JSON file
    :return: dict, the content of the JSON file as a dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return None

def pagerank(M, d: float = 0.85):
    """PageRank algorithm with explicit number of iterations. Returns ranking of nodes (pages) in the adjacency matrix.

    Parameters
    ----------
    M : numpy array
        adjacency matrix where M_i,j represents the link from 'j' to 'i', such that for all 'j'
        sum(i, M_i,j) = 1
    d : float, optional
        damping factor, by default 0.85

    Returns
    -------
    numpy array
        a vector of ranks such that v_i is the i-th rank from [0, 1],

    """
    print("Building...")
    N = M.shape[1]
    w = np.ones(N) / N
    M_hat = d * M
    v = M_hat @ w + (1 - d)

    normVal = np.linalg.norm(w-v)
    i  = 0
    print("Starting...")
    while(normVal >= 1e-10):
        w = v
        v = M_hat @ w + (1 - d)
        normVal = np.linalg.norm(w-v)
        print(f"i = {i}: error = {normVal}")
        if i % 5 == 0:
            yield v
        i += 1
    return v

# M = np.array([[0, 0, 0, 0],
#               [0, 0, 0, 0],
#               [1, 0.5, 0, 0],
#               [0, 0.5, 1, 0]])
# v = pagerank(M, 0.85)

def convert_to_adjacency_matrix(graph):
    # Get all unique nodes in the graph
    nodes = set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors.keys())
    
    # Create a sorted list of nodes to ensure consistent ordering
    nodes = sorted(nodes)
    
    # Create a mapping from node to index
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    
    # Initialize an NxN matrix with zeros, using float32 for faster arithmetic
    N = len(nodes)
    adjacency_matrix = np.zeros((N, N), dtype=np.float32)
    
    # Fill the adjacency matrix
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            i = node_to_index[node]
            j = node_to_index[neighbor]
            # Place the weight in the transposed position to correctly represent the PageRank matrix
            adjacency_matrix[j, i] = weight
    
    # Normalize the columns to ensure the sum of each column is 1
    column_sums = adjacency_matrix.sum(axis=0)
    # Avoid division by zero in case there is a column with sum 0
    column_sums[column_sums == 0] = 1
    adjacency_matrix = adjacency_matrix / column_sums
    
    return adjacency_matrix, node_to_index



wgraph = read_json_to_dict('weighted_graph.json')

name_to_int = dict()
int_to_name = dict()
for i, name in enumerate(wgraph):
    name_to_int[name] = i
    int_to_name[i] = name

int_wgraph = dict()
for name in wgraph:
    i = name_to_int[name]
    int_wgraph[i] = dict()
    for linked_name in wgraph[name]:
        j = name_to_int[linked_name]
        int_wgraph[i][j] = wgraph[name][linked_name]

adj_matrix, node_to_index = convert_to_adjacency_matrix(int_wgraph)

# # Now you can apply the pagerank algorithm to the adjacency matrix
# ranks = pagerank(adj_matrix)

# # If you need to map the ranks back to the original nodes:
# rank_dict = {int_to_name[node]: rank for node, rank in zip(node_to_index.keys(), ranks)}

# save_dict_to_json(rank_dict, 'ranks.json')



for i, ranks in enumerate(pagerank(adj_matrix)):
    #rank_dict = {int_to_name[node]: rank for node, rank in zip(node_to_index.keys(), ranks)}

    ranks = [(int_to_name[node], rank) for node, rank in zip(node_to_index.keys(), ranks)]
    ranks = sorted(ranks, key = lambda p: p[1], reverse=True)

    ranks_dict = dict()
    ranks_dict['ranks'] = ranks

    save_dict_to_json(ranks_dict, f"ranks{i}.json")