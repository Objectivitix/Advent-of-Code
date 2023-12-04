import re

NON_SYMBOLS = "0123456789."

def get_adj(i, start_j, end_j):
    for j in range(start_j - 1, end_j + 1):
        yield i - 1, j
        yield i + 1, j

    yield i, start_j - 1
    yield i, end_j

def get_adj_bounded(i, start_j, end_j, m, n):
    for adj_i, adj_j in get_adj(i, start_j, end_j):
        if 0 <= adj_i < m and 0 <= adj_j < n:
            yield adj_i, adj_j

with open("input.txt") as file:
    inp = file.read().splitlines()

DIMS = len(inp), len(inp[0])

part_numbers = []

for i, line in enumerate(inp):
    for match in re.finditer("\d+", line):

        for adj_i, adj_j in get_adj_bounded(i, *match.span(), *DIMS):
            if inp[adj_i][adj_j] not in NON_SYMBOLS:
                part_numbers.append(match.group())

print(sum(map(int, part_numbers)))
