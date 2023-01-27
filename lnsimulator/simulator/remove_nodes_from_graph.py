import networkx as nx

def remove_highest_degree_node(G):
    """ remove the highest degree node from the graph """
    H = G.copy()
    highest_degree_node = max(H.degree(), key=lambda x: x[1])[0]
    predecessors = list(G.predecessors(highest_degree_node))
    for pred in predecessors:
        G.remove_edge(pred, highest_degree_node)
    print("Removing the node: " + str(highest_degree_node))
    H.remove_node(highest_degree_node)
    return H

def remove_k_highest_degree_nodes(G, k):
    for i in range(k):
        G = remove_highest_degree_node(G)
    return G

