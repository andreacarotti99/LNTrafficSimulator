import pandas as pd
from matplotlib import pyplot as plt
import os





def main():

    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_file_directory, "results.csv")
    df = pd.read_csv(file_path)
    df['ratio'] = df['total_fee'].divide(df['capacity'], fill_value=0)
    df = df.sort_values(by='capacity',ascending=False)

    print("Avg deg: " + str(df['degree'].mean()))
    print("Avg cap: " + str(df['capacity'].mean()))
    print("Avg fee: " + str(df['total_fee'].mean()))
    print("Avg routed trans: " + str(df['routed_transactions'].mean()))
    print("Number of nodes: " + str(df.shape[0]))

    # highest_capacity_node = df.nlargest(2, 'capacity')['capacity'].idxmin()
    # node_number = df.loc[highest_capacity_node]['node']
    # print("Highest capacity node: " + str(node_number))
    # n = '03d37fca0656558de4fd86bbe490a38d84a46228e7ec1361801f54f9437a18d618_1'
    # f = df[df['node'] == n]['total_fee'].values[0]
    # print("Total fee of " + str(n) + ": " + str(f))

    # Performing the filtering:
    # df = df.head(180)
    # df.loc[df['total_fee'] > 3000, 'total_fee'] = 3000
    # df = df.loc[df['degree'] > 20]
    # df = df.loc[df['total_fee'] >= 125]
    # df = df.loc[df['routed_transactions'] >= 40]
    # df = df.loc[df['routed_transactions'] <= 100]
    # End filtering
    # df.loc[df['ratio'] > 0.0004, 'ratio'] = 0.0004
    # df = df.loc[df['ratio'] > 0.000005]
    # df = df.loc[df['capacity'] >= 16_000_000]


    ax = df.plot(x='node', y='ratio',kind='bar')
    plt.title("fee/capacity for each node")
    plt.suptitle("CAP of each node decreases (->) - DESC")
    plt.xlabel('node')
    plt.ylabel('fee/capacity')
    ax.set_xticklabels(df['node'],rotation=90, fontsize=4)
    # ax.set_xticklabels(df['node'],rotation=90, fontsize=4)
    plt.show()
    return



if __name__ == "__main__":
    main()





