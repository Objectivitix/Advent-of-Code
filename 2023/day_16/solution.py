from collections import deque

N, E, S, W = -1, 1j, 1, -1j

OPTICS = {
    ".": {N: N, E: E, S: S, W: W},
    "/": {N: E, E: N, S: W, W: S},
    "\\": {N: W, E: S, S: E, W: N},
    "|": {N: N, E: [N, S], S: S, W: [N, S]},
    "-": {N: [E, W], E: E, S: [E, W], W: W},
}


def parse_input(file):
    inp = file.read().splitlines()

    yield len(inp)
    yield len(inp[0])

    contraption = {}

    for i, line in enumerate(inp):
        for j, char in enumerate(line):
            if char in OPTICS:
                contraption[complex(i, j)] = char

    yield contraption


with open("input.txt") as file:
    HEIGHT, WIDTH, CONTRAPTION = parse_input(file)


def energize(start_state):
    laser_heads = deque()
    laser_heads.append(start_state)

    seen_states = set()

    while laser_heads:
        prev_dir, pos = laser_heads.popleft()

        if (prev_dir, pos) in seen_states:
            continue

        if not (0 <= pos.real < HEIGHT and 0 <= pos.imag < WIDTH):
            continue

        seen_states.add((prev_dir, pos))

        tile = CONTRAPTION.get(pos, ".")
        next_ = OPTICS[tile][prev_dir]

        if not isinstance(next_, list):
            laser_heads.append((next_, pos + next_))
            continue

        for dir in next_:
            laser_heads.append((dir, pos + dir))

    return len({pos for _, pos in seen_states})


def part_one():
    return energize((E, 0+0j))


def part_two():
    start_states = [
        *((N, complex(HEIGHT - 1, j)) for j in range(WIDTH)),
        *((E, complex(i, 0)) for i in range(HEIGHT)),
        *((S, complex(0, j)) for j in range(WIDTH)),
        *((W, complex(i, WIDTH - 1)) for i in range(HEIGHT)),
    ]

    return max(energize(start) for start in start_states)


print(part_one())
print(part_two())
