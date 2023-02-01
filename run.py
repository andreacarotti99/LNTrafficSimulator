import pandas as pd
import numpy as np
from lnsimulator.ln_utils import preprocess_json_file
from lnsimulator.simulator.simulate import *
from lnsimulator.simulator.useful_functions import total_nodes_capacities, compute_total_fees


def main():
    data_dir = "ln_data"  # path to the ln_data folder that contains the downloaded data
    amount = 1000  # original amount in satoshi of each transaction
    count = 1000 # number of transactions to simulate
    epsilon = 0  # percentage of merchants in the network
    drop_disabled = True  # drop temporarily disabled channels
    drop_low_cap = True  # drop channels with capacity less than amount
    with_depletion = True  # the available channel capacity is maintained for both endpoints
    find_alternative_paths = True
    highest_degree_nodes_to_remove = 0
    highest_degree_nodes_to_split = 1

    print("# 1. Load LN graph data...")
    directed_edges, undirected_edges = preprocess_json_file("%s/sample.json" % data_dir, highest_degree_nodes_to_split)

    print("\n# 2. Load meta data...")
    node_meta = pd.read_csv("%s/1ml_meta_data.csv" % data_dir)
    providers = list(node_meta["pub_key"])

    print("\n# 3. Start simulation...")
    G_list, all_router_fees_list, shortest_paths_list, avg_degree_list = \
        simulate_incrementally_removing_high_degree_nodes(highest_degree_nodes_to_split,
                                                        highest_degree_nodes_to_remove,
                                                        directed_edges,
                                                        providers,
                                                        amount,
                                                        count,
                                                        drop_disabled,
                                                        drop_low_cap,
                                                        with_depletion,
                                                        find_alternative_paths)

    print("\n 4. Computing results...")
    print_results_total_fees(all_router_fees_list, shortest_paths_list, avg_degree_list)


    nodes_fees = compute_total_fees(all_router_fees_list[0])  # nodes_fees is a dict
    nodes_capacities = total_nodes_capacities(undirected_edges)  # nodes_capacities is a dict
    nodes_degrees = dict(G_list[0].degree)  # nodes_degrees is a dict

    # Exporting to a csv file the results for each node: the fees of each node, the degrees of each node, the capacity of each node
    export_fees_degree_capacity(nodes_fees, nodes_degrees, nodes_capacities)

    # Showing in a graph the results
    show_results_capacity_fees_ratio(nodes_fees, nodes_capacities)
    show_results_degree_fees_ratio(nodes_fees, nodes_degrees)


if __name__ == "__main__":
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.options.display.max_colwidth = None
    pd.options.display.width = None
    np.random.seed(6)
    main()

