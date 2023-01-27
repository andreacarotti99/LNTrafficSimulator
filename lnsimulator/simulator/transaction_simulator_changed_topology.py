import sys, os, json, copy
import pandas as pd
from lnsimulator.simulator.graph_preprocessing import generate_graph_for_path_search, init_capacities, \
    prepare_edges_for_simulation, init_node_params
from lnsimulator.simulator.path_searching import get_shortest_paths, \
    get_shortest_paths_successful_generated_transactions
from lnsimulator.simulator.remove_nodes_from_graph import remove_highest_degree_node
from lnsimulator.simulator.remove_transactions import filter_transactions
from lnsimulator.simulator.transaction_sampling import sample_transactions
from lnsimulator.simulator.transaction_simulator import get_shortest_paths_with_node_removals
from lnsimulator.simulator.useful_functions import *


class TransactionSimulatorDifferentTopologies():
    def __init__(self, edges, merchants, amount_sat, count, epsilon=0.8, drop_disabled=True, drop_low_cap=True, with_depletion=True, time_window=None, verbose=False):
        self.verbose = verbose
        self.with_depletion = with_depletion
        self.amount = amount_sat
        self.edges = prepare_edges_for_simulation(edges, amount_sat, drop_disabled, drop_low_cap, time_window, verbose=self.verbose)
        self.node_variables, self.merchants, active_ratio = init_node_params(self.edges, merchants, verbose=self.verbose)
        self.transactions = sample_transactions(self.node_variables, amount_sat, count, epsilon, self.merchants, verbose=self.verbose)
        # self.transactions = sample_transactions_fixed_nodes(self.node_variables, amount_sat, count)
        self.params = {
            "amount":amount_sat,
            "count":count,
            "epsilon":epsilon,
            "with_depletion":with_depletion,
            "drop_disabled":drop_disabled,
            "drop_low_cap": drop_low_cap,
            "time_window":time_window
        }

    def simulate_with_multiple_topologies(self, weight="total_fee", with_node_removals=False, max_threads=1,
                                          excluded=[], required_length=None, cap_change_nodes=[], capacity_fraction=1.0,
                                          num_of_highest_degree_nodes_to_remove=0):
        shortest_paths_list = []
        alternative_paths_list = []
        all_router_fees_list = []
        total_depletions_list = []
        gini_coefficient_list = []
        avg_degree_list = []

        edges_tmp = self.edges.copy()

        # with depletion means that the capacity map will change according to the transactions
        if self.with_depletion:
            current_capacity_map, edges_with_capacity = init_capacities(edges_tmp, self.transactions, self.amount, self.verbose)
            G = generate_graph_for_path_search(edges_with_capacity, self.transactions, self.amount)
        else:
            current_capacity_map = None
            G = generate_graph_for_path_search(edges_tmp, self.transactions, self.amount)

        print("Total nodes in the graph: " + str(G.number_of_nodes()))

        trans_to_generate = self.transactions.shape[0]
        shortest_paths, hashed_transactions, all_router_fees, total_depletions, self.transactions = get_shortest_paths_successful_generated_transactions(self, trans_to_generate, num_of_highest_degree_nodes_to_remove, copy.deepcopy(current_capacity_map), G, hash_transactions=with_node_removals, cost_prefix="original_", weight=weight, required_length=required_length)
        # remove the transactions that have as src and trg the k highest_degree_nodes
        self.transactions = filter_transactions(self.transactions, num_of_highest_degree_nodes_to_remove, G)


        """Starting the multiple iterations considering different topologies"""
        for i in range(num_of_highest_degree_nodes_to_remove+1):

            capacity_map_iteration = copy.deepcopy(current_capacity_map)
            print("\nSimulation removing " + str(i) + " nodes...")
            if i > 0:
                G = remove_highest_degree_node(G)
            print("\nNodes: " + str(G.number_of_nodes()))
            if len(excluded) > 0:
                print(G.number_of_edges(), G.number_of_nodes())
                for node in excluded:
                    if node in G.nodes():
                        G.remove_node(node)
                    pseudo_node = str(node) + "_trg"
                    if pseudo_node in G.nodes():
                        G.remove_node(pseudo_node)
                if self.verbose:
                    print(G.number_of_edges(), G.number_of_nodes())
                print("Additional nodes were EXCLUDED!")
            print("Graph and capacities were INITIALIZED")
            if self.verbose:
                print("Using weight='%s' for the simulation" % weight)
            print("Transactions simulated on original graph STARTED..")

            shortest_paths, hashed_transactions, all_router_fees, total_depletions = get_shortest_paths(capacity_map_iteration, G, self.transactions, hash_transactions=with_node_removals, cost_prefix="original_", weight=weight, required_length=required_length)

            for h in range(shortest_paths.shape[0]):
                print("\nTrans. id: " + str(shortest_paths['transaction_id'].iloc[h]))
                print("Trans. cost: " + str(shortest_paths['original_cost'].iloc[h]))
                print("Trans. length: " + str(shortest_paths['length'].iloc[h]))
                print("Trans. path:")
                print(shortest_paths['path'].iloc[h])


            # print("Router fees other i")
            # print(all_router_fees.values)
            # print("Length trans")
            # print(self.transactions.shape[0])
            # print("Length all rout fees")
            # print(all_router_fees.shape[0])
            # print("List of transactions after shortest paths")
            # print(self.transactions.values)
            # print()

            success_tx_ids = set(shortest_paths["transaction_id"]) # this contains only successful transactions
            # print("Num of suc trans")
            # print(len(success_tx_ids))

            self.transactions["success"] = self.transactions["transaction_id"].apply(lambda x: x in success_tx_ids)
            print("Transactions simulated on original graph DONE")
            print("Transaction success rate:")
            print(self.transactions["success"].value_counts() / len(self.transactions))

            # print(self.transactions["success"])

            if self.verbose:
                print("Length distribution of optimal paths:")
                print(shortest_paths["length"].value_counts())
            if with_node_removals:
                print("Base fee optimization STARTED..")
                alternative_paths = get_shortest_paths_with_node_removals(capacity_map_iteration, G, hashed_transactions, weight=weight, threads=max_threads)
                print("Base fee optimization DONE")
                if self.verbose:
                    if verbose:
                        print("Length distribution of optimal paths:")
                        print(alternative_paths["length"].value_counts())
            else:
                alternative_paths = pd.DataFrame([])
            self.shortest_paths = shortest_paths
            self.alternative_paths = alternative_paths
            self.all_router_fees = all_router_fees

            shortest_paths_list.append(shortest_paths)
            alternative_paths_list.append(alternative_paths)
            all_router_fees_list.append(all_router_fees)
            total_depletions_list.append(total_depletions)

            print("Fees")
            print(all_router_fees)
            print("Transactions")
            print(self.transactions)

            gini_coefficient = compute_gini_coefficient_graph(G)
            gini_coefficient_list.append(gini_coefficient)
            avg_degree_list.append(avg_degree(G))
            # draw_lorenz_curve(G)
            # print("avg degree:")

            transactions = self.transactions
            successful_transactions = transactions[transactions['success'] == True]

        # print(shortest_paths_list)
        return shortest_paths_list, alternative_paths_list, all_router_fees_list, total_depletions_list, successful_transactions, G, gini_coefficient_list, avg_degree_list



