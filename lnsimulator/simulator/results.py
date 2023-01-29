import matplotlib.pyplot as plt
import pandas as pd

def draw_avg_degree_nodes_removing_highest_degree_nodes(avg_degree_list):
    nodes_removed = []
    for i in range(len(avg_degree_list)):
        nodes_removed.append(i)
    plt.plot(nodes_removed, avg_degree_list)
    plt.title("Average degree of the graph removing incrementally highest degree nodes")
    plt.xlabel("Number of highest degree nodes removed")
    plt.ylabel("Avg degree")
    plt.show()
    return

def draw_total_fees_income_removing_highest_degree_nodes(all_router_fees_list):
    total_fees_incrementally_removing_nodes = []
    nodes_removed = []
    for i in range(len(all_router_fees_list)):
        nodes_removed.append(i)
        total_fees_incrementally_removing_nodes.append(all_router_fees_list[i]['fee'].sum())
    plt.plot(nodes_removed, total_fees_incrementally_removing_nodes)
    plt.title("Total income of all nodes removing incrementally highest degree nodes")
    plt.xlabel("Number of highest degree nodes removed")
    plt.ylabel("Sum of all satoshi earned by all nodes")
    plt.show()
    return

def show_results_total_fees(all_router_fees_list, shortest_paths_list, gini_coefficient_list, avg_degree_list):
    average_fees_incrementally_removing_nodes = []
    nodes_removed = []
    print("\n# Printing the results...")
    for i in range(len(all_router_fees_list)):
        print("\nAverage all routers fee removing " + str(i) + " highest degree nodes: " + str(all_router_fees_list[i]['fee'].mean()))
        print("Sum of all routers fee removing " + str(i) + " highest degree nodes: " + str(all_router_fees_list[i]['fee'].sum()))
        print("Average path length removing " + str(i) + " highest degree nodes: " + str(shortest_paths_list[i]['length'].mean()))

        nodes_removed.append(i)
        average_fees_incrementally_removing_nodes.append(all_router_fees_list[i]['fee'].mean())
        print("Gini coefficient removing " + str(i) + " highest degree nodes: " + str(gini_coefficient_list[i]))
    # plt.plot(nodes_removed, average_fees_incrementally_removing_nodes)

    draw_total_fees_income_removing_highest_degree_nodes(all_router_fees_list)
    draw_avg_degree_nodes_removing_highest_degree_nodes(avg_degree_list)
    return

def show_results_fees_capacity_ratio(nodes_fees, nodes_capacities):
    df = pd.DataFrame(nodes_fees.items(), columns=['node', 'total_fee'])
    df['capacity'] = df['node'].map(nodes_capacities)
    # df['ratio'] = df['total_fee']/df['capacity']
    df['ratio'] = df['capacity'].divide(df['total_fee'], fill_value=0)
    df = df.sort_values(by='capacity',ascending=False)
    print(df.head(20))
    ax = df.plot(x='node', y='ratio',kind='bar')
    plt.title("Ratio (Capacity) / (Total Fees Earned) for each node")
    plt.suptitle("The capacity of each node is in descending order towards right")
    plt.xlabel('node')
    plt.ylabel('Capacity / Total node fee')
    ax.set_xticklabels(df['node'],rotation=90, fontsize=4)
    plt.show()
    return
