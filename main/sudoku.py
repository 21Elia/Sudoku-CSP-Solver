# i have a set of variables X = {x1, x2, ___, x_n}
# i have a set of domains D = {1, ___, 9}
#
# constraints: all different in 3x3
#              all different in row
#              all different in column



class Sudoku:
    def __init__(self, board: str):
        
        self.board:str = board; #board is a string of 81 values (9x9) where value 0 => empty cell
        self.neighbors:dict = self.build_graph() # {variable : neighbor cells}
        self.domains:dict = self.initialize_domains() # { (r,c) : [valid_values] }
        self.assignments:dict = self.initialize_assignments() # { (r, c) : value}



    def solve(self):
        if not self.AC3():
            return None # doesn't admit any solution
        return self.back_tracking_search(self.assignments)



    def initialize_domains(self):
        domains = {}
        all_values = set(range(1,10))
        for r in range(9):
            for c in range(9):
                index = r * 9 + c
                value = int(self.board[index])
                cell = (r, c)

                if(value == 0):
                    domains[cell] = set(all_values)
                else:
                    domains[cell] = {value}
        return domains
    


    def initialize_assignments(self):
        assignments = {}
        for r in range(9):
            for c in range(9):
                index = r * 9 + c
                value = int(self.board[index])
                cell = (r, c)
                if(value != 0):
                    assignments[cell] = value
        return assignments



    def build_graph(self):
        # creating a list containing all sudoku cells: (0,0) ..., (8,8)
        cells = []
        for r in range(9):
            for c in range(9):
                cells.append((r,c))

        neighbors = {} # {cell : neighbors}

        for (r, c) in cells:
            constraints = set() # using a set to avoid duplicates

            # scanning row neighbors
            for c2 in range(9):
                if(c2 != c): # making sure I don't count the current cell
                    row_neighbor = (r, c2)
                    constraints.add(row_neighbor)
        
            # scanning column neighbors
            for r2 in range(9):
                if(r2 != r):
                    col_constraint = (r2, c)
                    constraints.add(col_constraint)
            
            # finding the 3x3 box's start of where the cell belongs
            start_x = (r // 3) * 3;
            start_y = (c // 3) * 3;

            # scanning box neighbors
            for box_row in range(start_x, start_x + 3):
                for box_col in range(start_y, start_y + 3):
                    if (box_row, box_col) != (r, c): 
                        box_constraint = (box_row, box_col)
                        constraints.add(box_constraint)
            
            neighbors[(r, c)] = constraints
    
        return neighbors



    def AC3(self):
        Q = []

        # initializing the queue with all the edges of the neighbors graph
        for Xi in self.neighbors.keys():
            for Xj in self.neighbors[Xi]:
                edge = (Xi, Xj)
                Q.append(edge)

        while len(Q) > 0:
            (Xi, Xj) = Q.pop(0)
            if self.revise(Xi, Xj, self.domains):
                if len(self.domains[Xi]) == 0:
                    return False
                for Xk in self.neighbors[Xi]:
                    if(Xk != Xj):
                        Q.append((Xk, Xi))
        return True



    def revise(self, Xi, Xj, domains):
        revised = False
        invalid_values = []  
        
        for x in domains[Xi]:
            valid = False
            for y in domains[Xj]:
                if(x != y):
                    valid = True
                    break
            if not valid:
                invalid_values.append(x)
                revised = True
        
        for x in invalid_values:
            domains[Xi].remove(x)
        return revised



    def back_tracking_search(self, assignments):
        # base case
        if len(assignments) == 81:
            return assignments
        
        # variable selection (MRV)
        X = self.select_minimum_remaining_var(assignments)
        
        # ordering variable's domain (LCV)
        for value in self.order_domain(X, assignments):
            # checking if the value is consistent with the assignments
            consistent = True
            for neighbor in self.neighbors[X]:
                if neighbor in assignments and assignments[neighbor] == value:
                    consistent = False
                    break
                   
            if consistent: # attempting to assign the value
                assignments[X] = value
                removals = self.forward_checking(X, value) # doing inference

                if removals != None: # if inference succeds, I go deeper
                    result = self.back_tracking_search(assignments)
                    
                    if result != None:
                        # if result is not None it means calls are returning the assignments dict
                        return result
                    # if result is None => inference failed => undo inference through the levels
                    for cell, value in removals.items():
                        self.domains[cell].add(value)
                del assignments[X] # if inference fails, it means some Domain is empty => undo assignment
        return None # sub-tree failed, has no solution => prev calls try other variables



    def forward_checking(self, X, value):
        removals = {} # {neighbor : [removed_variables]}
        for neighbor in self.neighbors[X]:
            if value in self.domains[neighbor]:

                self.domains[neighbor].remove(value)
                removals[neighbor] = value

                if(len(self.domains[neighbor]) == 0): # if domain is empty I undo the inference locally
                    for cell, value in removals.items():
                        self.domains[cell].add(value)
                    return None
        return removals
    


    def select_minimum_remaining_var(self, assignments):
        best_var = None
        min_domain_size = 10
        for r in range(9):
            for c in range(9):
                cell = (r, c)

                if cell in assignments: # skipping already assigned variables
                    continue
                
                current_domain_size = len(self.domains[cell])

                if(current_domain_size < min_domain_size):
                    min_domain_size = current_domain_size
                    best_var = cell
                
                # if current minimum domain size == 1 => can't do better so I exit
                if min_domain_size == 1:
                    return best_var
        return best_var
    


    def order_domain(self, X, assignments):
        # implementing ordered_domain based on least constraining values heuristic

        # Idea: for each value in the domain, i look for the occurrences in the neighbors graph, 
        # and I save the information in a dictionary {x \in D_{X} : # occurrences}.
        # then I order the map based on the # of occurrences and return the ordered domain values.

        current_domain = list(self.domains[X])
        occurrences_map = {} # dizionario {x \in D_{X} : # occurrences in the neighbors graph}
        for value in current_domain:
            count = 0

            for neighbor in self.neighbors[X]:

                if neighbor not in assignments: # se un vicino è stato già assegnato lo skippo
                    if value in self.domains[neighbor]:
                        count += 1

            occurrences_map[value] = count

        ordered_occurrences_map = sorted(occurrences_map.items(), key = lambda pair : pair[1])
        # specifying to order based on the # of occurrences

        ordered_domain = []
        for value, count in ordered_occurrences_map:
            ordered_domain.append(value)

        return ordered_domain