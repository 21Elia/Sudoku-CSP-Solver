# Sudoku CSP Solver

This project implements a solver for Sudoku puzzles using a Constraint Satisfaction Problem (CSP) approach. 
The Backtracking Search algorithm is optimized with the implementation of different heuristics to find the solution efficiently.

## Algorithms
The solution is structured  around the Sudoku class and utilizes a combination of inference and heuristic algorithms to minimize the variable's domain space, meaning reducing search time:
1. **Inference (Constraint Propagation)**
    - **AC-3 (Arc Consistency Algorithm 3)**: Executed once at the beginning in the `solve()` method to pre-process the puzzle. It reduces the initial domain of the cells, resulting in a         significantly slimmer search tree. 
    - **Forward Checking**: Applied after every variable assignment during backtracking. The technique consists of propagating the effects of a choice: once assigned a certain variable, we           want to remove conflicting values from the domains of the adjacent unassigned variables, avoiding conflitcs and reducing search space. 
    
2. **Optimized Search (Backtracking Search)**
The core solver is a Backtracking algorithm enhanced by the following heuristics: 
    - **MRV  (Minimum Remaining Values / Fail-First)**: Selects the unassigned variable with the smallest domain. The idea is to firstly explore small sub-tree, to reduce chances of deep         searches failures in the search tree.
    - **LCV (Least Constraining Value)**: Once the variable is chosen by MRV, the algorithm first selects the domain values that are present in the fewest number of variable in the               constraint graph. 
---
## Project Execution
The project just requires Python 3. No external libraries are necessary.

**File Structure**
```
/Sudoku-CSP-Solver-main/
├── main.py        # Execution and testing logic
├── Sudoku.py      # The main Sudoku class with CSP algorithms
└── .gitignore     # Files to ignore (cache, virtual environments, etc.)
```

**Instructions**

1. Ensure you are in the main project directory (Sudoku-CSP-Solver-main).
2. Run the main file from your  terminal using the following command:
```
python3 main.py
```

The program will output the initial grid and the solved grid (or a message indicating no solution was 
found).
