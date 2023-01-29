import pandas as pd
import numpy as np
from lnsimulator.ln_utils import preprocess_json_file
from lnsimulator.simulator.simulate import *
from lnsimulator.simulator.useful_functions import total_nodes_capacities, compute_total_fees, divide_fees_by_capacities


def main():
    data_dir = "ln_data"  # path to the ln_data folder that contains the downloaded data
    amount = 1000  # original amount in satoshi of each transaction
    count = 100 # number of transactions to simulate
    epsilon = 0  # percentage of merchants in the network
    drop_disabled = True  # drop temporarily disabled channels
    drop_low_cap = True  # drop channels with capacity less than amount
    with_depletion = True  # the available channel capacity is maintained for both endpoints
    find_alternative_paths = True
    highest_degree_nodes_to_remove = 3

    print("# 1. Load LN graph data...")
    directed_edges, undirected_edges = preprocess_json_file("%s/sample.json" % data_dir)

    print("\n# 2. Load meta data...")
    node_meta = pd.read_csv("%s/1ml_meta_data.csv" % data_dir)
    providers = list(node_meta["pub_key"])

    print("\n# 3. Start simulation...")
    all_router_fees_list = simulate_incrementally_removing_high_degree_nodes(highest_degree_nodes_to_remove, directed_edges, providers,
                                                      amount, count, drop_disabled, drop_low_cap, with_depletion,
                                                      find_alternative_paths)

    print("\n 4. Computing total_fees / capacity for each node...")
    for i in range(len(all_router_fees_list)):
        # saving into a dict the ratio between fees and capacities for each node (incrementally removing hd nodes)
        nodes_fees = compute_total_fees(all_router_fees_list[i])  # nodes_fees is a dict
        nodes_capacities = total_nodes_capacities(undirected_edges)  # nodes_capacities is a dict
        show_results_fees_capacity_ratio(nodes_fees, nodes_capacities)

if __name__ == "__main__":
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    np.random.seed(6)
    main()

