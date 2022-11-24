from random import randint, shuffle
from time import sleep
import copy
import time
import sys

# How many times do you want to try to make a solvable sudoku pair?
iterations = int(sys.argv[1])

pairs = 0

with open("generators/pair16x16.txt", "w") as f1, open("generators/pair9x9.txt", "w") as f2:

  for i in range(iterations):
    print(i, "iterations")

    # Update the starting time of each iteration
    starttime = time.time()

    # How many times do you want to try to make a solvable sudoku? More attempts results in a harder sudoku & a lower amount of pairs created
    attempts = int(sys.argv[2])

    #initialise empty 16 by 16 grid
    grid = []
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


    #A function to checks if the grid is full
    def checkGrid(grid):
      for row in range(0,16):
          for col in range(0,16):
            if grid[row][col]==0:
              return False  
      return True 

    # A function to check all possible combinations (16x16) of numbers until a solution is found
    def solveGrid(grid):
      global counter
      #Find next empty cell
      for i in range(0,256):
        row=i//16
        col=i%16
        if grid[row][col]==0:
          for value in range (1,17):
            #Check that this value has not already been used in this row
            if not(value in grid[row]):
              #Check that this value has not already be used in this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col],
                                grid[9][col],grid[10][col],grid[11][col],grid[12][col],grid[13][col],grid[14][col],grid[15][col]):
                #Identify in which subgrid we are
                square=[]
                if row<4:
                  if col<4:
                    square=[grid[i][0:4] for i in range(0,4)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(0,4)]
                  elif col<12:
                    square=[grid[i][8:12] for i in range(0,4)]
                  else:  
                    square=[grid[i][12:16] for i in range(0,4)]
                elif row<8:
                  if col<4:
                    square=[grid[i][0:4] for i in range(4,8)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(4,8)]
                  elif col<12:  
                    square=[grid[i][8:12] for i in range(4,8)]
                  else:  
                    square=[grid[i][12:16] for i in range(4,8)]
                elif row<12:
                  if col<4:
                    square=[grid[i][0:4] for i in range(8,12)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(8,12)]
                  elif col<12:  
                    square=[grid[i][8:12] for i in range(8,12)]
                  else:  
                    square=[grid[i][12:16] for i in range(8,12)]
                else:
                  if col<4:
                    square=[grid[i][0:4] for i in range(12,16)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(12,16)]
                  elif col<12:  
                    square=[grid[i][8:12] for i in range(12,16)]
                  else:  
                    square=[grid[i][12:16] for i in range(12,16)]
                #Check that this value has not already be used in the subgrid
                if not value in (square[0] + square[1] + square[2] + square[3]):
                  grid[row][col]=value
                  if checkGrid(grid):
                    counter+=1
                    break
                  if starttime + 10 < time.time():
                    break
                  else:
                    if solveGrid(grid):
                      return True
          break
      grid[row][col]=0

    if starttime + 10 < time.time():
      continue

    #A function to check if the grid is full
    def checkGridSmall(grid):
      for row in range(0,9):
          for col in range(0,9):
            if grid[row][col]==0:
              return False
  
      return True 

    # A function to check all possible combinations (9x9) of numbers until a solution is found
    def solveGridSmall(grid):
      global solvetrys
      global counter
      solvetrys += 1
      #Find next empty cell
      for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col]==0:
          for value in range (1,10):
            #Check that this value has not already been used in this row
            if not(value in grid[row]):
              #Check that this value has not already be used in this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                #Identify in which subgrid we are
                square=[]
                if row<3:
                  if col<3:
                    square=[grid[i][0:3] for i in range(0,3)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(0,3)]
                  else:  
                    square=[grid[i][6:9] for i in range(0,3)]
                elif row<6:
                  if col<3:
                    square=[grid[i][0:3] for i in range(3,6)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(3,6)]
                  else:  
                    square=[grid[i][6:9] for i in range(3,6)]
                else:
                  if col<3:
                    square=[grid[i][0:3] for i in range(6,9)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(6,9)]
                  else:  
                    square=[grid[i][6:9] for i in range(6,9)]
                #Check that this value has not already be used in the subgrid
                if not value in (square[0] + square[1] + square[2]):
                  grid[row][col]=value
                  if checkGridSmall(grid):
                    counter+=1
                    break
                  if solvetrys > 100:
                    break
                  if starttime + 10 < time.time():
                    break
                  else:
                    if solveGridSmall(grid):
                      return True
          break
      grid[row][col]=0

    # Time condition
    if starttime + 10 < time.time():
      continue

    # Numbers to pick from
    numberList=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

    # A function to check all possible combinations of numbers until a solution is found
    def fillGrid(grid):
      global counter
      #Find next empty cell
      for i in range(0,256):
        row=i//16
        col=i%16
        if grid[row][col]==0:
          shuffle(numberList)
          for value in numberList:
            #Check that this value has not already been used in this row
            if not(value in grid[row]):
              #Check that this value has not already be used in this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col],
                                grid[9][col],grid[10][col],grid[11][col],grid[12][col],grid[13][col],grid[14][col],grid[15][col]):
                #Identify in which subgrid we are
                square=[]
                if row<4:
                  if col<4:
                    square=[grid[i][0:4] for i in range(0,4)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(0,4)]
                  elif col<12:
                    square=[grid[i][8:12] for i in range(0,4)]
                  else:  
                    square=[grid[i][12:16] for i in range(0,4)]
                elif row<8:
                  if col<4:
                    square=[grid[i][0:4] for i in range(4,8)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(4,8)]
                  elif col<12:  
                    square=[grid[i][8:12] for i in range(4,8)]
                  else:  
                    square=[grid[i][12:16] for i in range(4,8)]
                elif row<12:
                  if col<4:
                    square=[grid[i][0:4] for i in range(8,12)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(8,12)]
                  elif col<12:  
                    square=[grid[i][8:12] for i in range(8,12)]
                  else:  
                    square=[grid[i][12:16] for i in range(8,12)]
                else:
                  if col<4:
                    square=[grid[i][0:4] for i in range(12,16)]
                  elif col<8:
                    square=[grid[i][4:8] for i in range(12,16)]
                  elif col<12:  
                    square=[grid[i][8:12] for i in range(12,16)]
                  else:  
                    square=[grid[i][12:16] for i in range(12,16)]
                #Check that this value has not already be used in the subgrid
                if not value in (square[0] + square[1] + square[2] + square[3]):
                  grid[row][col]=value
                  if checkGrid(grid):
                    return True
                  if starttime + 10 < time.time():
                    break
                  else:
                    if fillGrid(grid):
                      return True
          break
      grid[row][col]=0

    # Time condition

    if starttime + 10 < time.time():
      continue

    # Fill up the 16x16 sudoku

    fillGrid(grid)

    # Number list to pick from 9x9

    numberList=[1,2,3,4,5,6,7,8,9]


    def fillGridSmall(grid):
      global counter
      #Find next empty cell
      for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col]==0:
          shuffle(numberList)      
          for value in numberList:
            #Check that this value has not already be used on this row
            if not(value in grid[row]):
              #Check that this value has not already be used on this column
              if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
                #Identify in which subgrid we are
                square=[]
                if row<3:
                  if col<3:
                    square=[grid[i][0:3] for i in range(0,3)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(0,3)]
                  else:  
                    square=[grid[i][6:9] for i in range(0,3)]
                elif row<6:
                  if col<3:
                    square=[grid[i][0:3] for i in range(3,6)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(3,6)]
                  else:  
                    square=[grid[i][6:9] for i in range(3,6)]
                else:
                  if col<3:
                    square=[grid[i][0:3] for i in range(6,9)]
                  elif col<6:
                    square=[grid[i][3:6] for i in range(6,9)]
                  else:  
                    square=[grid[i][6:9] for i in range(6,9)]
                #Check that this value has not already be used in the subgrid
                if not value in (square[0] + square[1] + square[2]):
                  grid[row][col]=value
                  if checkGridSmall(grid):
                    return True
                  if starttime + 10 < time.time():
                    break
                  else:
                    if fillGridSmall(grid):
                      return True
          break
      grid[row][col]=0             
        
    #Time condition
    if starttime + 10 < time.time():
      continue

    # Count the amount of solutions
    counter=1

    # Try to create a special 16x16 sudoku with a unique solution
    while attempts > 0:
      #Select a random cell in the lower right corner of the 16x16 that is not already empty
      row = randint(7,15)
      col = randint(7,15)
      while grid[row][col]==0:
        row = randint(7,15)
        col = randint(7,15)
      #Remember its cell value in case we need to put it back  
      backup = grid[row][col]
      grid[row][col]=0
      
      #Take a full copy of the sudoku
      copyGrid = copy.deepcopy(grid)

      #Count the number of solutions that this grid has
      counter=0      
      solveGrid(copyGrid)   
      #If there is no unique solution, then we put the value back and try again
      if counter!=1:
        grid[row][col]=backup
        #Try again to find an even harder puzzle
        attempts -= 1


    # Register where the empty spots in the large grid are located adjusted for the 9x9 sudoku
    emptys = []
    for row in range(len(grid)):
      for column in range(len(grid)):
        if grid[row][column] == 0:
          emptys.append([row - 7,column - 7])


    # Create a smaller 9x9 grid
    smallGrid = []
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    smallGrid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    #Time condition
    if starttime + 10 < time.time():
      continue


    # Fill up the small sudoku
    fillGridSmall(smallGrid)

    # Put empty spaces in similar spots as the 16x16
    for i in emptys:
      smallGrid[i[0]][i[1]] = 0

    # Create boolean value for solvability
    isSolvable = False

    # Try to find a solution for the 9x9 sudoku
    counter=1
    trys = 0
    solvetrys = 0
    while isSolvable == False and trys < 10:
      counter=0
      solveGridSmall(smallGrid)
      trys += 1
      if counter == 1:
        isSolvable = True

    # If we created a 16x16, and a 9x9 with empty spaces in the same spot as the 16x16, 
    # then we succeeded in finding a similar pair and can write the sudokus to a file

    if isSolvable == True:
      pairs += 1
      format_grid = []

      for row in grid:
          ROW = ''
          for i in range(len(row)):
              if row[i] == 0:
                  ROW += '.'
              elif row[i] == 10:
                  ROW += 'A'
              elif row[i] == 11:
                  ROW += 'B'
              elif row[i] == 12:
                  ROW += 'C'
              elif row[i] == 13:
                  ROW += 'D'
              elif row[i] == 14:
                  ROW += 'E'
              elif row[i] == 15:
                  ROW += 'F'
              elif row[i] == 16:
                  ROW += 'G'
              else:
                  ROW += str(row[i])
          format_grid.append(ROW)


      for row in format_grid:
          f1.write(row)

      f1.write('\n')
      
      format_smallGrid = []

      for row in smallGrid:
          ROW = ''
          for i in range(len(row)):
              if row[i] == 0:
                  ROW += '.'
              else:
                  ROW += str(row[i])
          format_smallGrid.append(ROW)

      for row in format_smallGrid:
          f2.write(row)

      f2.write('\n')

print(f"Created {pairs} pairs")
