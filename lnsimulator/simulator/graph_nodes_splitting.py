from collections import Counter
import pandas as pd
import random
import numpy as np

def split_hdn(df, num_hdn_to_split=0):
    """ Given a dataframe of edges splits num_hdn_to_split highest degree nodes into nodes with half the edges of the sarting one"""
    for i in range(num_hdn_to_split):
        node_to_split = highest_degree_node(df)
        df = split_node_dataframe(df, node_to_split)
    return df

def highest_degree_node(df):
    """ Given a dataframe of edges "node1_pub","node2_pub","last_update","capacity","channel_id",'node1_policy','node2_policy',
    returns the key of the node with the highest degree (i.e., number of edges). """
    node_list = list(df['node1_pub']) + list(df['node2_pub'])
    node_degree = Counter(node_list)
    return max(node_degree, key=node_degree.get)

def split_node_dataframe(df, node):
    # Get all the edges for the given node
    edges = df[(df['node1_pub'] == node) | (df['node2_pub'] == node)]

    # Shuffle the edges randomly
    edges = edges.sample(frac=1).reset_index(drop=True)

    # Get the number of edges
    num_edges = len(edges)

    # Create two new nodes
    new_node1 = node + "_1"
    new_node2 = node + "_2"

    # Split the edges into two halves
    first_half = edges[:num_edges//2]
    second_half = edges[num_edges//2:]

    # Replace the node in the first half with the new node1
    first_half.loc[first_half['node1_pub'] == node, 'node1_pub'] = new_node1
    first_half.loc[first_half['node2_pub'] == node, 'node2_pub'] = new_node1

    # Replace the node in the second half with the new node2
    second_half.loc[second_half['node1_pub'] == node, 'node1_pub'] = new_node2
    second_half.loc[second_half['node2_pub'] == node, 'node2_pub'] = new_node2

    # Remove the original node from the dataframe
    df = df[(df['node1_pub'] != node) & (df['node2_pub'] != node)]

    # Concatenate the two halves and the original dataframe to form the new dataframe
    df = pd.concat([df, first_half, second_half])

    return df
