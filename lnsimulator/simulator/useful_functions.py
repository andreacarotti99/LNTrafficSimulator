
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


def get_hcn(d, k):
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return [key for key, value in sorted_items[:k]]
