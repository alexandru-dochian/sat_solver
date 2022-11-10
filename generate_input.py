#!/usr/bin/python3

import math
import os

def generate_sudoku_rules():
    
    pass


"""
    e.g. 
        sudoku_inline = "...3..4114..3..."
        result = ['143', '234', '241', '311', '324', '413']
"""
def from_sudoku_inline_to_clauses(sudoku_inline):
    sudoku_size = int(math.sqrt(len(sudoku_inline)))
    
    clauses = []
    for row_index in range(sudoku_size):
        for column_index in range(sudoku_size):
            position_inline = sudoku_size * row_index + column_index
            value_at_position = sudoku_inline[position_inline]
            
            if value_at_position != ".":
                clauses.append("{}{}{}".format(row_index + 1, column_index + 1, value_at_position))
    return clauses

def build_input(rules_dimacs_file, sudoku_puzzles_file, target_folder_path, NUMBER_OF_FILES=10):
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)
    
    final_number_of_variables = None
    final_number_of_clauses = None

    rules = []
    with open(rules_dimacs_file) as f:
        lines = f.readlines()
        first_line = lines[0]
        splitted_header = first_line.split(" ")
        final_number_of_variables = int(splitted_header[2])
        rules = lines[1:]
    
    with open(sudoku_puzzles_file) as f:
        lines = f.readlines()
        for line_index in range(0, len(lines)):
            line = lines[line_index]
            clauses = from_sudoku_inline_to_clauses(line)
            puzzle_rules = list(map(lambda clause: "{} 0\n".format(clause), clauses))
        
            with open("{}/test{}.in".format(target_folder_path, line_index + 1), 'w') as f:
                final_number_of_clauses = len(rules) + len(puzzle_rules)
                f.write("p cnf {} {}\n".format(final_number_of_variables, final_number_of_clauses))
                
                for rule in rules:
                    f.write(rule)

                for puzzle_rule in puzzle_rules:
                    f.write(puzzle_rule)

            if line_index + 1 >= NUMBER_OF_FILES:
                break
            
if __name__ == "__main__":
    build_input(
        rules_dimacs_file = "documentation/sudoku-rules/sudoku-rules-4x4.txt",
        sudoku_puzzles_file = "documentation/testsets/4x4.txt",
        target_folder_path = "input/4x4"
    )
    build_input(
        rules_dimacs_file = "documentation/sudoku-rules/sudoku-rules-9x9.txt",
        sudoku_puzzles_file = "documentation/testsets/damnhard.sdk.txt",
        target_folder_path = "input/9x9"
    )