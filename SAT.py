#!/usr/bin/python3

############### 2. ############################################################
def contains_empty_clause(set_of_clauses):
    # TODO
    return True

###############################################################################
############### 3. ############################################################
def filter_out_tautologies(set_of_clauses):
    # TODO
    filtered_set_of_clauses = set_of_clauses
    return set_of_clauses

###############################################################################
############### 4. ############################################################
def find_unit_clauses(set_of_clauses):
    # TODO
    return []

def apply_unit_clauses(set_of_clauses, unit_clauses):
    # TODO
    return set_of_clauses

###############################################################################
############### 5. ############################################################
def find_pure_literals(set_of_clauses):
    # TODO
    return []

def apply_pure_literals(set_of_clauses, pure_literals):
    # TODO
    return set_of_clauses

###############################################################################
############### 6. ############################################################
def choose_variable(set_of_clauses, heuristic):

    # TODO
    if heuristic is None:
        # default
    else:
        # other   
    return None

def set_variable_value(set_of_clauses, variable, value):
    # TODO
    return set_of_clauses

def davis_putnam(set_of_clauses, heuristic = None):
    # 0. TODO
    # Simplification after True & False branching


    # 1. Satisfiability check
    if len(set_of_clauses) == 0:
        return True
    
    # 2. Empty clause check
    if contains_empty_clause(set_of_clauses):
        return False
    
    # 3. Tautologies check
    set_of_clauses_without_tautologies = filter_out_tautologies(set_of_clauses)
    if len(set_of_clauses_without_tautologies) != len(set_of_clauses):
        return davis_putnam(set_of_clauses_without_tautologies)

    # 4. Unit clauses check
    unit_clauses = find_unit_clauses(set_of_clauses)
    if (len(unit_clauses) != 0):
        new_set_of_clauses = apply_unit_clauses(set_of_clauses, unit_clauses)
        return davis_putnam(new_set_of_clauses)
    
    # 5. Pure literal check
    pure_literals = find_pure_literals(set_of_clauses)
    if (len(pure_literals) != 0):
        new_set_of_clauses = apply_pure_literals(set_of_clauses, pure_literals)
        return davis_putnam(new_set_of_clauses)
    
    # 6. Split
    variable = choose_variable(set_of_clauses, heuristic)
    order_of_truth_assignment = chose_order_of_truth_assignment(heuristic)

    # TODO with respect to `order_of_truth_assignment`
    if davis_putnam(set_variable_value(set_of_clauses, variable, True)):
        return True
    else:
       return davis_putnam(set_variable_value(set_of_clauses, variable, False))

def main():
    # parser
    # TODO Implement parser
    input_file = None

    # TODO get rules from input_file
    set_of_clauses = None 

    # TODO  get heuristic from input_file
    heuristic = None 

    # TODO get puzzle
    puzzle = None 

    # TODO write result to file
    result = davis_putnam(set_of_clauses, heuristic)
    
if __name__ == "__main__":
    main()