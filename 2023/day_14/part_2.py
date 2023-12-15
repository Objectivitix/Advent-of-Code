# Day 8 has taught me to hypothesize, test, and assume.
# So I hypothesized. I tested. This code assumes puzzle
# input spins itself into a cycle, whose period is
# small enough to result in a decent runtime.

import itertools

TIMES = 1_000_000_000

ROCK = "O"
WALL = "#"
SPACE = "."

DIRECTIONS = [0, 3, 2, 1]


def rotate(platform):
    return list(map(list, zip(*reversed(platform))))


def rectify(snapshot):
    direction, string = snapshot
    platform = [list(line) for line in string.splitlines()]

    for _ in range(direction):
        platform = rotate(platform)

    return platform


def stringify(platform):
    return "\n".join("".join(row) for row in platform)


def settle(i, j, platform):
    curr_i = i

    while curr_i - 1 >= 0 and platform[curr_i - 1][j] == SPACE:
        curr_i = curr_i - 1

    return curr_i, j


with open("input.txt") as file:
    *platform, = map(list, file.read().splitlines())

seen = []
cycle_start = None

for dir in itertools.cycle(DIRECTIONS):
    for i, line in enumerate(platform):
        for j, char in enumerate(line):
            if char != ROCK:
                continue

            new_i, new_j = settle(i, j, platform)

            platform[i][j] = SPACE
            platform[new_i][new_j] = ROCK

    snapshot = dir, stringify(platform)

    if snapshot in seen:
        cycle_start = seen.index(snapshot)
        break

    seen.append(snapshot)

    platform = rotate(platform)

cycle_period = len(seen) - cycle_start

index = (TIMES * 4 - cycle_start - 1) % cycle_period
final_platform = rectify(seen[cycle_start + index])

total_load = sum(
    load * line.count(ROCK)
    for load, line
    in enumerate(reversed(final_platform), 1)
)

print(total_load)
