import pandas as pd
from matplotlib import pyplot as plt
import os

def main():
    file_path = os.path.join(os.getcwd(), "results.csv")
    df = pd.read_csv(file_path)
    df['ratio'] = df['degree'].divide(df['total_fee'], fill_value=0)
    df = df.sort_values(by='total_fee',ascending=False)
    ax = df.plot(x='node', y='capacity',kind='bar')
    plt.title(" ")
    plt.suptitle(" ")
    plt.xlabel('node')
    plt.ylabel(' ')
    ax.set_xticklabels(df['node'],rotation=90, fontsize=4)
    plt.show()
    return

if __name__ == "__main__":
    main()
