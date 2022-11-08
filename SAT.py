#!/usr/bin/python3

# Imports and global variables
from copy import deepcopy
import random
import argparse

GLOBAL_OVERVIEW = {
    "solution" : None,
    "initial_state" : None,
}

###############################################################################
############### Utils #########################################################
def is_literal_negated(literal):
    return literal[0] == "~"

def get_negated_literal(literal):
    return literal[1:] if is_literal_negated(literal) else "~" + literal

###############################################################################
############### 2. ############################################################
def contains_empty_clause(set_of_clauses):
    for clause in set_of_clauses:
        if len(clause) == 0:
            return True
    return False

###############################################################################
############### 3. ############################################################
def filter_out_tautologies(set_of_clauses):
    filtered_set_of_clauses = []
    for clause in set_of_clauses:
        clause_cloned = deepcopy(clause)
        for literal in clause_cloned:
            negated_literal = get_negated_literal(literal)
            
            if negated_literal in clause_cloned:
                while negated_literal in clause_cloned:
                    clause_cloned.remove(negated_literal)
                while literal in clause_cloned:
                    clause_cloned.remove(literal)

        filtered_set_of_clauses.append(clause_cloned)
    return filtered_set_of_clauses

###############################################################################
############### 4. ############################################################
def set_variable_value(state, variable, value):
    if is_literal_negated(variable):
        variable = get_negated_literal(variable)
        value = True if value is False else True

    new_set_of_clauses = []
    for clause in state["set_of_clauses"]:
        negated_variable = get_negated_literal(variable)
        if variable in clause:
            continue
        
        if negated_variable in clause:
            clause.remove(negated_variable)

            if len(clause) != 0:
                new_set_of_clauses.append(clause)

    state["variables"][variable] = value
    state["set_of_clauses"] = new_set_of_clauses
    return state

def find_literals_in_unit_clauses(set_of_clauses):
    literals_in_unit_clauses = []
    for clause in set_of_clauses:
        if len(clause) == 1:
            literals_in_unit_clauses.append(clause[0])
    return literals_in_unit_clauses

def handle_unit_clauses(state, literals_in_unit_clauses):    
    for literal in literals_in_unit_clauses:
        state = set_variable_value(state, literal, True)

    return state

###############################################################################
############### 5. ############################################################
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

def handle_pure_literals(state, pure_literals):
    for literal in pure_literals:
        if is_literal_negated(literal):
            state = set_variable_value(state, literal, False)
        else:
            state = set_variable_value(state, literal, True)
    
    return state

###############################################################################
############### 6. ############################################################
def choose_variable_and_order_of_branching(state, heuristic):
    variable = None
    order_of_branching = (True, False)
    
    if heuristic == 1:
        not_assigned_variables = {k: v for k, v in state["variables"].items() if v is None}
        variable =  random.choice(list(not_assigned_variables.keys()))
    elif heuristic == 2:
        """
            TODO
            set `variable` and `order_of_branching` based on:
                - `state`
                - `heuristic`
                - `GLOBAL_OVERVIEW`
        """
        raise Exception("Not implemented yet!")
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

def davis_putnam(state, heuristic = None):
    # 1. Satisfiability check
    if len(state["set_of_clauses"]) == 0:
        GLOBAL_OVERVIEW["solution"] = state["variables"]
        return True
    
    # 2. Empty clause check
    if contains_empty_clause(state["set_of_clauses"]):
        return False
    
    # 3. Tautologies check
    set_of_clauses_without_tautologies = filter_out_tautologies(state["set_of_clauses"])
    if set_of_clauses_without_tautologies != state["set_of_clauses"]:
        state["set_of_clauses"] = set_of_clauses_without_tautologies
        return davis_putnam(state, heuristic)

    # 4. Unit clauses check
    literals_in_unit_clauses = find_literals_in_unit_clauses(state["set_of_clauses"])
    if (len(literals_in_unit_clauses) != 0):
        state = handle_unit_clauses(state, literals_in_unit_clauses)
        return davis_putnam(state, heuristic)
    
    # 5. Pure literal check
    pure_literals = find_pure_literals(state["set_of_clauses"])
    if (len(pure_literals) != 0):
        state = handle_pure_literals(state, pure_literals)
        return davis_putnam(state, heuristic)
    
    # 6. Split
    variable, order_of_branching = choose_variable_and_order_of_branching(state, heuristic)

    cloned_state = deepcopy(state)
    cloned_state = set_variable_value(cloned_state, variable, True)
    if davis_putnam(cloned_state, heuristic):
        return True
    else:
        set_variable_value(state, variable, False)
        return davis_putnam(state, heuristic)

