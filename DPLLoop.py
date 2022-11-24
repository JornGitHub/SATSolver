import DPLL
import numpy as np
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import sys
from pathlib import Path
import os

normal9x9 = 'test/normal_sudokus9x9'
normal16x16 = 'test/normal_sudokus16x16'
special9x9 = 'test/special_sudokus9x9'
special16x16 = 'test/special_sudokus16x16'

def remove_outliers(list_backtracks, list_time):
    Q1 = np.quantile(list_backtracks, 0.15)
    # Q2 = np.quantile(list_backtracks, 0.5)
    Q3 = np.quantile(list_backtracks, 0.85)
    IQR = Q3 - Q1
    upper_fence = Q3 + (1.5 * IQR)
    new_list_backtracks = []
    new_list_time = []
    for i in range(len(list_backtracks)):
        if list_backtracks[i] < upper_fence:
            new_list_backtracks.append(list_backtracks[i])
            new_list_time.append(list_time[i])

    all_lists = []

    if sum(new_list_backtracks) == 0:
        all_lists.append(list_backtracks)
        all_lists.append(list_time)
    else:
        all_lists.append(new_list_backtracks)
        all_lists.append(new_list_time)

    return all_lists

def dpll_loop(start, stop, heuristic):
    
    total_values = []
    total_backtracks = []
    total_units = []
    total_time = []
    total_backtracks_no_zeros = []
    total_units_no_zeros = []
    total_time_no_zeros = []


    for i in range(start, stop):
        number = i
        if sys.argv[1] == '1':
            values = DPLL.main(f'{normal9x9}/sudoku{number}.cnf', heuristic)
        if sys.argv[1] == '2':
            values = DPLL.main(f'{normal16x16}/sudoku{number}.cnf', heuristic)
        if sys.argv[1] == '3':
            values = DPLL.main(f'{special9x9}/sudoku{number}.cnf', heuristic)
        if sys.argv[1] == '4':
            values = DPLL.main(f'{special16x16}/sudoku{number}.cnf', heuristic)
        total_values.append(values)

    for value in total_values:
        if value[0] != 0:
            total_backtracks_no_zeros.append(value[0])
            total_units_no_zeros.append(value[1])
            total_time_no_zeros.append(value[2])
        total_backtracks.append(value[0])
        total_units.append(value[1])
        total_time.append(value[2])

    total_backtracks_no_outliers = remove_outliers(total_backtracks, total_time)[0]
    # total_units_no_outliers = remove_outliers(total_backtracks, total_time)[1]
    total_time_no_outliers = remove_outliers(total_backtracks, total_time)[1]

    mean_backtracks = sum(total_backtracks) / len(total_backtracks)
    mean_units = sum(total_units) / len(total_units)
    mean_time = sum(total_time) / len(total_time)

    values = []
    values.append(total_backtracks_no_outliers)
    values.append(total_units)
    values.append(total_time_no_outliers)
    values.append(mean_backtracks)
    values.append(mean_units)
    values.append(mean_time)

    return values

start = 1
heuristics = ['-H1', '-H2', '-H3']

if sys.argv[1] == '1' or sys.argv[1] == '3':
    size = 9

if sys.argv[1] == '2' or sys.argv[1] == '4':
    size = 16

stop = 3

total_values = []

for heuristic in heuristics:
    values = dpll_loop(start, stop, heuristic)
    total_values.append(values)

Path(f"{os.getcwd()}/results").mkdir(parents=True, exist_ok=True)

for i in range(len(total_values)):
    with open(f"results/result{heuristics[i]}", 'w') as output:
        for j in range(len(total_values[i])):
            output.write(f"{total_values[i][j]}\n")

plot_scatter_list_backtracks = []
plot_scatter_list_units = []
# plot_bar_list_units_number = []
marker = ['x', '+', '1', '2', '3', '4']
# width =0.35
# for values in total_values:
#     values[1] = sorted(values[1], reverse=True)

Path(f"{os.getcwd()}/graphs").mkdir(parents=True, exist_ok=True)

# Graph backtracks against time
for i in range(len(total_values)):
    plot_scatter_list_backtracks.append(plt1.scatter(total_values[i][0], total_values[i][2], marker=marker[i], linewidths=1))
    # plot_scatter_list_units.append(plt2.scatter(total_values[i][1], total_values[i][2], marker=marker[i], linewidths=1))
    # for j in range(len(total_values[i][1])):
    #     plot_bar_list_units.append(plt2.bar(heuristics[i], total_values[i][1][j], width))

#Graph unit clauses against time
# print(total_values[i][1])
# print(total_values[i][2])
# for i in range(len(total_values)):
#     plot_scatter_list_units.append(plt.scatter(total_values[i][1], total_values[i][2], marker=marker[i], linewidths=1))

plt1.xlabel('Number of backtracks')
plt1.ylabel('Time (sec)')
plt1.title(f'SAT Solver backtracks for sudokus {size}x{size}')

plt1.legend(plot_scatter_list_backtracks,
           heuristics,
           scatterpoints=1,
           bbox_to_anchor=(1.20, 1),
           borderaxespad=0)

# plt.autoscale()

plt1.tight_layout(rect=[0, 0, 1, 1])

plt1.savefig('graphs/backtrack_graph.png')

plt1.show()

# plt2.xlabel('Number of units')
# plt2.ylabel('Time (sec)')
# plt2.title(f'SAT Solver units for sudokus {size}x{size}')
#
# plt2.legend(plot_scatter_list_units,
#            heuristics,
#            scatterpoints=1,
#            bbox_to_anchor=(1.20, 1),
#            borderaxespad=0)
#
# # plt.autoscale()
#
# plt2.tight_layout(rect=[0, 0, 1, 1])
#
# plt2.savefig('graphs/unit_graph.png')
#
# plt2.show()
