import os
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read(id, date):
    file = f'loogs/{date}/{id}.csv'
    data = pd.read_csv(file)
    print(data)
    data['g_o_b'] = data['result'] != "Game"
    score = round(data['g_o_b'].sum()/data.shape[0], 2)
    data.to_csv(file, index=False)
    csv_to_img(data)
    return score


def csv_to_img(df):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    fig.tight_layout()
    plt.savefig("loogs/2023-02-09/1.png")



if __name__ == '__main__':
    read(1, "2023-02-09")


