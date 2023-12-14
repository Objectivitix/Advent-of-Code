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


def chunk(iterable, n):
    iterators = [iter(iterable)] * n

    return zip(*iterators)


def get_adj(i, j, dir):
    di, dj = DELTAS[dir]
    return i + di, j + dj


def get_adjs(i, j, dirs, m, n):
    for dir in dirs:
        adj_i, adj_j = get_adj(i, j, dir)

        if 0 <= adj_i < m and 0 <= adj_j < n:
            yield adj_i, adj_j, dir


def get_diags(m, n):
    pass


def parse_raw(raw, dims):
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


def get_loop_set(start, maze):
    curr = start
    loop = {start}

    loop_closed = False
    loop_length = 1

    while True:
        for neighbor in maze[curr]:
            if neighbor == start and loop_length > 2:
                loop_closed = True
                break

            if neighbor in loop:
                continue

            curr = neighbor
            loop.add(neighbor)
            loop_length += 1
            break

        if loop_closed:
            break

    return loop


with open("input.txt") as file:
    RAW = file.read().splitlines()

HEIGHT, WIDTH = len(RAW), len(RAW[0])

start, maze = parse_raw(RAW, (HEIGHT, WIDTH))
loop = get_loop_set(start, maze)

cleaned = [
    [RAW[i][j] if (i, j) in loop else "." for j in range(WIDTH)]
    for i in range(HEIGHT)
]

total = 0

for diag in get_diags(WIDTH, HEIGHT):
    print(diag)
    line = (
        "".join(cleaned[i][j] for (i, j) in diag)
        .replace("7", "-|")
        .replace("L", "|-")
    )

    indices = []

    for i, char in enumerate(line):
        if char in "-|FJ":
            indices.append(i)

    print(line)
    # print(list(chunk(indices, 2)))
    for a, b in chunk(indices, 2):
        total += b - a - 1

print(total)
# print("\n".join("".join(row) for row in cleaned).translate(str.maketrans("|-LJ7F", "│─└┘┐┌")))
