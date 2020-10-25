# CS 76: Artificial Intelligence - PA5:Logic
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming and Mack Reiferson

import random
import sys

from SAT import SAT
from display import display_sudoku_solution

# Main class developed for testing of the SAT solvers.
if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    # Grab the method of solving you want
    method = str(sys.argv[2]).lower()

    # Instantiation of the SAT solver
    sat = SAT(sys.argv[1], 100000, 0.8)

    assignment = None
    if method == 'gsat':
        assignment = sat.gsat()
    elif method == 'walksat':
        assignment = sat.walksat()
    else:
        print("Incorrect Assignment:\n"
              "Usage: /solve_sudoku.py <file.cnf> <gsat/walksat>")
        exit(1)
    print(str(assignment) + "\n")

    if assignment:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
        print(puzzle_name + " solved in " + str(sat.num_flips) + " flips with " + method + " solver")

