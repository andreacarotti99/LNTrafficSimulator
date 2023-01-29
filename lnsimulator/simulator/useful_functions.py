import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def compute_gini_coefficient_transactions(transactions):
    print("\n# Gini coefficient of the transactions in the network...")
    # Selecting only the source and the target of transactions from the original df
    transactions_df = transactions[['source', 'target']]
    # Count the number of transactions for each node
    transactions_count = transactions_df.source.value_counts().to_dict()
    # Normalize the transactions count by dividing by the total number of transactions
    transactions_prob = {k: v/sum(transactions_count.values()) for k, v in transactions_count.items()}
    # Calculate the Gini coefficient
    prob_sum = sum(np.square(list(transactions_prob.values())))
    gini = 1 - prob_sum
    print("Gini coefficient = ", gini)

def compute_gini_coefficient_graph(G):
    degrees = dict(G.degree())
    sorted_degrees = sorted(degrees.values())
    gini = 1.0 - (2.0 * sum(sorted_degrees) / (len(sorted_degrees) * sum(sorted_degrees)))
    return gini

def draw_lorenz_curve(G):
    # Extract the degree of each node
    degrees = [d for n, d in G.degree()]
    # Sort the degree of nodes in ascending order
    degrees.sort()
    # Calculate the total degree of the graph
    total_degree = sum(degrees)
    # Calculate the cumulative degree of the nodes
    cumulative_degree = [sum(degrees[:i+1])/total_degree for i in range(len(degrees))]
    # Plot the Lorenz curve
    plt.plot(range(len(cumulative_degree)), cumulative_degree)
    plt.plot([0, len(cumulative_degree)], [0, 1], 'r--')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Cumulative Degree')
    plt.title('Lorenz Curve')
    plt.show()

def avg_pairwise_distance(G):
    """ Calculates the average distance between each pair of nodes in a graph G. """
    pairs = nx.all_pairs_shortest_path_length(G)
    total_dist = sum(dist for _, dist_dict in pairs for _, dist in dist_dict.items())
    n = G.order()
    return total_dist / (n * (n-1))

def avg_degree(G):
    """ Calculates the average degree of the nodes in a graph G. """
    sum = 0
    for node in G:
        sum += G.degree[node]
    return sum/G.order()

def total_nodes_capacities(edges):
    """ Creates a dict with the nodes and their capacity """
    # Create an empty dictionary to store the total capacity of each node
    node_capacities = {}
    # Iterate through each row of the edges DataFrame
    for _, row in edges.iterrows():
        # Get the capacity of the channel
        capacity = row["capacity"]
        # Divide the capacity equally between the two nodes
        node1_capacity = capacity / 2
        node2_capacity = capacity / 2
        # Get the public keys of the two nodes in the channel
        node1_pub = row["node1_pub"]
        node2_pub = row["node2_pub"]
        # Check if the current node1_pub already exists in the dictionary
        if node1_pub in node_capacities:
            # If it does, add the capacity to the existing value
            node_capacities[node1_pub] += node1_capacity
        else:
            # If it doesn't, add the node1_pub as a key with the capacity as the value
            node_capacities[node1_pub] = node1_capacity
        # Check if the current node2_pub already exists in the dictionary
        if node2_pub in node_capacities:
            # If it does, add the capacity to the existing value
            node_capacities[node2_pub] += node2_capacity
        else:
            # If it doesn't, add the node2_pub as a key with the capacity as the value
            node_capacities[node2_pub] = node2_capacity
    return node_capacities

def compute_total_fees(all_router_fees):
    """ Creates a dictionary with each node and the total fees earned of the node"""
    # group the dataframe by 'node' and sum the 'fee' column
    total_fees = all_router_fees.groupby('node')['fee'].sum().to_dict()
    return total_fees


def divide_fees_by_capacities(total_fees, node_capacities):
    result = {}
    for key in total_fees.keys():
        if key in node_capacities:
            result[key] = total_fees[key]/node_capacities[key]
        else:
            result[key] = None
    return result
