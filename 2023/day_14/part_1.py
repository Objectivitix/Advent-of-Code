ROCK = "O"
WALL = "#"
SPACE = "."


def settle(i, j, platform):
    curr_i = i

    while curr_i - 1 >= 0 and platform[curr_i - 1][j] == SPACE:
        curr_i = curr_i - 1

    return curr_i, j


with open("input.txt") as file:
    *platform, = map(list, file.read().splitlines())

for i, line in enumerate(platform):
    for j, char in enumerate(line):
        if char != ROCK:
            continue

        new_i, new_j = settle(i, j, platform)

        platform[i][j] = SPACE
        platform[new_i][new_j] = ROCK

total_load = sum(
    load * line.count(ROCK)
    for load, line
    in enumerate(reversed(platform), 1)
)

print(total_load)
