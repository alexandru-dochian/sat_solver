# Sat Solver


## Data
Inputs are found in `input` folder.

## Run

```
$ ./SAT.py -h

>    usage: SAT [-h] [-S STRATEGY] [input_file]
>
>    General purpose SAT solver
>
>    positional arguments:
>    input_file
>
>    options:
>    -h, --help   show this help message and exit
>    -S STRATEGY  1, 2 or 3. Defaults to 1

```

---
Example:
```
./SAT.py -S1 input/4x4/test0.in
```


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

## Work

 - [x] DP algorithm
 - [ ] Heuristic 1
 - [ ] Heuristic 2