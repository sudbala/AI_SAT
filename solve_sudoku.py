from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    display_sudoku_solution("test.sol")

    # puzzle_name = str(sys.argv[1][:-4])
    # sol_filename = puzzle_name + ".sol"
    puzzle_name = "puzzle1"
    sol_filename = puzzle_name + ".sol"

    # sat = SAT("one_cell.cnf")
    # sat = SAT("rows.cnf")
    sat = SAT("puzzle1.cnf")

    print(sat.clauses)
    print(" ")
    print(sat.variables)

    assignment = sat.walksat()
    print(assignment)

    if assignment:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
