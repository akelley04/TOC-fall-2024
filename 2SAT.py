#!/usr/bin/env python3

import csv

def read_csv(csvfile):
    file_name = csvfile
    row_counter = 0
    clauses = []
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            print(lines)
            row_counter += 1
            #grab problem number by taking from first row
            if row_counter == 1:
                problem_number = int(lines[1])
            #grab variable number and clause number by taking from second row
            elif row_counter == 2:
                num_vars = int(lines[2])
                num_clauses = int(lines[3])
            else:
                clause = [int(i) for i in lines[:-1] if i != '0']
                clauses.append(clause)
    return clauses, problem_number, num_clauses, num_vars

def unit_prop(clauses, values):
    #remember any clauses with a single literal
    singles = []
    #loop through each clause of all clauses
    for clause in clauses:
        print(clause)
        #if a clause has a single append it to remember
        if len(clause) == 1:
            singles.append(clause[0])
    print(f'singles: {singles}')
    #loop through the list of single literals 
    for single in singles:
        #assign the value in the values list
        if single < 0:
            values[abs(single) - 1] = False
        elif single > 0:
            values[single - 1] = True
        # using list comprehension if that variable appears in other clauses then also remove that literal
        for i, clause in enumerate(clauses):
            clauses[i] = [var for var in clause if abs(var) != abs(single)]
    #remove any empty lists, must modify in place
    clauses[:] = [clause for clause in clauses if len(clause) != 0] 
    print(f'IN UNIT 1: {clauses}')
    return 

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
    for key in purevars.keys():
        if key < 0:
            values[abs(key) - 1] = False
        else:
            values[abs(key) - 1] = True
    print(purevars)
    print(values)
def DPLL(clauses, values):
    # unit propagation
    while any(len(clause) == 1 for clause in clauses):
        unit_prop(clauses, values)
        print(f'IN DPLL 1: {clauses}')

    # pure literal elimination:
    # while there is a literal l that occurs pure in clauses do
    #     clauses ← pure-literal-assign(l, clauses);
    # # stopping conditions:
    # if clauses is empty then
    #     return true;
    # if clauses contains an empty clause then
    #     return false;
    # # DPLL procedure:
    # l ← choose-literal(clauses);
    # return DPLL(clauses ∧ {l}) or DPLL(clauses ∧ {¬l});


def main():
    clauses, problem_number, num_clauses, num_vars = read_csv("2SAT_test2.csv")
    values = [None] * num_vars
    print(f'values: {values}')
    print(f'problem number: {problem_number}')
    print(f'# of clauses: {num_clauses}')
    print(f'# of variables: {num_vars}')
    print(clauses)
    # print("\n")
    # DPLL(clauses, values)
    # print(f'MAIN 2: {clauses}')
    # print(values)

    #pure elim
    pure_elim(clauses, values)
    # if clauses:
    #     print("unsatisfiable")
    # else:
    #     print("satisfiable")

if __name__ == "__main__":
    main()