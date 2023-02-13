import pandas as pd
import copy
from .path_searching import get_shortest_paths
from .remove_nodes_from_graph import remove_highest_degree_node
from .transaction_sampling import sample_transactions_fixed_nodes

def generate_successful_transactions(self, trans_to_generate, num_of_highest_degree_nodes_to_remove, init_capacities, G_origi, hash_transactions=True,
                                     cost_prefix="", weight="total_fee", required_length=None):

    """ Given the sampled number of transaction, this function generates the same amount of transactions, but successful.
        It randomly extracts sources and target from the sample and tries to find a successful path from source to target.
        New Source and target are randomly picked from the sample until a successful transaction is found.
        When it is found, the working transaction is added to the list of transactions, then the final list is returned """

    new_transactions = pd.DataFrame(columns=['transaction_id', 'source', 'target', 'amount_SAT'])
    G_without_k_nodes = G_origi.copy()
    print("\nHighest degree nodes that will be removed during simulation:")
    for i in range(num_of_highest_degree_nodes_to_remove):
        G_without_k_nodes = remove_highest_degree_node(G_without_k_nodes)
    new_cap_map = copy.deepcopy(init_capacities)
    k = 0
    print("\nGenerating " + str(trans_to_generate) + " random transactions from the original sample...")

    while k < trans_to_generate:
        transaction = sample_transactions_fixed_nodes(self.transactions, self.amount, 1, k) # transaction is a dataframe with only one value
        sp, ht, arf, td, rt = get_shortest_paths(new_cap_map, G_without_k_nodes, transaction, hash_transactions, cost_prefix, weight, required_length)
        tr_fees_cost = sp[cost_prefix+'cost'].iloc[0]
        tr_length = sp['length'].iloc[0]
        tr_path = sp['path'].iloc[0]
        if sp['length'].iloc[0] > 0 and tr_fees_cost > 0:  # if a path of length > 0 is found
            new_transaction = {'transaction_id': k, 'source': transaction['source'].iloc[0], 'target': transaction['target'].iloc[0], 'amount_SAT': transaction['amount_SAT'].iloc[0]}
            new_transactions = new_transactions.append(new_transaction, ignore_index=True)
            print("\nTr. ID: " + str(new_transaction['transaction_id']))
            print("Amount: " + str(new_transaction['amount_SAT']))
            print("Length: " + str(tr_length))
            print("Cost: " + str(tr_fees_cost))
            print("Path:")
            print(tr_path)
            k += 1
    print("\nTransactions successfully generated\n")

    # print(new_cap_map)

    return new_transactions
