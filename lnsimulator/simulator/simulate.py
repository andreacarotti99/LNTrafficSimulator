import lnsimulator.simulator.transaction_simulator_changed_topology as ts_topologies
from lnsimulator.simulator.results import *


def simulate_incrementally_removing_high_degree_nodes(k, directed_edges, providers, amount, count, drop_disabled, drop_low_cap, with_depletion, find_alternative_paths):

    print("\n# Starting simulation incrementally removing top " + str(k) + " high degree nodes...")
    simulator = ts_topologies.TransactionSimulatorDifferentTopologies(directed_edges, providers, amount, count, drop_disabled=drop_disabled, drop_low_cap=drop_low_cap, with_depletion=with_depletion)
    shortest_paths_list, alternative_paths_list, all_router_fees_list, total_depletions_list, successful_transactions, FinalGraph, gini_coefficient_list, avg_degree_list = simulator.simulate_with_multiple_topologies(weight="total_fee", with_node_removals=find_alternative_paths, max_threads=1, num_of_highest_degree_nodes_to_remove=k)

    # shortest_paths is a df:   'transaction_id', 'original_cost', 'length', 'path'
    # all_router_fees is a df:  'transaction_id', 'node', 'fee'
    # transactions is a df:     'transaction_id', 'source', 'target', 'amount_SAT', 'success'

    show_results(all_router_fees_list, shortest_paths_list, gini_coefficient_list, avg_degree_list)

    return
