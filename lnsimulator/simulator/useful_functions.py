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
