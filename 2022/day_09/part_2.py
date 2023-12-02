KNOTS_N = 9

DIRECTION_DELTAS = {
    "U": 0+1j,
    "R": 1+0j,
    "D": 0-1j,
    "L": -1+0j,
}

KNOT_MOVEMENTS = {
    0+2j: 0+1j, 2+0j: 1+0j, 0-2j: 0-1j, -2+0j: -1+0j,
    1+2j: 1+1j, 2+2j: 1+1j, 2+1j: 1+1j, 2-1j: 1-1j, 2-2j: 1-1j, 1-2j: 1-1j,
    -1-2j: -1-1j, -2-2j: -1-1j, -2-1j: -1-1j, -2+1j: -1+1j, -2+2j: -1+1j, -1+2j: -1+1j,
}

with open("input.txt") as file:
    input = [
        ((motion := line.split())[0], int(motion[1]))
        for line in file.read().splitlines()
    ]

head_pos = 0+0j
knots_pos = [0+0j] * KNOTS_N

tail_trail = {0+0j}

for direction, steps in input:
    for _ in range(steps):
        head_pos += DIRECTION_DELTAS[direction]
        prev_knot_pos = head_pos

        for i, curr_knot_pos in enumerate(knots_pos):
            delta = prev_knot_pos - curr_knot_pos
            knots_pos[i] += KNOT_MOVEMENTS.get(delta, 0)

            prev_knot_pos = knots_pos[i]

        tail_trail.add(knots_pos[-1])

print(len(tail_trail))
