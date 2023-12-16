# I was so excited for this linear algebra
# solution to work! But I think some precision
# error is preventing greatness. I'm not sure
# how to resolve it - will come back later.

import numpy as np
from numpy.polynomial import Polynomial as P


def are_constant(seq):
    return len(set(seq)) == 1


with open("input.txt") as file:
    SEQUENCES = np.genfromtxt(file, dtype=int)

next_total = 0
prev_total = 0

for seq in SEQUENCES:
    curr = seq.copy()
    degree = 0

    while not are_constant(curr):
        curr = np.diff(curr)
        degree += 1

    x = (
        np.arange(degree + 1)[:, np.newaxis]
        ** np.arange(degree, -1, -1)
    )

    y = np.array(seq[:degree + 1])

    coeffs = np.linalg.solve(x, y)

    polynomial = P(coeffs[::-1])

    next_total += polynomial(len(seq))
    prev_total += polynomial(-1)

print(round(next_total), round(prev_total))
