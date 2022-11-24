# SATsolver

This repo contains a DPLL SAT solver with 4 different heuristics:

- random split
- Jeroslow-Wang (JW)
- Conflict-Depedent Clause Learner (CDCL)
- Last Evaluated Free Variable (LEVF)

There is a testset split up in 4 different categories, 2 normal 9x9 and 16x16 sudoku sets. Additionally, there are specially made paired 9x9 & 16x16 sudokus.
The paired sudokus are generated so that the bottom right of the 16x16 sudoku matches the 9x9 sudoku in terms of its empty spots.
This is done to try and test the impact of additional constraints on a similar sudoku, the research question we try to aswer.

The repo contains sudoku generators (normal and paired). Run the normal generator with the following input:

    python3 generators/sudoku_generator.py 9 10 2

Here 9 represents the size of the sudoku, 10 the amount of sudokus to make, and 2, the amount of empty spots in the generated sudoku. The generated sudokus can be found in /generators as {size}x{size}.txt.

To create paired sudokus, run:

    python3 generators/sudoku_pair.py 10 1

Here, 10 represents the amount of iterations, and 1 the amount of times the script retries to come up with a pair. It is not always possible
to create a matching solvable pair, so the amount of iterations does not equal the amount of pairs that are received. The generated paired sudokus can be found in /generators as pair{size}x{size}.txt.

To convert the created sudokus to CNF format run:

    python3 CNF/toCNF{size}.py generators/{txt_file}.txt

Where the first input gives the CNF converter we want to use (toCNF9 for 9x9 & toCNF16 for 16x16), and the second input is the sudoku we want to convert.
The paired sudokus can be formatted by this function by using e.g. generators/pair9x9.txt as the second argument.

The result will be stored in CNF/CNF{size} and is ready to be transfered to the test directory for testing.

To run a single sudoku on a single heuristic use:

     python3 DPLL.py -H1 test/normal_sudokus9x9/sudoku1.cnf

Where -H1 is the chosen implementation followed by the input filename.
The possible implementations are as follows: H1) Random heuristic, H2) Jeroslow-Wang heuristic, H3) LEFV

The solution file is the stored in solutions/filename.out (empty file if unsolvable)

To run all 3 heuristics simultaneously on a large testset run:

    python3 DPLLoop.py 1

Use input 1 for normal9x9, 2 for normal16x16, 3 for special9x9, and 4 for special16x16.



