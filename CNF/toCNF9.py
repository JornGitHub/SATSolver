"""
This file makes a CNF file of clauses on the sudoku's puzzle and rules
"""

# Import relevant packages
import sys
import os
from pathlib import Path

# Size of sudoku

SIZE = 9
SQUARE = 3
NUMBERS = {}
symbols = " 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(SIZE + 1):
    NUMBERS[symbols[i]] = i


# Extract the unsolved sudokus from a text file
def read_sudokus(filename: str):
    puzzles = []
    with open(filename, 'r', encoding='UTF-8') as handle:
        for line in handle.readlines():
            line = line.strip()
            line = [line[i:i + SIZE] for i in range(0, len(line), SIZE)]
            puzzles.append(line)
    return puzzles


# Transform the extracted sudokus into CNF files
def toCNF(sudoku, count):

    def var(r, c, v):
        return int(str(r)+str(c)+str(v))
    

    clauses = []

    # Add the clauses for all givens

    clausecounter = 0

    for row in range(1, SIZE+1):
        for column in range(1, SIZE+1):
            if sudoku[row-1][column-1] in NUMBERS.keys():
                clausecounter +=1
                clauses.append([var(row,column,NUMBERS[sudoku[row-1][column-1]])])

    

    file = open(f"CNF/CNF9/sudoku{count}.cnf", "w")
    file.write(f'p cnf 729 {str(11988 + clausecounter)}\n')
    for clause in clauses:
        file.write(' '.join([str(lit) for lit in clause]) + ' 0\n')

    with open('rules/rules9x9.txt') as f:
        for line in f:
            file.write(line)


if __name__ == '__main__':
    Path(f"CNF/CNF9").mkdir(parents=True, exist_ok=True)
    sudokus = read_sudokus(sys.argv[1])
    count = 1
    for sudoku in sudokus:
        toCNF(sudoku, count)
        count += 1