def get_initial_state(input_file):
    if input_file is None:
        return get_default_initial_state()
    
    # TODO build state from input file
    with open(input_file) as f:
        lines = f.readlines()
        first_line = lines[0]
        splitted_header = first_line.split(" ")
        number_of_variables = int(splitted_header[2])
        number_of_clauses = int(splitted_header[3])

        clauses = []
        for clause_index in range(1, number_of_clauses):
            clauses.append(lines[clause_index])
        
        print("lines[clause_index + 2]", lines[clause_index + 2])
    return get_default_initial_state()

def get_default_initial_state():
    return {
        "variables": {
            "a" : None,
            "b" : None,
            "c" : None,
            "d" : None,
        },
        "set_of_clauses": [
            ["a", "b", "c"],
            ["a", "~b"],
            ["a", "~c"],
            ["~a", "c"],
        ],
    }

def log():
    result = GLOBAL_OVERVIEW["solution"] is not None
    print("Result: " + "[Satisfiable]" if result == True else "[Unsatisfiable]")
    print(GLOBAL_OVERVIEW["solution"])

def parse_arguments():
    parser = argparse.ArgumentParser(prog='SAT', description="General purpose SAT solver")
    parser.add_argument("-S", dest = "strategy", type=int, help="1, 2 or 3. Defaults to 1")
    parser.add_argument("input_file")
    arguments = parser.parse_args()
    
    if arguments.strategy not in [1, 2, 3]:
        raise Exception("STRATEGY should be 1, 2 or 3")
    return arguments.strategy, arguments.input_file

def init():
    heuristic, input_file = parse_arguments()

    state = get_initial_state(input_file) 
    
    GLOBAL_OVERVIEW["initial_state"] = state
    GLOBAL_OVERVIEW["input_file"] = input_file
    GLOBAL_OVERVIEW["heuristic"] = heuristic
    
    return state, heuristic

def main():
    state, heuristic = init()
    davis_putnam(state, heuristic)
    log()

############### Test ##########################################################
def test_implementation():
    # Test `is_literal_negated` ###############################################
    assert is_literal_negated("~X") == True, "Error!"
    assert is_literal_negated("X") == False, "Error!"

    # Test `get_negated_literal` ##############################################
    assert get_negated_literal("X") == "~X", "Error!"
    assert get_negated_literal("~X") == "X", "Error!"

    # Test `filter_out_tautologies` ###########################################
    expected = [
        ["b", "~d"],
        ["~a", "c"],
        [],
    ]
    actual = filter_out_tautologies([
        ["a", "~a", "a", "b", "~d"],
        ["~a", "b", "~b", "c"],
        [],
    ])
    
    assert actual == expected, "Error!"

    # Test `find_pure_literals` ###############################################
    expected = ["~d", "c"]
    actual = find_pure_literals([
        ["a", "~a", "b", "~d"],
        ["~a", "b", "~b", "c"],
        [],
    ])
    assert actual == expected, "Error!"

    # Test `find_literals_in_unit_clauses` ####################################
    expected = ["d"]
    actual = find_literals_in_unit_clauses([
        ["a", "~a", "b", "~d"],
        ["~a", "b", "~b", "c"],
        ["d"],
    ])
    assert actual == expected, "Error!"

    # Test `set_variable_value` ###############################################
    initial_state = {
        "variables": {
            "a" : None,
            "b" : None,
            "c" : None,
        },
        "set_of_clauses": [
            ["a", "b", "c"],
            ["a", "~b"],
            ["a", "~c"],
            ["~a", "c"],
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

    set_variable_value(initial_state, "a", True)
    assert initial_state == expected_state, "Error!"

###############################################################################

if __name__ == "__main__":
    test_implementation()
    main()
