# Constraint.py
# Eisner Oct 2017
#
# This class wraps a dictionary of constraints, and has methods to find
# whether an assignment satisfies a constraint, and whether a variable is
# involved in a constraint.


class Constraint:
    def __init__(self):
        """
        Key is a pair of integers corresponding to indices of CSP
        variables involved in constraint, value is a list of pairs
        of integers that represent allowable combinations of
        values for the key.
        """
        self.c = dict()

    def add_constraint(self, k, v):
        """
        Adds a constraint
        :param k: tuple containing a pair of variables
        :param v: list of tuples containing legal values
        """
        self.c[k] = v

    def is_satisfied(self, assignment):
        """
        Figures out whether assignment satisfies the
        constraints
        :param assignment: partial or complete assignment
        :return: boolean whether assignment satisfies the constraints
        """
        for k, v in self.c.items():
            assignment_to_check = assignment[k[0]], assignment[k[1]]
            if assignment_to_check not in v and -1 not in assignment_to_check:
                return False

        return True

    def involves(self, variable):
        """
        Finds constraints related to variable
        :param variable: variable to test
        :return: constraints related to variable
        """
        constraints = []
        for k, v in self.c.items():
            if variable in k:
                constraints.append(k)

        return constraints



