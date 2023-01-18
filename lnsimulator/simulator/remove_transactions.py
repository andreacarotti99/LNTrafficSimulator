from lnsimulator.simulator.remove_nodes_from_graph import remove_highest_degree_node


def filter_transactions(transactions, num_of_highest_degree_nodes_to_remove, G):
    """ in order to calculate dijkstra multiple times, each time removing the highest degree node,
    it is necessary to remove all the transactions that have as source and as target the removed nodes """
    highest_degree_nodes = []
    for i in range(num_of_highest_degree_nodes_to_remove):
        highest_degree_node = max(G.degree(), key=lambda x: x[1])[0]
        G = remove_highest_degree_node(G)
        highest_degree_nodes.append(highest_degree_node)
    highest_degree_nodes_trg = [s + "_trg" for s in highest_degree_nodes]
    # print(highest_degree_nodes)
    # print(highest_degree_nodes_trg)
    new_transactions = transactions[~transactions.source.isin(highest_degree_nodes)]
    new_transactions = new_transactions[~new_transactions.target.isin(highest_degree_nodes_trg)]
    return new_transactions
