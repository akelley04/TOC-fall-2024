#!/usr/bin/env python3

import csv

def read_csv(csvfile):
    file_name = csvfile
    clauses = []
    count = 0
    sat = 0
    unsat = 0
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            #grab problem number by taking from first row
            if lines[0] == 'c':
                problem_number = int(lines[1])
            #grab variable number and clause number by taking from second row
            elif lines[0] == 'p':
                num_vars = int(lines[2])
                num_clauses = int(lines[3])
                print(f'Problem #{problem_number} has {num_vars} variables and {num_clauses} clauses')
            #grab all lines of literals
            else:
                clause = [int(i) for i in lines[:-1] if i != '0']
                clauses.append(clause)
                count += 1
                #collected all the clauses
                if count == num_clauses:
                    values = [None] * num_vars
                    done = DPLL(clauses, values)
                    if done:
                        print("Satisfiable")
                        sat += 1
                    else:
                        print("Unsatisfiable")
                        unsat += 1
                    count = 0
                    clauses = []
    print(f'SATISFIED: {sat}')
    print(f'UNSATISFIED: {unsat}')


def unit_prop(clauses, values):
    #remember any clauses with a single literal
    singles = []

    #loop through each clause of all clauses
    for clause in clauses:
        #if a clause has a single append it to remember
        if len(clause) == 1:
            singles.append(clause[0])
    #loop through the list of single literals 
    if singles:
        for single in singles:
            #assign the value in the values list
            if single < 0:
                values[abs(single) - 1] = False
            elif single > 0:
                values[single - 1] = True
            # remove clause from clauses if literal appears in it
            clauses[:] = [clause for clause in clauses if single not in clause]
            # remove negation of literal from each clause of clauses
            for i, clause in enumerate(clauses):
                clauses[i] = [lit for lit in clause if lit != -(single)]

def pure_elim(clauses, values):
    #dictionary to hold literals that only appears as a positive OR negative literal in all clauses 
    purevars = {}
    #collect all numbers into the dictionary
    for clause in clauses:
        for num in clause:
            purevars[num] = purevars.get(num, 0) + 1
    #sort through any variable that has both positive and negtive literals
    purevars = {key: value for key, value in purevars.items() if -(key) not in purevars}
    #assign the truth value in the values list
    for pure in purevars.keys():
        if pure < 0:
            values[abs(pure) - 1] = False
        else:
            values[abs(pure) - 1] = True
        # where any appearance of a pure literal exists, remove clause from clauses
        clauses[:] = [clause for clause in clauses if pure not in clause]

def DPLL(clauses, values):
    # unit propagation
    while any(len(clause) == 1 for clause in clauses):
        unit_prop(clauses, values)
        
    #pure literal elimination
    pure_elim(clauses, values)

    #stopping conditions 1) satisfiable when clauses are empty 2) unsatisfiable when a clause is empty
    if not clauses:
        return True
    if any(len(clause) == 0 for clause in clauses):
        return False
    
    #DPLL procedure
    #select literal by choosing the first literal of the first clause of clauses
    l = clauses[0][0]
    #recursion
    return DPLL(clauses + [[l]], values) or DPLL(clauses + [[-l]], values)

def main():
    read_csv("2SAT_test4.csv")

if __name__ == "__main__":
    main()