#!/usr/bin/python3

# Imports and global variables
from copy import deepcopy
import random
import argparse
import time
import json
import string
import os

GLOBAL_OVERVIEW = {
    "heuristic" : None,
    "input_file" : None,
    "start_time" : None,
    "puzzle_clauses": None,
    "unit_literals" : 0,
    "branching_count" : 0,     
    "initial_state" : None,
    "final_state" : None,
}

###############################################################################
############### Utils #########################################################
def is_literal_negated(literal):
    return literal[0] == "-"

def get_negated_literal(literal):
    return literal[1:] if is_literal_negated(literal) else "-" + literal

###############################################################################
############### Empty clause ##################################################
def contains_empty_clause(set_of_clauses):
    for clause in set_of_clauses:
        if len(clause) == 0:
            return True
    return False

###############################################################################
############### Tautologies ###################################################
def filter_out_tautologies(set_of_clauses):
    filtered_set_of_clauses = []
    for clause in set_of_clauses:
        tautology = False
        for literal in clause:
            negated_literal = get_negated_literal(literal)
            
            if negated_literal in clause:
                tautology = True
                break
        
        if not tautology:
            filtered_set_of_clauses.append(clause)

    return filtered_set_of_clauses

###############################################################################
############### Branching and state update ####################################
def set_variable_value(state, variable, value):
    if variable is None:
        return state

    mapping = {
        variable: value,
        get_negated_literal(variable): True if value is False else False
    }

    new_set_of_clauses = []
    for clause in state["set_of_clauses"]:
        for literal_index in range(len(clause)):
            literal = clause[literal_index]
            if literal in mapping:
                clause[literal_index] = mapping[literal]

        # Remove conjuction
        if True in clause:
            continue
        
        # Remove disjunction
        while False in clause:
            clause.remove(False)

        new_set_of_clauses.append(clause)
    
    if is_literal_negated(variable):
        variable = get_negated_literal(variable)

    # variables keys always in positive form    
    state["variables"][variable] = mapping[variable]
    state["set_of_clauses"] = new_set_of_clauses
    return state

###############################################################################
############### Unit clauses and pure literals ################################
def find_literals_in_unit_clauses(set_of_clauses):
    literals_in_unit_clauses = []
    for clause in set_of_clauses:
        if len(clause) == 1:
            literals_in_unit_clauses.append(clause[0])
    return literals_in_unit_clauses

def find_pure_literals(set_of_clauses):
    literals_occurrences = dict()
    for clause in set_of_clauses:
        for literal in clause:
            if literal in literals_occurrences:
                literals_occurrences[literal] += 1
            else:
                literals_occurrences[literal] = 1
    
    pure_literals = []
    for literal in literals_occurrences:
        negated_literal = get_negated_literal(literal)
        if negated_literal not in literals_occurrences:
            pure_literals.append(literal)

    return pure_literals

 
def find_max_occurance_variable(set_of_clauses):
    literals_occurrences = dict()
    literals_weights = dict()
 
    for clause in set_of_clauses:
        for literal in clause:
 
            if literal in literals_occurrences:
                literals_occurrences[literal] += 1
            else:
                literals_occurrences[literal] = 1
 
         #   if literal in clause:
        #        literals_weights[literal] += 2^(-len(clause))
           
    weights=[] #The two-sided Jeroslow-Wang (JW-TS) heuristic identifies the variable x with the largest sum J(x) + J(¬x)
    for literal in literals_occurrences.keys:
       
#list(positive variables get_negated_literal(pos))
 
sums=[]
for pos_literal in positive_variables:
    sums.append(literals_weights[pos_literal] + literals_weights[get_negated_literal(pos_literal)])
    max_index(sums)
   
 
 
    most_occured_variable = max(literals_occurrences, key=literals_occurrences.get)
    #most_occured_variable_neg = get_negated_literal(most_occured_variable)
 
 
 
    return max(literals_occurrences, key=literals_occurrences.get)
 
 



