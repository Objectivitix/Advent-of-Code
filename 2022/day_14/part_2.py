import re

ROCK_INTERVAL_REGEX = r"(^| )(?=((\d+,\d+) -> (\d+,\d+)))"

SAND_STARTING_POS = (500, 0)
FLOOR_RELATIVE_Y = 2

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
floor_y = highest_y + FLOOR_RELATIVE_Y

rested_units_n = 0
source_blocked = False

while True:
    sand_pos = SAND_STARTING_POS

    while True:
        if sand_pos[1] + 1 == floor_y:
            rested_units_n += 1
            obstacles.add(sand_pos)
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
            if sand_pos == SAND_STARTING_POS:
                source_blocked = True

            if (expendable := (sand_pos[0], sand_pos[1] + 2)) in obstacles:
                obstacles.remove(expendable)

            break

    if source_blocked:
        break

print(rested_units_n)
