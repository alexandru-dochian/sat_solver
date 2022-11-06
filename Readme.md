# Sat Solver

## Overleaf edit link

https://www.overleaf.com/1581887799gtzqjnqscsmf

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