"""
Script for making boxplots
"""

import pandas as pd
import matplotlib.pyplot as plt


def boxplot():

    # paste list1 here
    list1 = [1311, 1051]
    # paste list2 here
    list2 = [0.826958, 0.788139]
    # paste list3 here
    list3 = [0.826958, 0.788139]
    # paste list4 here
    list4 = [0.826958, 0.788139]

    # change which lists to include here
    df = pd.DataFrame(list(zip(list1, list2, list3, list4)), columns=['random', 'JW', 'LEFV', 'CDCL'])

    df.boxplot(grid=False)
    plt.title('Boxplot for ...')
    plt.xlabel('{xlabel}')
    plt.ylabel('{ylabel}')
    plt.show()

if __name__ == "__main__":
    boxplot()