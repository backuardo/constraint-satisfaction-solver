import time
from math import inf
# CSP.py
# Eisner Oct 2017
#
#
# This class is a generic CSP solver that implements backtracking. Optional
# boolean parameters enable the search to run with MRV and LCV heuristics,
# as well as AC-3 inference.


class CSP:
    def __init__(self, variables, domain, constraints, mrv=False, lcv=False,
                 ac3=False):
        """
        :param variables: list of integers corresponding to string variables
        :param domain: list of sets of values, indices correspond to variables
        :param constraints: Constraint object with hash table of constraints
        :param mrv: boolean whether or not MRV is on
        :param lcv: boolean whether or not LCV is on
        :param ac3: boolean whether or not AC3 is on
        """
        self.variables = variables
        self.domain = domain
        self.constraints = constraints
        self.adjacency = []  # Will hold arcs
        self.mrv_on = mrv
        self.lcv_on = lcv
        self.ac3_on = ac3

        # Populate arcs for AC-3
        for v in self.variables:
            adj = set()
            for key in self.constraints.c:
                if v in key:
                    adj.add(key[0])
                    adj.add(key[1])
                    adj.remove(v)
            self.adjacency.append(adj)

    def backtracking_search(self):
        """
        Main backtracking search method

        :return: a solution, or failure
        """
        start_time = time.time()  # Mark start time

        # Initial assignment is -1 for each value
        initial_assignment = [(x * 0 - 1) for x in range(len(self.variables))]
        result = self.backtrack(initial_assignment)
        print('Run time: ', (time.time() - start_time))
        return result

    def backtrack(self, assignment):
        """
        Recursive backtracking search method

        :param assignment: values to some or all variables
        :return: a solution, or failure
        """
        result = None

        # Base case: complete assignment
        if self.is_complete(assignment):
            result = assignment

        # Using MRV or not?
        var = self.first_unassigned_variable(assignment) if not self.mrv_on \
            else self.minimum_remaining_value(assignment)

        # Insure there are some domain values for var
        if self.get_domain_values(var) is not None:

            # Using LCV or not?
            values = self.get_domain_values(var) if not self.lcv_on else \
                self.least_constraining_value(assignment, var)

            for value in values:
                if self.no_conflicts(assignment, var, value):
                    assignment[var] = value
                    domain_save = self.domain  # To revert back later

                    # Remove value from adjacent variables domains
                    self.domain[var] = value
                    neighbors = self.constraints.involves(var)
                    if neighbors:
                        for i, j in neighbors:
                            if i == var:
                                if type(self.domain[j]) is set:
                                    if value in self.domain[j]:
                                        self.domain[j].remove(value)
                            if j == var:
                                if type(self.domain[i]) is set:
                                    if value in self.domain[i]:
                                        self.domain[i].remove(value)

                    if self.ac3_on:
                        if self.ac3():
                            result = self.backtrack(assignment)
                            if result is not None:
                                return result
                            self.domain = domain_save

                    if not self.ac3_on:
                        result = self.backtrack(assignment)
                        if result is not None:
                            return result
                        self.domain = domain_save

                assignment[var] = -1  # Unassign
        return result

    def ac3(self):
        """
        Returns false if an inconsistency is found and true otherwise
        """
        # Use .append() and .pop(0) to maintain FIFO
        arcs = [k for k in self.constraints.c]
        while arcs:
            (xi, xj) = arcs.pop(0)
            if self.revise(xi, xj):
                if self.domain[xi] == 0:
                    return False
                self.adjacency[xi].remove(xj)
                for adjacent in self.adjacency[xi]:
                    arcs.append((adjacent, xi))
        return True

    def revise(self, xi, xj):
        """
        Returns true if we revise the domain of xi
        """
        revised = False

        dj = self.domain[xj].copy() \
            if type(self.domain[xj]) is set else {self.domain[xj]}
        di = self.domain[xi].copy() \
            if type(self.domain[xi]) is set else {self.domain[xi]}

        for x in di:
            constraint_satisfied = False
            for y in dj:
                if (x, y) in self.constraints.c[(xi, xj)]:
                    constraint_satisfied = True

            if not constraint_satisfied:
                self.domain[xi].remove(x)
                revised = True
        return revised

    def least_constraining_value(self, assignment, variable):
        """
        Prefers the value that rules out the fewest choices for neighboring
        values in the constraint graph.
        :param assignment: partial assignment
        :param variable: variable we are ordering values for
        :return: list of values sorted by least number of conflicts caused
        """
        variable_conflicts = []  # Tuples (variable, number_conflicts)

        # Only one value
        if type(self.domain[variable]) is int:
            return self.domain[variable]

        # More than one value
        for value in self.domain[variable]:
            variable_conflicts.append((value, self.number_conflicts(
                assignment, variable, value)))

        # Sort values and return
        s_values = sorted(variable_conflicts, key=lambda conflict: conflict[1])
        return [i[0] for i in s_values]

    def minimum_remaining_value(self, assignment):
        """
        Chooses variable with the fewest legal values
        :param assignment: partial assignment
        :return: variable with least values in domain
        """
        unassigned = []
        min_var = None
        min_value = inf

        for i in range(len(assignment)):
            if assignment[i] == -1:
                unassigned.append(i)

        for variable in unassigned:
            if type(self.domain[variable]) is set:
                if len(self.domain[variable]) < min_value:
                    min_var = variable
                    min_value = len(self.domain[variable])

        return min_var

    @staticmethod
    def first_unassigned_variable(assignment):
        """
        Used when MRV is off -- chooses first unassigned variable
        :param assignment: partial assignment
        :return: first unassigned variable
        """
        for value in assignment:
            if value == -1:
                return assignment.index(value)

        return None

    def get_domain_values(self, var):
        """
        :param var: variable to return domains of
        :return: a set of possible values for var
        """
        if var is not None:
            return self.domain[var]
        else:
            return None

    @staticmethod
    def is_complete(assignment):
        """
        Finds whether or not each variable has been assigned a value
        :param assignment: partial or full assignment
        :return: True if complete, else if incomplete
        """
        for value in assignment:
            if value == -1:
                return False
        return True

    def number_conflicts(self, assignment, variable, value):
        """
        Finds the number of conflicts that result from variable being
        assigned value
        :param assignment: partial assignment
        :param variable: variable to test
        :param value: value to test on variable
        :return: resulting number of conflicts
        """
        conflicts = 0
        for k, v in self.constraints.c.items():

            if k[0] == variable:
                for p in v:
                    if p[0] == value:
                        if assignment[k[1]] != -1 or assignment[k[1]] != p[1]:
                            conflicts += 1

            if k[1] == variable:
                for p in v:
                    if p[1] == value:
                        if assignment[k[0]] != -1 or assignment[k[0]] != p[0]:
                            conflicts += 1

        return conflicts

    def no_conflicts(self, assignment, variable, value):
        """
        Whether or not assigning value to variable causes a conflict
        :param assignment: partial assignment
        :param variable: variable to assign
        :param value: value to assign to variable
        :return: whether there are no conflicts or not
        """
        for k, v in self.constraints.c.items():

            if k[0] == variable:
                match = False
                for p in v:
                    if p[0] == value:
                        if assignment[k[1]] == -1 or assignment[k[1]] == p[1]:
                            match = True
                if not match:
                    return False

            if k[1] == variable:
                match = False
                for p in v:
                    if p[1] == value:
                        if assignment[k[0]] == -1 or assignment[k[0]] == p[0]:
                            match = True
                if not match:
                    return False

        return True

