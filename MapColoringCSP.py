from CSP import CSP

# MapColoringMapColoringCSP.py
# Eisner Oct 2017
#
# This class is a wrapper for a map coloring CSP problem that returns a
# readable output


class MapColoringCSP(CSP):
    def __init__(self, variables, constraints, values, mrv=False,
                 lcv=False, ac3=False):
        """
        :param variables: list of string names for variables
        :param constraints: Constraint object with hash table
        :param values: possible colors
        :param mrv: boolean whether or not MRV is on
        :param lcv: boolean whether or not LCV is on
        :param ac3: boolean whether or not AC3 is on
        """
        self.variables_list = variables
        self.domain = []
        self.constraints = constraints
        self.values_list = values
        self.variables = [i for i in range(len(self.variables_list))]
        self.domain_int = []
        self.mrv = mrv
        self.lcv = lcv
        self.ac3 = ac3

        # Populate domain
        for i in range(len(self.variables_list)):
            self.domain.append({i for i in range(len(self.values_list))})

        # Build CSP object
        self.csp = CSP(self.variables, self.domain, self.constraints,
                       self.mrv, self.lcv, self.ac3)

    def solve(self):
        """
        Calls backtracking_search
        :return: nice string representation of assignment
        """
        assignment = self.csp.backtracking_search()
        return self.__str__(assignment)

    def __str__(self, assignment):
        result = ''
        for i in range(len(assignment)):
            result += 'Color for '
            result += (self.variables_list[i] + ': ')
            result += (self.values_list[assignment[i]] + '\n')

        print('Map Color CSP')
        print('Variables: ', self.variables_list)
        print('Assignment: ', assignment)
        print('Using MRV? ', self.mrv)
        print('Using LCV? ', self.lcv)
        print('Using AC3? ', self.ac3)
        return result
