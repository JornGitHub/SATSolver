import sys
import os
from pathlib import Path
import math
from random import sample

SIZE = int(sys.argv[1])
amount = int(sys.argv[2])
length = int(math.sqrt(SIZE))
square = length * length


def generate_sudoku():
    file = open(f"generators/{SIZE}x{SIZE}.txt", "w")

    # requirements for a lengthline valid solution
    def requirements(row, columns):
        return (length * (row % length) + row // length + columns) % square

    # randomize rows, columns and numbers (of valid length requirements)
    def shuffle(sudoku):
        return sample(sudoku, len(sudoku))

    rowLength = range(length)
    rows = [grid * length + row for grid in shuffle(rowLength) for row in shuffle(rowLength)]
    cols = [grid * length + column for grid in shuffle(rowLength) for column in shuffle(rowLength)]
    nums = shuffle(range(1, length * length + 1))

    symbol = " 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def expandLine(line):
        return line[0] + line[5:9].join([line[1:5] * (length - 1)] * length) + line[9:13]

    line0 = expandLine("╔═══╤═══╦═══╗")
    line1 = expandLine("║ . │ . ║ . ║")
    line2 = expandLine("╟───┼───╫───╢")
    line3 = expandLine("╠═══╪═══╬═══╣")
    line4 = expandLine("╚═══╧═══╩═══╝")

    for i in range(amount):
        # produce full sudoku using randomized lengthline requirements
        nums = shuffle(range(1, length * length + 1))
        board = [[nums[requirements(row, column)] for column in cols] for row in rows]

        # nums = [[""] + [symbol[n] for n in row] for row in board]
        # print(line0)
        # for r in range(1, square + 1):
        #     print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
        #     print([line2, line3, line4][(r % square == 0) + (r % length == 0)])

        squares = square * square
        empties = squares * int(sys.argv[3]) // 4

        for p in sample(range(squares), empties):
            board[p // square][p % square] = 0

        numSize = len(str(square))

        right_format = []
        for line in board:
            row = ""
            for digit in line:
                if digit != 0:
                    row = row + symbol[digit]
                else:
                    row = row + "."
            right_format.append(row)

        for row in right_format:
            file.write(row)

        file.write('\n')


if __name__ == '__main__':
    file = open(f"generators/{SIZE}x{SIZE}.txt", "w")
    generate_sudoku()
