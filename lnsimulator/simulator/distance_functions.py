def weight_between_edges_distance_function(u, v, data, G):
    # Get the weight of the edge between the two nodes
    return data.get('total_fee', 0)

def degree_distance_function(u, v, data, G):
    # Get the weight of the edge between the two nodes
    # 1 is if the attribute "total_fee" is not present
    return data.get('total_fee', 1) + G.degree[v]