###############################################################################
############### Branching #####################################################
def choose_variable_and_order_of_branching(state, heuristic):
    variable = None
    order_of_branching = (True, False)
    
    if heuristic == 1:
        not_assigned_variables = {k: v for k, v in state["variables"].items() if v is None}
        not_assigned_variables = list(not_assigned_variables.keys())
        variable = random.choice(not_assigned_variables) if len(not_assigned_variables) > 0 else None 

    elif heuristic == 2:
        # Tautologies check
        set_of_clauses_without_tautologies = filter_out_tautologies(state["set_of_clauses"])
        if set_of_clauses_without_tautologies != state["set_of_clauses"]:
            state["set_of_clauses"] = set_of_clauses_without_tautologies

        # Unit clauses check
        literals_in_unit_clauses = find_literals_in_unit_clauses(state["set_of_clauses"])
        if (len(literals_in_unit_clauses) != 0):
            GLOBAL_OVERVIEW["unit_literals"] += len(literals_in_unit_clauses)
            for literal_in_unit_clause in literals_in_unit_clauses:
                set_variable_value(state, literal_in_unit_clause, True)
        
        # Pure literal check
        pure_literals = find_pure_literals(state["set_of_clauses"])
        if (len(pure_literals) != 0):
            for pure_literal in pure_literals:
                set_variable_value(state, pure_literal, True)
        
        not_assigned_variables = {k: v for k, v in state["variables"].items() if v is None}
        not_assigned_variables = list(not_assigned_variables.keys())
        variable = random.choice(not_assigned_variables) if len(not_assigned_variables) > 0 else None 
    elif heuristic == 3:
        """
            TODO 
            set `variable` and `order_of_branching` based on:
                - `state`
                - `heuristic`
                - `GLOBAL_OVERVIEW`
        """
        raise Exception("Not implemented yet!")
    else:
        raise Exception("Invalid usage!")

    return variable, order_of_branching

def davis_putnam(state, heuristic = None, depth = 0):
    GLOBAL_OVERVIEW["branching_count"] += 1
    print("davis_putnam> depth={}, clauses={}".format(depth, len(state["set_of_clauses"])))
    state = deepcopy(state)

    # Satisfiability check
    if len(state["set_of_clauses"]) == 0:
        GLOBAL_OVERVIEW["final_state"] = state
        return True
    
    # Empty clause check
    if contains_empty_clause(state["set_of_clauses"]):
        return False

    # Split
    variable, order_of_branching = choose_variable_and_order_of_branching(state, heuristic)

    cloned_state = deepcopy(state)
    if davis_putnam(set_variable_value(cloned_state, variable, order_of_branching[0]), heuristic, depth + 1):
        return True
    else:
        return davis_putnam(set_variable_value(state, variable, order_of_branching[1]), heuristic, depth + 1)

def get_variables_dictionary_from_clauses(clauses):
    result = dict()
    for clause in clauses:
        for literal in clause:
            if is_literal_negated(literal):
                literal = get_negated_literal(literal)
            
            if literal not in result:
                result[literal] = None
    return result

def get_initial_state(input_file):
    if input_file is None:
        return get_default_initial_state()
    
    with open(input_file) as f:
        lines = f.readlines()
        
        clauses = []
        for line in lines[1:]:
            tokens = line.split(" ")
            stripped_tokens = list(map(lambda x: x.strip(), tokens[:-1])) 
            filtered_tokens = list(filter(lambda x: x != "", stripped_tokens)) 
            filtered_tokens = list(map(lambda x: str(int(x)), filtered_tokens)) 

            if len(filtered_tokens) > 0:
                clauses.append(filtered_tokens)
        
        # saving sudoku puzzle initial assumptions
        GLOBAL_OVERVIEW["puzzle_clauses"] = find_literals_in_unit_clauses(clauses)
        try:
            print_sudoku(GLOBAL_OVERVIEW["puzzle_clauses"], "initial_sudoku")
        except Exception:
            pass
        return {
            "variables" : get_variables_dictionary_from_clauses(clauses),
            "set_of_clauses" : clauses
        }

