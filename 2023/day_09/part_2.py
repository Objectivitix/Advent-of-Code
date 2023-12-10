from itertools import pairwise


def get_differences(seq):
    for a, b in pairwise(seq):
        yield b - a


def are_constant(seq):
    return len(set(seq)) == 1


with open("input.txt") as file:
    SEQUENCES = [
        [int(number) for number in line.split()]
        for line in file.read().splitlines()
    ]

total = 0

for seq in SEQUENCES:
    diffs = [seq.copy()]

    while True:
        curr_diffs = diffs[-1]

        if are_constant(curr_diffs):
            break

        diffs.append(list(get_differences(curr_diffs)))

    rev_diffs = reversed(diffs)
    prev_term = next(rev_diffs)[0]

    for diff in rev_diffs:
        prev_term = diff[0] - prev_term

    total += prev_term

print(total)
