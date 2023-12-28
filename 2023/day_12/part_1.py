import re


def parse_raw(file):
    for line in file.read().splitlines():
        springs, condition = line.split()
        yield list(springs), list(map(int, condition.split(",")))


def get_unknown_indices(springs):
    for i, char in enumerate(springs):
        if char == "?":
            yield i


def get_subsets(n):
    for number in range(2 ** n):
        yield [int(bit) for bit in f"{number:0{n}b}"]


def get_possbilities(springs):
    indices = list(get_unknown_indices(springs))

    for subset in get_subsets(len(indices)):
        possibility = springs.copy()

        for include, index in zip(subset, indices):
            possibility[index] = "#" if include else "."

        yield possibility


def get_contiguous_groups(springs):
    for group in re.findall(r"#+", "".join(springs)):
        yield len(group)


with open("input.txt") as file:
    RECORD = list(parse_raw(file))

total = 0

for springs, condition in RECORD:
    for possibility in get_possbilities(springs):
        if list(get_contiguous_groups(possibility)) == condition:
            total += 1

print(total)