def get_default_initial_state():
    return {
        "variables": {
            "a" : None,
            "b" : None,
            "c" : None,
        },
        "set_of_clauses": [
            ["a", "b", "c"],
            ["a", "-b"],
            ["a", "-c"],
            ["-a", "c"],
        ],
    }



"""
    Can take any sudoku's from 2x2 to 9x9
    e.g. 
        variables = ['143', '234', '241', '311', '324', '413']
        
        print>
            ? ? ? 3
            ? ? 4 1
            1 4 ? ?
            3 ? ? ?
"""
def print_sudoku(variables, title):
    max_from_variable = lambda variable: max([int(variable[0]), int(variable[1]), int(variable[2])])
    sudoku_size = max(list(map(lambda variable : max_from_variable(variable), variables)))
    
    sudoku_matrix = [["?" for _ in range(sudoku_size)] for _ in range(sudoku_size)]
    for variable in variables:
        row_index = int(variable[0])
        column_index = int(variable[1])
        sudoku_value = variable[2]
        sudoku_matrix[row_index - 1][column_index - 1] = sudoku_value

    GLOBAL_OVERVIEW[title] = sudoku_matrix

    sudoku_matrix_string = ""
    for row in sudoku_matrix:
        sudoku_matrix_string += (" ".join(row) + "\n")
    print("{}:\n{}\n".format(title, sudoku_matrix_string))

def save_to_file(logs_directory = "logs"):
    with open("{}.out".format(GLOBAL_OVERVIEW["input_file"]), "w") as f:
        final_state_variables = GLOBAL_OVERVIEW["final_state"]["variables"]
        number_of_variables = len(final_state_variables.keys())
        number_of_clauses = number_of_variables
        f.write("p cnf {} {}\n".format(number_of_variables, number_of_clauses))
        for variable in final_state_variables:
            variable_value = final_state_variables[variable]
            
            if variable_value == True:
                f.write("{} 0\n".format(variable))
            else:
                f.write("-{} 0\n".format(variable))

    with open("{}.out.log".format(GLOBAL_OVERVIEW["input_file"]), "w") as f:
        f.write(json.dumps(GLOBAL_OVERVIEW))

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
    random_log_file_name = "".join(random.choice(string.ascii_letters) for _ in range(10))
    with open("{}/{}.log".format(logs_directory, random_log_file_name), "w") as f:
        f.write(json.dumps(GLOBAL_OVERVIEW))

def log():
    GLOBAL_OVERVIEW["time_lapsed"] = time.time() - GLOBAL_OVERVIEW["start_time"]
    
    result = "final_state" in GLOBAL_OVERVIEW and GLOBAL_OVERVIEW["final_state"] is not None
    print("\nResult: " + "[Satisfiable]\n" if result == True else "[Unsatisfiable]\n")

    if result:
        try:
            variables_dictionary = GLOBAL_OVERVIEW["final_state"]["variables"]
            variables_key_list = variables_dictionary.keys()
            positive_variable = list(filter(lambda variable: variables_dictionary[variable], variables_key_list))
            print_sudoku(positive_variable, "final_sudoku")
        except Exception:
            pass

    save_to_file()

def parse_arguments():
    parser = argparse.ArgumentParser(prog='SAT', description="General purpose SAT solver")
    parser.add_argument("-S", dest = "heuristic", type=int, help="1, 2 or 3. Defaults to 1")
    parser.add_argument("input_file", nargs="?")
    arguments = parser.parse_args()
    
    if arguments.heuristic not in [1, 2, 3]:
        raise Exception("HEURISTIC should be 1, 2 or 3")
    return arguments.heuristic, arguments.input_file

