#!/usr/bin/python3

import random


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
    for clause in set_of_clauses:
        for literal in clause:
            negated_literal = get_negated_literal(literal)
            
            # TODO: Question: Should we remove all occurrences of literal
            # and negated_literal in this situation?)
            if negated_literal in clause:
                clause.remove(negated_literal)
                clause.remove(literal)
    return set_of_clauses

###############################################################################
############### 4. ############################################################
"""
    This method has lateral effect on state variable
"""
def set_variable_value(state, variable, value):
    raise Exception("Not implemented yet!") 

def find_literals_in_unit_clauses(set_of_clauses):
    literals_in_unit_clauses = []
    for clause in set_of_clauses:
        if len(clause) == 1:
            literals_in_unit_clauses.append(clause[0])
    return literals_in_unit_clauses

"""
    This method has lateral effect on state variable
"""
def handle_unit_clauses(state, literals_in_unit_clauses):
    for literal in literals_in_unit_clauses:
        set_variable_value(state, literal, True)

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

"""
    This method has lateral effect on state variable
"""
def handle_pure_literals(state, pure_literals):
    for literal in pure_literals:
        if is_literal_negated(literal):
            set_variable_value(state, literal, False)
        else:
            set_variable_value(state, literal, True)

###############################################################################
############### 6. ############################################################
def choose_variable(state, heuristic):
    if heuristic is None:
        not_assigned_variables = {k: v for k, v in state["variables"].items() if v is None}
        return random.choice(list(not_assigned_variables.keys()))
    else:
        # TODO
        return None

def davis_putnam(state, heuristic = None):
    set_of_clauses = state["set_of_clauses"]
    
    # 1. Satisfiability check
    if len(set_of_clauses) == 0:
        return True
    
    # 2. Empty clause check
    if contains_empty_clause(set_of_clauses):
        return False
    
    # 3. Tautologies check
    set_of_clauses_without_tautologies = filter_out_tautologies(set_of_clauses)
    if set_of_clauses_without_tautologies != set_of_clauses:
        state["set_of_clauses"] = set_of_clauses_without_tautologies
        return davis_putnam(state, heuristic)

    # 4. Unit clauses check
    literals_in_unit_clauses = find_literals_in_unit_clauses(set_of_clauses)
    if (len(literals_in_unit_clauses) != 0):
        handle_unit_clauses(state, literals_in_unit_clauses)
        return davis_putnam(state, heuristic)
    
    # 5. Pure literal check
    pure_literals = find_pure_literals(set_of_clauses)
    if (len(pure_literals) != 0):
        handle_pure_literals(state, pure_literals)
        return davis_putnam(state, heuristic)
    
    # 6. Split
    variable = choose_variable(state, heuristic)

    
    if davis_putnam(set_variable_value(set_of_clauses, variable, True)):
        return True
    else:
       return davis_putnam(set_variable_value(set_of_clauses, variable, False))

def get_initial_state(input_file):
    if input_file is None:
        return get_default_initial_state()
    
    # TODO build state from input file
    return None

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

def main():
    # TODO Implement parser
    input_file = None
    heuristic = None 

    # TODO get state from input_file
    state = get_initial_state(input_file) 

    # TODO write result to file
    result = davis_putnam(state, heuristic)
    

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
        ["a", "~a", "b", "~d"],
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

###############################################################################

if __name__ == "__main__":
    test_implementation()
    main()
