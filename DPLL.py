import sys
from heuristics import DPLL
import datetime
import time

sys.setrecursionlimit(1000)


def main(argv, heuristic):
    if argv[0] == '-H1':
        print('Using: Random Split Heuristic.')
        sat_solver = DPLL(argv[1])
        sat_solver.split = 1
    elif heuristic == '-H1':
        print('Using: Random Split Heuristic.')
        sat_solver = DPLL(argv)
        sat_solver.split = 1
    elif argv[0] == '-H2':
        print('Using: Jeroslow-Wang Heuristic.')
        sat_solver = DPLL(argv[1])
        sat_solver.split = 2
    elif heuristic == '-H2':
        print('Using: Jeroslow-Wang Heuristic.')
        sat_solver = DPLL(argv)
        sat_solver.split = 2
    elif argv[0] == '-H3':
        print('Using: Last Encountered Free Variable.')
        sat_solver = DPLL(argv[1])
        sat_solver.split = 3
    elif heuristic == '-H3':
        print('Using: Last Encountered Free Variable.')
        sat_solver = DPLL(argv)
        sat_solver.split = 3
    else:
        print('Incorrect input. try calling again with the following format:')
        print("for Linux: 'sh SAT.sh -Hx DIMACS-file'")
        print("for Windows: 'SAT.bat -Hx DIMACS-file'")
        exit()
    print('Solving...')

    st = datetime.datetime.now()
    clauses = sat_solver.read_clauses()
    var = sat_solver.solve(clauses)
    et = datetime.datetime.now()
    elapsed_time = et - st

    if var is False:
        print('The problem is not solvable')
        sat_solver.output_results()
    else:
        sat_solver.output_results(var)
        print('SAT problem solved!')

    print('Execution time:', elapsed_time, 'seconds')

    values = []
    backtracks, units = sat_solver.get_measures()

    values.append(backtracks)
    values.append(units)
    values.append(elapsed_time.total_seconds())

    return values


if __name__ == '__main__':
    main(sys.argv[1:], heuristic = None)