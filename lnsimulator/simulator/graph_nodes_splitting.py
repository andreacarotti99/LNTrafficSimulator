import pandas as pd

from lnsimulator.simulator.useful_functions import total_nodes_capacities


def split_huge_nodes(df, num_nodes_to_split=0, split_by_edge=True):
    """ Given a dataframe of edges splits num_nodes_to_split highest degree nodes into nodes with half the edges of the starting one.
    or splits num_nodes_to_split highest capacity nodes into nodes with half the capacity of the starting nodes"""
    if split_by_edge == True:
        print("\nSplitting highest degree nodes by edges...")
        for i in range(num_nodes_to_split):
            node_to_split, node_to_split_degree = get_highest_degree_node(df)
            print("Splitting the node: " + str(node_to_split) + " with degree: " + str(node_to_split_degree))
            df = split_node_dataframe_by_edge(df, node_to_split)
    else:  # split_by_edge == False means that the split is by capacity
        print("\nSplitting highest capacity nodes by capacity...")
        for i in range(num_nodes_to_split):
            node_to_split, node_to_split_capacity = get_highest_capacity_node(df)
            print("Splitting the node: " + str(node_to_split) + " with capacity: " + str(node_to_split_capacity))
            df = split_node_dataframe_by_capacity(df, node_to_split)
    return df

def get_highest_degree_node(df):
    """ Given a dataframe of edges "node1_pub","node2_pub","last_update","capacity","channel_id",'node1_policy','node2_policy',
    returns the key of the node with the highest degree (i.e. max number of edges). """

    # create a list of all unique nodes
    nodes = list(set(df['node1_pub'].tolist() + df['node2_pub'].tolist()))

    # initialize dictionary to store the number of edges for each node
    node_degree = {node: 0 for node in nodes}

    # count the number of edges for each node
    for index, row in df.iterrows():
        node_degree[row['node1_pub']] += 1
        node_degree[row['node2_pub']] += 1

    # find the node with the highest degree
    highest_degree_node = max(node_degree, key=node_degree.get)

    return highest_degree_node, node_degree.get(highest_degree_node)


def get_highest_capacity_node(df):
    nodes_capacities = total_nodes_capacities(df)
    highest_capacity_node = max(nodes_capacities, key=nodes_capacities.get)
    return highest_capacity_node, nodes_capacities.get(highest_capacity_node)


def split_node_dataframe_by_edge(df, node):
    """ Given the key of a node and a dataframe: 'node1_pub','node2_pub','last_update','capacity','channel_id','node1_policy','node2_policy'
    it finds the node in the dataframe and splits it into two new nodes, then removes the original node from the dataframe """

    # Get all the edges for the given node
    edges = df[(df['node1_pub'] == node) | (df['node2_pub'] == node)]

    # Shuffle the edges randomly
    edges = edges.sample(frac=1).reset_index(drop=True)

    # Get the number of edges
    num_edges = len(edges)

    # Split the edges into two halves
    first_half = edges[:num_edges//2]
    second_half = edges[num_edges//2:]

    # Replace the node in the first half with the new node1
    first_half = replace_node_edges(first_half, node, '_1', 'node1_pub')
    first_half = replace_node_edges(first_half, node, '_1', 'node2_pub')

    # Replace the node in the second half with the new node2
    second_half = replace_node_edges(second_half, node, '_2', 'node1_pub')
    second_half = replace_node_edges(second_half, node, '_2', 'node2_pub')

    # Remove the original node from the dataframe
    df = df[(df['node1_pub'] != node) & (df['node2_pub'] != node)]

    # Concatenate the two halves and the original dataframe to form the new dataframe
    df = pd.concat([df, first_half, second_half])

    df = df.sample(frac=1).reset_index(drop=True)

    return df

def replace_node_edges(df, node, new_node_idx='_1', column_to_substitute='node1_pub'):
    new_node1 = node + new_node_idx
    for i, row in df.iterrows():
        if row[column_to_substitute] == node:
            df.at[i, column_to_substitute] = new_node1
    return df


def split_node_dataframe_by_capacity(df, node):
    # Get all the edges for the given node
    edges = df[(df['node1_pub'] == node) | (df['node2_pub'] == node)]

    node1_df = edges.copy()
    node2_df = edges.copy()

    # Two copies of the df containing the node and in the first copy we add '_1' to the name of the node and split by two the capacity
    for i, row in node1_df.iterrows():
        if row['node1_pub'] == node:
            node1_df.at[i, 'node1_pub'] = node + "_1"
            node1_df.at[i, 'capacity'] = node1_df.at[i, 'capacity'] / 2
        if row['node2_pub'] == node:
            node1_df.at[i, 'node2_pub'] = node + "_1"
            node1_df.at[i, 'capacity'] = node1_df.at[i, 'capacity'] / 2

    for i, row in node2_df.iterrows():
        if row['node1_pub'] == node:
            node2_df.at[i, 'node1_pub'] = node + "_2"
            node2_df.at[i, 'capacity'] = node2_df.at[i, 'capacity'] / 2
        if row['node2_pub'] == node:
            node2_df.at[i, 'node2_pub'] = node + "_2"
            node2_df.at[i, 'capacity'] = node2_df.at[i, 'capacity'] / 2

    # Remove the original node from the dataframe
    df = df[(df['node1_pub'] != node) & (df['node2_pub'] != node)]

    # Concatenate the two copies and the original dataframe to form the new dataframe
    df = pd.concat([df, node1_df, node2_df])

    df = df.sample(frac=1).reset_index(drop=True)

    return df

def replace_node_capacity(df, node, new_node_idx='_1', column_to_substitute='node1_pub'):
    new_node1 = node + new_node_idx
    for i, row in df.iterrows():
        if row[column_to_substitute] == node:
            df.at[i, column_to_substitute] = new_node1
    return df
