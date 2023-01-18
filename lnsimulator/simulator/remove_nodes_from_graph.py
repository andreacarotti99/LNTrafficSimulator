import networkx as nx

def remove_highest_degree_node(G):
    """ remove the highest degree node from the graph """
    H = G.copy()
    highest_degree_node = max(H.degree(), key=lambda x: x[1])[0]
    H.remove_node(highest_degree_node)
    return H

def remove_k_highest_degree_nodes(G, k):
    for i in range(k):
        G = remove_highest_degree_node(G)
    return G

