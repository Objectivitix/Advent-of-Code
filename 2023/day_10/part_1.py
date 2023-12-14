from collections import defaultdict

DELTAS = {
    "north": (-1, 0),
    "east": (0, 1),
    "south": (1, 0),
    "west": (0, -1),
}

OUT = {
    "S": ["north", "east", "south", "west"],
    ".": [],
    "|": ["north", "south"],
    "-": ["east", "west"],
    "L": ["north", "east"],
    "J": ["north", "west"],
    "7": ["south", "west"],
    "F": ["south", "east"],
}

IN = {
    "north": "7|FS",
    "east": "J-7S",
    "south": "J|LS",
    "west": "L-FS",
}


def get_adj(i, j, dir):
    di, dj = DELTAS[dir]
    return i + di, j + dj


def get_adjs(i, j, dirs, m, n):
    for dir in dirs:
        adj_i, adj_j = get_adj(i, j, dir)

        if 0 <= adj_i < m and 0 <= adj_j < n:
            yield adj_i, adj_j, dir


def parse_raw(raw):
    dims = len(raw), len(raw[0])

    start_pos = None
    adj_list = defaultdict(list)

    for i, line in enumerate(raw):
        for j, char in enumerate(line):

            if char == "S":
                start_pos = i, j

            for adj_i, adj_j, dir in get_adjs(i, j, OUT[char], *dims):
                if raw[adj_i][adj_j] in IN[dir]:
                    adj_list[i, j].append((adj_i, adj_j))

    return start_pos, adj_list


with open("input.txt") as file:
    RAW = file.read().splitlines()

START, MAZE = parse_raw(RAW)

curr = START
visited = {START}

loop_closed = False
loop_length = 1

while True:
    for neighbor in MAZE[curr]:
        if neighbor == START and loop_length > 2:
            loop_closed = True
            break

        if neighbor in visited:
            continue

        curr = neighbor
        visited.add(neighbor)
        loop_length += 1
        break

    if loop_closed:
        break

print(f"{loop_length / 2:.0f}")
