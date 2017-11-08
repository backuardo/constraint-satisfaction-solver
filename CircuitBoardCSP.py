from CSP import CSP

# CircuitBoardCSP.py
# Eisner Oct 2017
#
# This class is a wrapper for a circuit board CSP problem that returns a
# readable output.


class CircuitBoardCSP(CSP):
    def __init__(self, variables, domain, constraints, values,
                 variables_dim, board, mrv=False,
                 lcv=False, ac3=False):
        """
        :param variables: list of string names for variables
        :param domain: list of sets of values in domains
        :param constraints: Constraint object with hash table
        :param values: possible locations for lower left corner of component
        :param variables_dim: dimensions of each variable
        :param board: dimensions of circuit board
        :param mrv: boolean whether or not MRV is on
        :param lcv: boolean whether or not LCV is on
        :param ac3: boolean whether or not AC3 is on
        """
        self.variables_list = variables
        self.domain = domain
        self.constraints = constraints
        self.values = values
        self.variables = [i for i in range(len(self.variables_list))]
        self.variables_dim = variables_dim
        self.board = board
        self.mrv = mrv
        self.lcv = lcv
        self.ac3 = ac3
        self.csp = CSP(self.variables, self.domain, self.constraints,
                       self.mrv, self.lcv)

    def solve(self):
        """
        Calls backtracking_search
        :return: nice string representation of assignment
        """
        assignment = self.csp.backtracking_search()
        return self.__str__(assignment)

    def __str__(self, assignment):
        """
        To string implementation, prints additional information
        :param assignment: complete assignment for CSP
        :return: ascii representation of circuit board
        """
        print('Circuit Board CSP')
        print('Variables: ', self.variables_list)
        print('Variable Dimensions: ', self.variables_dim)
        print('Assignment: ', assignment)
        print('Using MRV? ', self.mrv)
        print('Using LCV? ', self.lcv)
        print('Using AC3? ', self.ac3)

        to_color = set()

        for location in assignment:
            sx = location[0]
            sy = location[1]
            ex = sx + self.variables_dim[assignment.index(location)][0]
            ey = sy + self.variables_dim[assignment.index(location)][1]
            for y1 in range(sy, ey):
                for x1 in range(sx, ex):
                    to_color.add((x1, y1, self.variables_list[assignment.index(
                        location)]))

        ascii_board = ''

        for y2 in range((self.board[1] - 1), -1, -1):
            row = ''
            for x2 in range(0, self.board[0]):
                color = False
                for value in self.variables_list:
                    if (x2, y2, str(value)) in to_color:
                        row += str(value)
                        color = True
                if not color:
                    row += '.'
            ascii_board += (row + '\n')

        return ascii_board
