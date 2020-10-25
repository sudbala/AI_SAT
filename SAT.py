
import random
import copy


# WORK IN PROGRESS
class SAT:

    # Constructor for the SAT problem. This specific implementation will be using GSAT and Walksat to solve the SAT
    # problems. TODO: Finish this part... More to come
    def __init__(self, filename):
        # TODO: Tries, flips, clauses, threshold, variable list
        self.max_tries = 2
        self.max_flips = 729
        self.threshold = 0.5
        self.variables = set()
        self.clauses = list()
        self.generate_clauses(filename)
        random.seed(1)

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

    # The GSAT algorithm. GSAT and WalkSAT differ in the methods used to select which variable to flip. GSAT makes
    # the change which minimizes the number fo unsatisfied clauses in the new assignment, or with some probability
    # picks a variable at random.
    def gsat(self):
        # The inputs into GSAT are a set of clauses, the max number of flips, and the max number of tries
        # We start by doing this algorithm for a number of tries
        for gsat_try in range(1, self.max_tries):
            # Random assignment of variables
            assignment = self.generate_random_assignment()
            # Now, for the maximum number of flips
            for flip in range(1, self.max_flips):
                print("flip: " + str(flip))
                # We need to see if the current assignment satisfies the clauses
                satisfied_clauses = []
                unsatisfied_clauses = []
                if self.satisfy(assignment, satisfied_clauses, unsatisfied_clauses):
                    return assignment
                # If we are not satisfied, then we need to either randomly flip a var, or score and flip. We start by
                # randomly flipping
                prob = random.random()
                if prob > self.threshold:
                    self.flip_var(assignment, True)
                # Otherwise , for each var, score how many clauses would be satisfied if var value were flipped.
                else:
                    self.flip_var(assignment)
        return None

    # Generates a random assignment for the variables
    def generate_random_assignment(self):
        assignment = {key: None for key in self.variables}
        # Now assign a random boolean to each variable
        for key in assignment.keys():
            assignment[key] = bool(random.getrandbits(1))
        return assignment

    # Determines whether the current assignment satisfies all the clauses
    def satisfy(self, assignment, satisfied_clauses, unsatisfied_clauses):
        # Now, for each clause in a sentence, we need to figure out if it be true or not
        for clause in self.clauses:
            # Now we want to determine if the current assignment satisfies this singular clause. If so, we add it to
            # satisfied clauses and if not, to unsatisfied clauses
            if self.is_true_clause(clause, assignment):
                satisfied_clauses.append(clause)
            else:
                unsatisfied_clauses.append(clause)
        # Check the length of unsatisfied clause, if no length, we are done! Otherwise false
        if len(unsatisfied_clauses) == 0:
            return True
        return False

    # Determines if a clause is true given the assignment
    def is_true_clause(self, clause, assignment):
        # We need to check every single literal in the clause
        is_negated = False
        is_true_clause = False
        for literal in clause:
            # First we need to check if we have a not sign in this literal
            if self.is_negated(literal):
                is_negated = True
                literal_symbol = literal[1:]
            else:
                literal_symbol = literal
            # Now grab the value of this symbol from the assignment
            assignment_value = assignment[literal_symbol]
            # Now, we return true if true; this occurs in two cases: If the assignment value is true, and our symbol
            # has not been negated OR if value is false but the symbol has been negated. Either way, its true
            if (assignment_value and not is_negated) or (not assignment_value and is_negated):
                is_true_clause = True
                break
        # As soon as it is true, the entire clause is true. Or we go all the way through and it is not
        return is_true_clause

    # Determines if a symbol has been negated. (Does it have '-')
    def is_negated(self, literal):
        return "-" in literal

    # Flips a var in the assignment, either randomly or by scores
    def flip_var(self, assignment, random_var=False):
        # Check if we are flipping a random var
        if random_var:
            key = random.choice(list(assignment.keys()))
            assignment[key] = not assignment[key]
        # If not, we gotta do it based on score
        else:
            made_satisfied = dict.fromkeys(assignment.keys(), 0)
            made_unsatisfied = dict.fromkeys(assignment.keys(), 0)
            # Check if a clause was made satisfied or made unsatisfied
            for variable in self.variables:
                for clause in self.clauses:
                    satisfied = self.is_true_clause(clause, assignment)
                    result = self.is_true_clause(clause, self.flip_assignment(assignment, variable))
                    if not satisfied and result:
                        made_satisfied[variable] += 1
                    elif satisfied and not result:
                        made_unsatisfied[variable] += 1
            # Now we get the differences between what satisfied and unsatisfied
            net_satisfied = dict.fromkeys(assignment.keys(), 0)
            for key in made_satisfied.keys():
                net_satisfied[key] = made_satisfied[key] - made_unsatisfied[key]
            # Now we get the max keys
            max_value = max(net_satisfied.values())
            print(max_value)
            max_keys = [k for k, v in net_satisfied.items() if v == max_value]
            # Make a random choice of key
            var_to_flip = random.choice(max_keys)
            assignment[var_to_flip] = not assignment[var_to_flip]

    # Flips an assignment model and returns a copy of the assignment
    def flip_assignment(self, assignment, variable):
        new_assignment = dict(assignment)
        new_assignment[variable] = not new_assignment[variable]
        return new_assignment

    # The WalkSAT first picks clause unsatisfied by assignment, flips var in clause. This clause is picked at random
    # among the others. Variable that will result in fewest previously satisfied clauses becoming unsatisfied is
    # is picked, with some probability of picking one var at random.  Less calculations, less possibilities.
    def walksat(self):
        # First thing we want to do is get a random assignment of vars
        assignment = self.generate_random_assignment()
        # Now we run algorithm for the maximum number of flips
        for flip in range(self.max_flips):
            # If we are satisfied, then finish
            satisfied_clauses = []
            unsatisfied_clauses = []
            if self.satisfy(assignment, satisfied_clauses, unsatisfied_clauses):
                return assignment
            # Otherwise, we want to randomly select a clause from the unsatisfied clauses
            clause = self.select_random_clause(unsatisfied_clauses)

            # First we check our random threshold
            prob = random.random()
            if prob < self.threshold:
                self.random_flip(assignment, clause)

    # Returns a random choice from the unsatisfied clauses to walksat
    def select_random_clause(self, unsatisfied_clauses):
        return random.choice(unsatisfied_clauses)

    # From a clause, select a random variable and flip it
    def random_flip(self, assignment, clause):
        random_var = random.choice(clause)
        # Check if negated
        if self.is_negated(random_var):
            random_var = random_var[1:]
        # Now flip
        assignment[random_var] = not assignment[random_var]
#
# if __name__ == "__main__":
#