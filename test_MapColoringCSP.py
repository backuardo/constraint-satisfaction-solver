from MapColoringCSP import MapColoringCSP
from Constraint import Constraint

# test_MapColoringCSP.py
# Eisner Oct 2017
#
# Test MapColoringCSP.py with Australia map example from
# http://www.cs.dartmouth.edu/~devin/cs76/04_constraint/constraint.html

variable_strings = ['Western Australia', 'Northern Territory',
                    'South Australia', 'Queensland', 'New South Wales',
                    'Victoria', 'Tasmania']

colors = ['red', 'green', 'blue']

# Build Constraint object
ac = Constraint()

# Add some constraints
ac.add_constraint((0, 1), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((1, 0), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((0, 2), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((2, 0), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((1, 2), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((2, 1), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((1, 3), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((3, 1), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((2, 3), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((3, 2), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((3, 4), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((4, 3), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((4, 5), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((5, 4), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((2, 5), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])
ac.add_constraint((5, 2), [(0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0)])

# Finally, create a MapColoringCSP object
australia = MapColoringCSP(variable_strings, ac, colors,
                           mrv=True, lcv=True, ac3=True)

print(australia.solve())
