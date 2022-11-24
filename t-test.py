"""
T-test script:
1) Paste the lists of values for which you want to test whether the means are significantly different (from results-H{})
2) run the script as >python3 t-test.py
"""

from scipy.stats import ttest_ind

# paste list1 here (backtracks, unit clauses, runtime)
list1 = [1132, 1051, 1987, 1077, 1086, 1483, 1067, 1098, 1082]
# paste list2 here (backtracks, unit clauses, runtime)
list2 = [1056, 1051, 1865, 1077, 1086, 1232, 1067, 1098, 1082]


def main(list1, list2):

    # t-test for independent samples
    res = ttest_ind(list1, list2, equal_var=False)

    print("==================================")
    print("T-test results:")
    print(f"t-statistic: {round(res.statistic, 5)}")
    if res.pvalue > 0.05:
        print(f"p-value = {round(res.pvalue, 5)} > 0.05; H0 not rejected: the two lists have equal mean and are not "
              f"significantly different")
    else:
        print(f"p-value = {round(res.pvalue, 5)} < 0.05; H0 rejected: the two means are significantly different")
    print("==================================")


if __name__ == "__main__":
    main(list1, list2)