# CS 76: Artificial Intelligence - PA5:Logic
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming and Mack Reiferson

# Import statements
import random


# A class that generalizes the SAT solving algorithms, GSAT and WalkSAT
class SAT:

    # Constructor for the SAT problem. This specific implementation will be using GSAT and Walksat to solve the SAT
    # problems. TODO: Finish this part... More to come
    def __init__(self, filename, max_flips, threshold):
        self.max_flips = max_flips
        self.threshold = threshold
        self.variables = set()
        self.clauses = list()
        self.assignment = dict()
        self.satisfied_clauses = []
        self.unsatisfied_clauses = []
        self.generate_clauses(filename)
        self.num_flips = 0

    # Generates the list of clauses and sets the variables list and all!
    def generate_clauses(self, filename):
        # First open up the file
        f = open(filename, "r")
        # Now we read the line which is a clause. Split by space
        clause_lines = f.readlines()
        for clause in clause_lines:
            clause_list = clause.split()
            # First we go through the list and add variables
            for variable in clause_list:
                if self.is_negated(variable):
                    variable = variable[1:]
                self.variables.add(variable)
            # Now we append this clause list into clauses
            self.clauses.append(clause_list)
        self.variables = list(self.variables)

    # The GSAT algorithm. GSAT and WalkSAT differ in the methods used to select which variable to flip. GSAT makes
    # the change which minimizes the number fo unsatisfied clauses in the new assignment, or with some probability
    # picks a variable at random.
    def gsat(self):
        # The inputs into GSAT are a set of clauses, the max number of flips
        # Random assignment of variables
        self.assignment = self.generate_random_assignment()
        # Now, for the maximum number of flips
        for flip in range(1, self.max_flips):
            # We need to see if the current assignment satisfies the clauses
            self.satisfied_clauses = []
            self.unsatisfied_clauses = []
            if self.satisfy():
                self.num_flips = flip
                return self.assignment
            print("GSAT flip: " + str(flip) + " with " + str(len(self.unsatisfied_clauses)) + " unsatisfied clauses left")
            # If we are not satisfied, then we need to either randomly flip a var, or score and flip. We start by
            # randomly flipping
            prob = random.random()
            if prob > self.threshold:
                self.random_flip(self.variables)
            # Otherwise , for each var, score how many clauses would be satisfied if var value were flipped.
            else:
                self.flip_var(clause_vars=self.variables)
        return None

    # The WalkSAT first picks clause unsatisfied by assignment, flips var in clause. This clause is picked at random
    # among the others. Variable that will result in fewest previously satisfied clauses becoming unsatisfied is
    # is picked, with some probability of picking one var at random.  Less calculations, less possibilities.
    def walksat(self):
        # First thing we want to do is get a random assignment of vars
        self.assignment = self.generate_random_assignment()
        # Now we run algorithm for the maximum number of flips
        for flip in range(self.max_flips):
            # If we are satisfied, then finish
            self.satisfied_clauses = []
            self.unsatisfied_clauses = []
            if self.satisfy():
                self.num_flips = flip
                return self.assignment
            print("Walksat flip: " + str(flip) + " with " + str(len(self.unsatisfied_clauses)) +
                  " unsatisfied clauses left")
            # Otherwise, we want to randomly select a clause from the unsatisfied clauses
            clause = self.select_random_clause()

            # First we check our random threshold
            prob = random.random()
            if prob > self.threshold:
                # If randomly, choose var randomly from clause and flip it
                self.random_flip(clause)
            else:
                # Otherwise, flip the var in the clause that maximizes the number of satisfied clauses
                self.flip_var(clause_vars=clause)
        return None

    # Generates a random assignment for the variables
    def generate_random_assignment(self):
        assignment = {key: None for key in self.variables}
        # Now assign a random boolean to each variable
        for key in assignment.keys():
            assignment[key] = bool(random.getrandbits(1))
        return assignment

    # Determines whether the current assignment satisfies all the clauses
    def satisfy(self):
        satisfied = False
        # Now, for each clause in a sentence, we need to figure out if it be true or not
        for clause in self.clauses:
            # Now we want to determine if the current assignment satisfies this singular clause. If so, we add it to
            # satisfied clauses and if not, to unsatisfied clauses
            eval_true = False
            for literal in clause:
                if not self.is_negated(literal):
                    # If a literal is true, and our assignment has it as true, then it is satisfied clause
                    if self.assignment[self.remove_negation(literal)]:
                        self.satisfied_clauses.append(clause)
                        eval_true = True
                        break
                elif self.is_negated(literal):
                    # If a literal is false, then we can be satisfied if our assignment is false
                    if not self.assignment[self.remove_negation(literal)]:
                        self.satisfied_clauses.append(clause)
                        eval_true = True
                        break
            # In the case we did not evaluate true, then the clause is actually unsatisfied.
            if not eval_true:
                self.unsatisfied_clauses.append(clause)
                satisfied = True
        # print("len unsat: " + str(len(self.unsatisfied_clauses)))
        return not satisfied

    # Determines if a symbol has been negated. (Does it have '-')
    def is_negated(self, literal):
        return "-" in literal

    # Remove negation if negated
    def remove_negation(self, literal):
        literal_var = literal
        if self.is_negated(literal):
            literal_var = literal[1:]
        return literal_var

    # This function returns number of clauses satisfied with the given var flip
    def num_satisfied(self, symbol):
        clauses_satisfied = 0
        # Now we go through the clauses and see which ones would become satisfied by checking if the unsatisfied clause
        # is in there
        for clause in self.unsatisfied_clauses:
            if symbol in clause:
                clauses_satisfied += 1
        return clauses_satisfied

    # This function returns number of clauses unsatisfied with given var flop
    def num_unsatisfied(self, symbol):
        clauses_unsatisfied = 0
        # This one is slightly different, for flipping the var does not necessarily mean that the clause would be true
        for clause in self.satisfied_clauses:
            if self.flip_literal(symbol) in clause:
                # if the flipped symbol is in the satisfied clauses, that tells us that flipping would indeed make that
                # literal false. however, there can still be another that makes it true
                still_true = False
                for literal in clause:
                    # make sure it is not the same literal
                    if not self.is_negated(literal):
                        if self.assignment[self.remove_negation(literal)] and literal != self.flip_literal(symbol):
                            still_true = True
                    elif self.is_negated(literal):
                        if not self.assignment[self.remove_negation(literal)] and literal != self.flip_literal(symbol):
                            still_true = True
                    # If there are no trues, then we have unsatisfied
                if not still_true:
                    clauses_unsatisfied += 1
        return clauses_unsatisfied

    def flip_literal(self, literal):
        if self.is_negated(literal):
            return literal[1:]
        else:
            return "-" + literal

    # Flips a var in the assignment, either randomly or by scores
    def flip_var(self, clause_vars=None):
        if clause_vars:
            max_satisfied_keys = []
            max_value = 0
            # Check if a clause was made satisfied or made unsatisfied
            for literal in clause_vars:
                variable = self.remove_negation(literal)
                current_value = self.assignment[variable]
                # Now we check, if i flip it, how many would we satisfy - how many would we unsatisfy
                if current_value:
                    # This means it is currently true in assignment. We need to check how many the false would satisfy
                    score = self.num_satisfied("-" + variable) - self.num_unsatisfied("-" + variable)
                else:
                    # This means that var is currently false in assignment. We need to check # true would satisfy
                    score = self.num_satisfied(variable) - self.num_unsatisfied(variable)
                # Now we check, do we have a max score?
                if score > max_value:
                    max_value = score
                    # Gotta reset our max_satisfied_keys
                    max_satisfied_keys = [variable]
                elif score == max_value:
                    max_satisfied_keys.append(variable)
            # Now that we have our max keys, choose one randomly

            if max_satisfied_keys:
                # print(max_value)
                key = random.choice(max_satisfied_keys)
                self.assignment[key] = not self.assignment[key]

    # Flips an assignment model and returns a copy of the assignment
    def flip_assignment(self, variable):
        new_assignment = dict(self.assignment)
        new_assignment[variable] = not new_assignment[variable]
        return new_assignment

    # Returns a random choice from the unsatisfied clauses to walksat
    def select_random_clause(self):
        return random.choice(self.unsatisfied_clauses)

    # From a clause, select a random variable and flip it
    def random_flip(self, clause):
        random_var = random.choice(clause)
        # Check if negated
        random_var = self.remove_negation(random_var)
        # Now flip
        self.assignment[random_var] = not self.assignment[random_var]

    # Writes the solution to a .sud file for the Sudoku display
    def write_solution(self, sol_filename):
        # We just need to print whether it is its symbol or negation of its symbol:
        f = open(sol_filename, "w")
        # Loop through assignment, write to file
        for key in self.assignment.keys():
            if self.assignment[key]:
                # If we are true, them write that true symbol and go on
                f.write(key + "\n")
            elif not self.assignment[key]:
                # Now we just add a negative sign to indicate it the opposite symbol
                f.write("-" + key + "\n")
        f.close()
