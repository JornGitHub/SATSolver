import sys
import os
from pathlib import Path

# Size of sudoku

SIZE = 16
SQUARE = 4
NUMBERS = {}
symbols = " 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(SIZE+1):
    NUMBERS[symbols[i]] = i


# Extract the unsolved sudokus from a text file

def read_sudokus(filename: str):
    puzzles = []
    with open(filename, 'r', encoding='UTF-8') as handle:
        for line in handle.readlines():
            line = line.strip()
            line = [line[i:i+SIZE] for i in range(0, len(line), SIZE)]
            puzzles.append(line)
    return puzzles

# Transform the extracted sudokus into CNF files

def toCNF(sudoku, count):

    # This encodes the literals in a way that makes the dpll work

    def var(r, c, v):
        
        return int(str(r)+str(c)+str(v))

    def pseudo_base(r, c, v):
        pseudo_base = (SIZE + 1) if SIZE > 10 else 10
        return r * pseudo_base**2 + c * pseudo_base + v
    

    clauses = []

    # Add the clauses for all givens

    clausecounter = 0

    for row in range(1, SIZE+1):
        for column in range(1, SIZE+1):
            if sudoku[row-1][column-1] in NUMBERS.keys():
                clausecounter +=1
                clauses.append([pseudo_base(row,column,NUMBERS[sudoku[row-1][column-1]])])

    file = open(f"CNF/CNF16/sudoku{count}.cnf", "w")

    file.write(f'p cnf 4096 {str(123904 + clausecounter)}\n')

    for clause in clauses:
        file.write(' '.join([str(lit) for lit in clause])+' 0\n')

    with open('rules/rules16x16.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines()[1:]:
            file.write(line.strip() + "\n")


if __name__ == '__main__':
    Path(f"CNF/CNF16").mkdir(parents=True, exist_ok=True)
    sudokus = read_sudokus(sys.argv[1])
    count = 1
    for sudoku in sudokus:
        toCNF(sudoku, count)
        count += 1