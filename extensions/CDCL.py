import random
import copy
from collections import defaultdict
from pathlib import Path
import os
import sys
from itertools import product

digits = "0123456789ABCDEFG"
unused = []
used = []
for a, b, c in product(digits[1:], digits, digits):
  num17 = a+b+c
  numdec = int(num17, 17)
  if "0" in num17:
    continue
  else:
    used.append(numdec)


unused = unused[18:]  # removing the ones below "111" / 307

class CDCL(object):

    def __init__(self, file):
        self.file = file
        self.backtracks = 0
        self.variables = 0
        self.learned_clauses = 0
        self.implications = 0
        self.splits = 0
        self.units = 0

    # Take CNF file as input

    def read_clauses(self):

        # Initialize clauses & variables
        clauses = []
        allVars = set()

        # Read input file
        with open(self.file, 'r') as input_file:
            for line in input_file:
                clauseLine = line.split()
                # Skip the first line if necessary
                if not clauseLine or clauseLine[0] == 'c':
                    continue
                # Learn the amount of variables
                elif clauseLine[0] == 'p':
                    self.variables = int(clauseLine[2])
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

    # Run BCP/unit only once at the start of the run

    def boolean_constraint_propagation(self, clauses, literal):
        new_clauses = [clause[:] for clause in clauses] 
        for clause in reversed(new_clauses):
            if literal in clause:                     
                new_clauses.remove(clause)                    
            if -literal in clause:                     
                clause.remove(-literal)                         
                if not clause:                         
                    return -1
        return new_clauses

    def unit_propagation(self, clauses):               
        assignment = []
        propagating = True
        while propagating:                           
            propagating = False
            for clause in clauses:                    
                if len(clause) == 1:                 
                    unit=clause[0]
                    clauses = self.boolean_constraint_propagation(clauses, unit)
                    self.units += 1
                    assignment += [unit]
                    propagating = True
                if clauses == -1:                
                    return -1, []
                if not clauses:                   
                    return clauses, assignment

        assignment = list(set(assignment))
        return clauses, assignment

    # Main solve function
    
    def solve(self, num_var):
        clauses = self.read_clauses()
        decision_level = []                             
        assignments = []                                      
        clauses, assignments = self.unit_propagation(clauses)                       
        count = self.VSIDS_heuristic(clauses)
        
        literal_watchers, clauses_watched_by_literals = self.create_watchers(clauses,assignments)
        while self.variables > len(assignments):             
            variable = self.VSIDC_split(count, assignments)                     
            self.splits += 1 
            decision_level.append(len(assignments))
            assignments.append(variable)
            conflict,literal_watchers = self.watch_propagation(clauses,literal_watchers,clauses_watched_by_literals,assignments,variable)         
            while conflict != -1 :
                self.conflict_counter(count, conflict)
                count = self.decay_scores(count)

                learned_clause = self.analyze_conflict(assignments, conflict, decision_level)      

                level = self.learn_clause(clauses,literal_watchers,clauses_watched_by_literals,learned_clause,assignments) 
                self.learned_clauses += 1
                backtrack_location,variable,self.implications = self.backtrack(assignments, level, decision_level)      

                if backtrack_location == -1:                                     
                    return -1
                assignments.append(variable)                                            
                
                conflict,literal_watch = self.watch_propagation(clauses,literal_watchers,clauses_watched_by_literals,assignments,variable)
       

        return assignments

    # Create watcher literals tracking the clauses

    def create_watchers(self, clauses, assignments):
        literal_watchers = {}
        clauses_watched_by_literals= []

        # Map the literal watchers to empty lists

        if self.variables == 729:
            for i in range(999,110, -1):
                if '0' in str(i):
                    continue
                literal_watchers[-i] = []

            for i in range(111,1000):
                if '0' in str(i):
                    continue
                literal_watchers[i] = []

        elif self.variables == 4096:
            for i in reversed(used):
                literal_watchers[-i] = []

            for i in used:
                literal_watchers[i] = []
        else:
            print("""If you meant to insert a 9x9 or 16x16 sudoku, please use 729 or 4096 variables.
                    If not, your SAT problem will be solved shortly""")
            for i in range (-self.variables,self.variables+1):
                literal_watch[i] = []

        # Pick two unique literals from every clause that are not assigned yet, starting from the left side
        # Append them to the literal watchers map

        for i in range(0, len(clauses)):
            new_clause = []
            first = 0
            for j in range(0, len(clauses[i])):
                if clauses[i][j] not in assignments and first == 0:
                    X = clauses[i][j]
                    first = 1
                    continue
                if clauses[i][j] not in assignments and first == 1:
                    Y = clauses[i][j]
                    break
            new_clause.append(X)
            new_clause.append(Y)
            clauses_watched_by_literals.append(new_clause)
            literal_watchers[X].append(i)
            literal_watchers[Y].append(i)

        return literal_watchers, clauses_watched_by_literals

    # The more efficient of unit propagation enabled by watch literals

    def watch_propagation(self, clauses, literal_watchers, clauses_watched_by_literals, assignments, variable):
        decision_list = [variable]
        while len(decision_list) != 0:
            variable = decision_list.pop()

            # Check which clause the negation of our assigned variable is watching
            # and update if necessary

            for implicated_clause_id in reversed(literal_watchers[-variable]):
                implicated_clause = clauses[implicated_clause_id][:]
                X = clauses_watched_by_literals[implicated_clause_id][0]
                Y = clauses_watched_by_literals[implicated_clause_id][1]
                X_prev = X
                Y_prev = Y
                state, assignments, X, Y, unit = self.current_state(implicated_clause, assignments, X, Y)

                # If the assignment causes a unit clause, keep propagating
                if state == "UNIT":
                    self.units += 1
                    decision_list.append(unit)
                    assignments.append(unit)
                
                # If the assignment causes unsatisfiability, return conflicting clause
                elif state == "UNSAT":
                    return implicated_clause, literal_watchers

                literal_watchers [X_prev].remove(implicated_clause_id)
                literal_watchers [Y_prev].remove(implicated_clause_id)
                clauses_watched_by_literals[implicated_clause_id][0] = X
                clauses_watched_by_literals[implicated_clause_id][1] = Y
                literal_watchers[X].append(implicated_clause_id)
                literal_watchers[Y].append(implicated_clause_id)

        return -1, literal_watchers

    # Helper function for figuring out if action is needed in watch_propagation

    def current_state(self, clause,assignments,X,Y):
        unit = 0

        # Check if one of the literals is watching the implemented clause

        if X in assignments or Y in assignments:                   
            return "SAT",assignments,X,Y,unit
        symbols=[]                                  
        for literal in clause:                  
            if -literal not in assignments:
                symbols.append(literal)
            if literal in assignments :
                if -X not in assignments :
                    return "SAT",assignments,X,literal,unit
                return "SAT",assignments,literal,Y,unit

        # If we have 1 literal remaining, we have a unit clause

        if len(symbols) == 1:                              
            return "UNIT",assignments,X,Y,symbols[0]
        
        # If none remain, that means the current assignments are unsatisfiable

        if len(symbols) == 0:                              
            return "UNSAT",assignments,X,Y,unit

        # If we have found 2 new literals, return and continue the solving process

        else :
            return "NEW",assignments,symbols[0],symbols[1],unit   

    # Helper function to add learned clause to the clause watched by literals set

    def learn_clause(self, clauses,literal_watchers,clauses_watched_by_literals,learned_clause,assignments):
        if len(learned_clause) == 0:
            return -1
        if len(learned_clause) == 1:              
            assignments.append(learned_clause[0])
            return 1,learned_clause[0]
        clauses.append(learned_clause)           
        X = learned_clause[0]
        Y = learned_clause[1]
        i = len(clauses)-1
        new_clause = []
        new_clause.append(X)
        new_clause.append(Y)
        clauses_watched_by_literals.append(new_clause)
        literal_watchers[X].append(i)
        literal_watchers[Y].append(i)
        return 0

    # Helper function to find a UIP

    def analyze_conflict(self, assignments, conflict,decision_level): 
        learn = []
        for level in decision_level:
            learn.append(-assignments[level])
        return learn

    # Initialize VSIDS score count

    def VSIDS_heuristic(self, clauses):
        count = {}
        if self.variables == 729:
            for i in range(999,110, -1):
                if '0' in str(i):
                    continue
                count[-i] = 0

            for i in range(111,1000):
                if '0' in str(i):
                    continue
                count[i] = 0

        elif self.variables == 4096:
            for i in reversed(used):
                count[-i] = 0

            for i in used:
                count[i] = 0
        else:
            for i in range (-self.variables,self.variables+1):
                count[i] = 0
        for clause in clauses:
            for literal in clause:
                count[literal] +=1

        return count

    # Update score count for literals

    def conflict_counter(self, count, clause):
        for literal in clause:
            count[literal] += 1
        return count

    # Reduce scores after every conflict

    def decay_scores(self, count):
        if self.variables == 729:
            for i in range(999,110, -1):
                if '0' in str(i):
                    continue
                count[-i] = count[-i]*90/100

            for i in range(111,1000):
                if '0' in str(i):
                    continue
                count[i] = count[i]*90/100

        elif self.variables == 4096:
            for i in reversed(used):
                count[-i] = count[-i]*90/100

            for i in used:
                count[i] = count[i]*90/100
        else:
            for i in range (-self.variables,self.variables+1):
                count[i] = count[i]*90/100

        return count

    # Choose the literal with the highest score

    def VSIDC_split(self, count, assignments):
        max = 0
        variable = 0
        if self.variables == 729:
            for i in range(999,110, -1):
                if '0' in str(i):
                    continue
                if count[-i] >= max and -i not in assignments:
                    max = count[i]
                    variable = i

            for i in range(111,1000):
                if '0' in str(i):
                    continue
                if count[i] >= max and i not in assignments:
                    max = count[i]
                    variable = i


        elif self.variables == 4096:
            for i in reversed(used):
                if count[-i] >= max and -i not in assignments:
                    max = count[i]
                    variable = -i

            for i in used:
                if count[i] >= max and i not in assignments:
                    max = count[i]
                    variable = i
        else:
            for i in range (-self.variables,self.variables+1):
                if counter[i]>=max and i not in assignments and -i not in assignments:
                    max=counter[i]
                    var=i
        return variable

    # Delete the assignments made after the decision level we backtrack to
        
    def backtrack(self, assignments, level, decision_level):
        self.backtracks += 1
        self.implications = self.implications + len(assignments) - len(decision_level)
        if not decision_level:
            return -1,-1,self.implications
        level = decision_level.pop()
        literal = assignments[level]
        del assignments[level:]
        return 0,-literal,self.implications

    # Helper variable for output

    def output_results(self, vars=None):

        Path(f"{os.getcwd()}/solutions").mkdir(parents=True, exist_ok=True)

        vars = sorted(vars, key = abs)

        input_file_name = self.file.split('/')
        input_file_name = input_file_name[-1]
        output_file = input_file_name[:-4] + '.out'
        if vars is None:
            with open(f"solutions/{output_file}", 'w') as output:
                output.write('')
        else:
            assignments = []
            for v in vars:
                assignments.append(str(v) + ' 0\n')
            with open(f"solutions/{output_file}", 'w') as output:
                output.write('p cnf {} {}\n'.format(len(vars), len(vars)))
                output.writelines(assignments)

    def get_measures(self):
        return self.backtracks, self.units