def init():
    heuristic, input_file = parse_arguments()

    state = get_initial_state(input_file) 
    GLOBAL_OVERVIEW["initial_state"] = deepcopy(state)
    GLOBAL_OVERVIEW["input_file"] = input_file
    GLOBAL_OVERVIEW["heuristic"] = heuristic
    GLOBAL_OVERVIEW["start_time"] = time.time()
    
    return state, heuristic

def main():
    state, heuristic = init()
    davis_putnam(state, heuristic)
    log()

############### Test ##########################################################
def test_implementation():
    # Test `is_literal_negated` ###############################################
    assert is_literal_negated("-X") == True, "Error!"
    assert is_literal_negated("X") == False, "Error!"

    # Test `get_negated_literal` ##############################################
    assert get_negated_literal("X") == "-X", "Error!"
    assert get_negated_literal("-X") == "X", "Error!"

    # Test `filter_out_tautologies` ###########################################
    expected = [
        ["a", "d"],
    ]
    actual = filter_out_tautologies([
        ["a", "-a", "a", "b", "-d"],
        ["-a", "b", "-b", "c"],
        ["a", "d"],
    ])
    
    assert actual == expected, "Error!"

    # Test `find_pure_literals` ###############################################
    expected = ["-d", "c"]
    actual = find_pure_literals([
        ["a", "-a", "b", "-d"],
        ["-a", "b", "-b", "c"],
        [],
    ])
    assert actual == expected, "Error!"

    # Test `find_literals_in_unit_clauses` ####################################
    expected = ["d"]
    actual = find_literals_in_unit_clauses([
        ["a", "-a", "b", "-d"],
        ["-a", "b", "-b", "c"],
        ["d"],
    ])
    assert actual == expected, "Error!"

    # Test `set_variable_value` ###############################################
    #### Test 1 ---------------------------------------------------------------
    initial_state = {
        "variables": {
            "a" : None,
            "b" : None,
            "c" : None,
        },
        "set_of_clauses": [
            ["a", "b", "c"],
            ["a", "-b"],
            ["a", "-c"],
            ["-a", "c"],
        ],
    }
    
    expected_state = {
        "variables": {
            "a" : True,
            "b" : None,
            "c" : None,
        },
        "set_of_clauses": [
            ["c"],
        ],
    }

    actual_state = set_variable_value(initial_state, "a", True)
    assert actual_state == expected_state, "Error!"

    #### Test 2 ---------------------------------------------------------------
    initial_state = {
        "variables": {
            "a" : None,
            "b" : None,
            "c" : None,
        },
        "set_of_clauses": [
            ["-a", "-b", "-c"],
            ["a", "-b"],
            ["a", "-c"],
            ["-a", "c"],
            ["a"],
            ["b"],
            ["c"],
        ],
    }
    
    expected_state = {
        "variables": {
            "a" : True,
            "b" : None,
            "c" : None,
        },
        "set_of_clauses": [
            ["-b", "-c"],
            ["c"],
            ["b"],
            ["c"],
        ],
    }

    actual_state = set_variable_value(initial_state, "a", True)
    assert actual_state == expected_state, "Error!"

    #### Test 3 ---------------------------------------------------------------
    expected_state = {
        "variables": {
            "16" : False,
        },
        "set_of_clauses": [],
    }
    
    initial_state = {
        "variables": {
            "16" : None,
        },
        "set_of_clauses": [['-16']],
    }
    

    actual_state = set_variable_value(initial_state, "16", False)
    assert actual_state == expected_state, "Error!"

    # Test `get_variables_dictionary_from_clauses` ###############################################
    expected = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "123": None,
        "456": None,
        "666": None,
    }
    actual = get_variables_dictionary_from_clauses([
        ["a", "-a", "b"],
        ["-a", "b", "-b", "c"],
        ["d"],
        ["123", "456", "-123"],
        ["-666"],
    ])
    assert actual == expected, "Error!"

###############################################################################

if __name__ == "__main__":
    test_implementation()
    main()
