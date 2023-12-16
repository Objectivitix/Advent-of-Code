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


def get_diag(start, end):
    curr = start

    while curr != end:
        yield curr
        curr = curr[0] + 1, curr[1] - 1

    yield curr


def get_diags(m, n):
    starts = [
        *((0, j) for j in range(n)),
        *((i, n - 1) for i in range(1, m))
    ]

    ends = [
        *((i, 0) for i in range(m)),
        *((m - 1, j) for j in range(1, n))
    ]

    for start, end in zip(starts, ends):
        yield list(get_diag(start, end))


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

for diag in get_diags(HEIGHT, WIDTH):
    # Scan diagonally to eliminate ambiguity.
    # Corners are essentially encountering two pipes.
    line = (
        "".join(cleaned[i][j] for (i, j) in diag)
        .replace("F", "-|")
        .replace("J", "|-")
    )

    indices = []

    for i, char in enumerate(line):

        # A pipe marks an inside-outside flip.
        # Remember that S is a pipe, too!
        if char in "-|7LS":
            indices.append(i)

    for a, b in chunk(indices, 2):
        total += b - a - 1

print(total)
