import re

ROCK_INTERVAL_REGEX = r"(^| )(?=((\d+,\d+) -> (\d+,\d+)))"

SAND_STARTING_POS = (500, 0)

def parse_rock_interval(*pos_strs):
    start_pos, end_pos = (
        tuple(map(int, pos_str.split(",")))
        for pos_str in pos_strs
    )

    if start_pos > end_pos:
        start_pos, end_pos = end_pos, start_pos

    if start_pos[0] == end_pos[0]:
        yield from ((start_pos[0], i) for i in range(start_pos[1], end_pos[1] + 1))
    if start_pos[1] == end_pos[1]:
        yield from ((i, start_pos[1]) for i in range(start_pos[0], end_pos[0] + 1))

with open("input.txt") as file:
    obstacles = {
        rock_pos
        for line in file.read().splitlines()
        for match in re.findall(ROCK_INTERVAL_REGEX, line)
        for rock_pos in parse_rock_interval(match[2], match[3])
    }

highest_y = max(pos[1] for pos in obstacles)

rested_units_n = 0
max_capacity_reached = False

while True:
    sand_pos = SAND_STARTING_POS

    while True:
        if sand_pos[1] + 1 > highest_y:
            max_capacity_reached = True
            break

        if (new := (sand_pos[0], sand_pos[1] + 1)) not in obstacles:
            sand_pos = new
        elif (new := (sand_pos[0] - 1, sand_pos[1] + 1)) not in obstacles:
            sand_pos = new
        elif (new := (sand_pos[0] + 1, sand_pos[1] + 1)) not in obstacles:
            sand_pos = new
        else:
            rested_units_n += 1
            obstacles.add(sand_pos)
            break

    if max_capacity_reached:
        break

print(rested_units_n)
