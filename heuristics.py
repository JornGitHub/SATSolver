import random
import copy
from collections import defaultdict
from pathlib import Path
import os


class DPLL(object):

    def __init__(self, file):
        self.file = file
        self.split = 0
        self.backtrack = 0
        self.unassigned_var = 0
        self.presence = 0
        self.units = 0

    # Choose the given heuristic

    def split_choice(self, clauses):
        
        if self.split == 1:
            return self.random_split(clauses)
        elif self.split == 2:
            return self.JW_heuristic(clauses)
        elif self.split == 3:
            return self.LEFV_heuristic(clauses)

    # Main solve function

    def solve(self, clauses):

        # Remove tautologies
        clauses = self.remove_tautologies(clauses)
        
        # Remove unit clauses
        clauses = self.unit_clauses(clauses)

        # Update clauses by checking for pure literals
        clauses = self.pure_literals(clauses)
        
        # If there is an empty clause in the set, return False
        if [] in clauses:
            return False

        # If the set is an empty clause, return True
        if len(clauses) == 0:
            return self.vars
        
        # Pick new variable to assign with chosen heuristic
        split_var = self.split_choice(clauses)
        # Keep track of the current clauses
        prevClauses = copy.deepcopy(clauses)

        # Assign positive or negative value to picked variable
        assignment = self.solve(self.remove_clauses(split_var, clauses))
        if assignment is False:
            self.backtrack += 1
            clauses = copy.deepcopy(prevClauses)
            assignment = self.solve(self.remove_clauses(-split_var, clauses))
        if assignment is False:
            return False

        return self.vars

    def random_split(self, clauses):

        clause = random.choice(clauses)
        split = random.choice(clause)
        return split

    # Remove clauses if the assignment is positive, shorten clauses if the assignment is negative

    def remove_clauses(self, variable, clauses):

        new_clauses = []
        if variable is not None:
            if variable >= 0:
                self.vars[variable] = True
            else:
                self.vars[abs(variable)] = False
            for clause in clauses:
                if variable in clause:
                    continue
                else:
                    if -variable in clause:
                        clause.remove(-variable)
                    new_clauses.append(clause)
                    if clause != []:
                        self.unassigned_var = clause[-1]  # for LAFV
        return new_clauses

    # Take CNF file as input

    def read_clauses(self):

        # Initialize clauses & variables
        clauses = []
        allVars = set()
        print(self.file)

        # Read input file
        with open(self.file, 'r') as input_file:
            for line in input_file:
                clauseLine = line.split()
                # Skip the first line if necessary
                if not clauseLine or clauseLine[0] == 'p' or clauseLine[0] == 'c':
                    continue
                # Extract the variables from the clauses and add both to their respective data structure
                else:
                    realClause = clauseLine[:-1]
                    clause = set()
                    for lit in realClause:
                        lit = int(lit)
                        clause.add(lit)
                        abs_lit = abs(lit)
                        allVars.add(abs_lit)
                    clauses.append(list(clause))
        
        self.vars = dict.fromkeys(allVars, False)
        return clauses

    # Check and remove clauses containing tautologies

    def remove_tautologies(self, clauses):

        new_clauses = []
        check = 1
        for clause in clauses:
            for lit in clause:
                if -lit in clause:
                    check = 0
                    break
            if check == 1:
                new_clauses.append(clause)
            else:
                check = 1
        return new_clauses

     # Check and remove clauses containing pure literals

    def pure_literals(self, clauses):

        p_lits = set()
        non_p_lits = set()
        for clause in clauses:
            for lit in clause:
                neg_lit = -lit
                abs_lit = abs(lit)
                if neg_lit not in p_lits:
                    if abs_lit not in non_p_lits:
                        p_lits.add(lit)
                else:
                    p_lits.remove(neg_lit)
                    non_p_lits.add(abs_lit)
        for lit in p_lits:
            clauses = self.remove_clauses(lit, clauses)
        return clauses

    # Check and remove clauses containing unit literals

    def unit_clauses(self, clauses):

        unit_var = set()
        for clause in clauses:
            if len(clause) == 1:
                self.units +=1
                unit_var.add(clause[0])
        while len(unit_var) > 0:
            for unit in unit_var:
                clauses = self.remove_clauses(unit, clauses)
            unit_var = set()
            clauses = self.unit_clauses(clauses)
        return clauses

    #Jeroslow Wang implementation

    def JW_heuristic(self, clauses):

        # Assign weights based on clause length & frequency

        J = defaultdict(int)
        for clause in clauses:
            clause_len = len(clause)
            for lit in clause:
                J[lit] += 2 ** (-clause_len)

        choices = []
        vals = []
        Jx = J.copy()
        for k, v in Jx.items():
            lit = abs(k)
            if lit not in choices:
                choices.append(lit)
                vals.append(J[k] + J[-k])

        # Pick a variable with priority based on their weights

        split = random.choices(choices, weights=vals, k=1)
        split = split[0]
        split = random.choices([split, -split], weights=[J[split], J[-split]], k=1)
        split = split[0]
        return split

    # Last Encountered Free Variable implementation

    def LEFV_heuristic(self, clauses):

        # During unit propagation save the last unassigned variable you see, if the variable is still unassigned at decision time use it otherwise choose a random

        if self.presence == 0:
            for clause in clauses:
                if self.unassigned_var in clause:
                    self.presence = 1
                    break
        if self.presence == 1:
            split = self.unassigned_var
        else:
            split = self.random_split(clauses)

        return split
    
    # Helper variable for output

    def output_results(self, vars=None):

        Path(f"{os.getcwd()}/solutions").mkdir(parents=True, exist_ok=True)

        input_file_name = self.file.split('/')
        input_file_name = input_file_name[-1]
        output_file = input_file_name[:-4] + '.out'
        if vars is None:
            with open(f"solutions/{output_file}", 'w') as output:
                output.write('')
        else:
            assignments = []
            for k, v in vars.items():
                if v:
                    assignments.append(str(k) + ' 0\n')
                else:
                    assignments.append(str(-k) + ' 0\n')
            with open(f"solutions/{output_file}", 'w') as output:
                output.write('p cnf {} {}\n'.format(len(vars), len(vars)))
                output.writelines(assignments)

    def get_measures(self):
        return self.backtrack, self.units
