# CS 76: Artificial Intelligence - PA5:Logic
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming and Mack Reiferson

# Import statements
from Sudoku import Sudoku
import sys


# Couple functions used to display the sudoku solution in sudoku format
def display_sudoku_solution(filename):

    test_sudoku = Sudoku()
    test_sudoku.read_solution(filename)
    print(test_sudoku)


# Main function for testing
if __name__ == "__main__":
    display_sudoku_solution(sys.argv[1])
