# Sat Solver

## Input file
DIMACS CNF format

This format is widely accepted as the standard format for boolean formulas in CNF. Benchmarks listed on satlib.org, for instance, are in the DIMACS CNF format.

An input file starts with comments (each line starts with c). The number of variables and the number of clauses is defined by the line p cnf variables clauses

Each of the next lines specifies a clause: a positive literal is denoted by the corresponding number, and a negative literal is denoted by the corresponding negative number. The last number in a line should be zero. For example,

```
c A sample .cnf file.
p cnf 3 2
1 -3 0
2 3 -1 0 
```
## Run
You are free to choose any programming language you fancy, but we must be able to run your SAT solver with the command SAT -Sn inputfile , for example: SAT -S2 sudoku_nr_10 , where SAT is the (compulsory) name of your program, n=1 for the basic DP and n=2 or 3 for your two other strategies, and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle). 

```
SAT -S2 sudoku_nr_10
```

## Work

### DPLL algorithm

#### Default

#### Heuristic One

#### Heuristic Two