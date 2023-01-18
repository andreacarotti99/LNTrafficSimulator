import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import functools
import concurrent.futures
from lnsimulator.ln_utils import preprocess_json_file
import lnsimulator.simulator.transaction_simulator as ts
import lnsimulator.simulator.transaction_simulator_changed_topology as ts_topologies


def simulate_incrementally_removing_high_degree_nodes(k, directed_edges, providers, amount, count, drop_disabled, drop_low_cap, with_depletion, find_alternative_paths):
    print("\n# Simulate incrementally removing top " + str(k) + " high degree nodes")
    simulator = ts_topologies.TransactionSimulatorDifferentTopologies(directed_edges, providers, amount, count, drop_disabled=drop_disabled, drop_low_cap=drop_low_cap, with_depletion=with_depletion)
    transactions = simulator.transactions
    shortest_paths_list, alternative_paths_list, all_router_fees_list, total_depletions_list, successful_transactions, FinalGraph = simulator.simulate_with_multiple_topologies(weight="total_fee", with_node_removals=find_alternative_paths, max_threads=1, num_of_highest_degree_nodes_to_remove=k)

    # shortest_paths is a df:
    # 'transaction_id', 'original_cost', 'length', 'path'

    # all_router_fees is a df:
    # 'transaction_id', 'node', 'fee'

    # transactions is a df:
    # 'transaction_id', 'source', 'target', 'amount_SAT', 'success'

    average_fees_incrementally_removing_nodes = []
    total_fees_incrementally_removing_nodes = []
    nodes_removed = []

    for i in range(len(all_router_fees_list)):
        print("Average all routers fee removing " + str(i) + " highest degree nodes: " + str(all_router_fees_list[i]['fee'].mean()))
        print("Sum of all routers fee removing " + str(i) + " highest degree nodes: " + str(all_router_fees_list[i]['fee'].sum()))
        nodes_removed.append(i)
        total_fees_incrementally_removing_nodes.append(all_router_fees_list[i]['fee'].sum())
        average_fees_incrementally_removing_nodes.append(all_router_fees_list[i]['fee'].mean())

    plt.plot(nodes_removed, total_fees_incrementally_removing_nodes)
    # plt.plot(nodes_removed, average_fees_incrementally_removing_nodes)
    plt.show()

    return

def main():
    data_dir = "ln_data" # path to the ln_data folder that contains the downloaded data
    amount = 20000 # original amount in satoshi of each transaction
    count = 1000 # number of transactions to simulate
    epsilon = 0 # percentage of merchants in the network
    drop_disabled = True # drop temporarily disabled channels
    drop_low_cap = True # drop channels with capacity less than amount
    with_depletion = True # the available channel capacity is mantained for both endpoints
    find_alternative_paths = True
    cost_function = "standard_dijkstra"
    highest_degree_nodes_to_remove = 10

    print("# 1. Load LN graph data")
    directed_edges = preprocess_json_file("%s/sample.json" % data_dir)

    print("\n# 2. Load meta data")
    node_meta = pd.read_csv("%s/1ml_meta_data.csv" % data_dir)
    providers = list(node_meta["pub_key"])

    simulate_incrementally_removing_high_degree_nodes(highest_degree_nodes_to_remove, directed_edges, providers, amount, count, drop_disabled, drop_low_cap, with_depletion, find_alternative_paths)

np.random.seed(1)
main()


'''
# print("\n# 3. Simulation")
# simulator = ts.TransactionSimulator(directed_edges, providers, amount, count, drop_disabled=drop_disabled, drop_low_cap=drop_low_cap, with_depletion=with_depletion)
# transactions = simulator.transactions
# _, _, all_router_fees, _ = simulator.simulate(weight="total_fee", with_node_removals=find_alternative_paths, max_threads=1)

# output_dir = "test"
# total_income, total_fee = simulator.export(output_dir)
# print(total_income['fee'].mean())

# print("\n# 4. Transactions:")
# print(transactions[['transaction_id', 'source', 'target', 'amount_SAT', 'success']])

print("\n# 4. Saving in test the results")
cheapest_paths, _, all_router_fees, _ = simulator.simulate(weight="total_fee", with_node_removals=False)
print(all_router_fees.head())

print("\n# 5. Saving in test the results")
output_dir = "test"
total_income, total_fee = simulator.export(output_dir)

print("\n# 6. Top nodes with highest daily income")
print(total_income.sort_values("fee", ascending=False).set_index("node").head(10))
df = total_income
mean_fee = df['fee'].mean()
print("\nAverage fee returns of the nodes = ", mean_fee)

print("\n# 7. Top nodes with highest daily traffic")
print(total_income.sort_values("num_trans", ascending=False).set_index("node").head(10))

print("\n# 8. Payment path length distribution")
print(cheapest_paths["length"].value_counts())

print("\n# 9. Payment success ratio")
print((cheapest_paths["length"] > -1).value_counts() / len(cheapest_paths))

print("\n# 10. Payment cost statistics")
print(cheapest_paths["original_cost"].describe())

print("\n# 11. Most frequent payment receivers")
print(simulator.transactions["target"].value_counts().head(5))

print("\n# 12. Number of unique payment senders and receivers")
print(simulator.transactions["source"].nunique(), simulator.transactions["target"].nunique())

print("\n# 13. Transactions shape")
print("Shape: ", transactions.shape)
print("Transactions:")
print(transactions.columns)
print(transactions.head(5))

print("\n# 14. Gini coefficient of the transactions in the network")
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
print("\nDone")
'''
