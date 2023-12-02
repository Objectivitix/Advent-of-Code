DIRECTION_DELTAS = {
    "U": 0+1j,
    "R": 1+0j,
    "D": 0-1j,
    "L": -1+0j,
}

TAIL_MOVEMENTS = {
    0+2j: 0+1j, 2+0j: 1+0j, 0-2j: 0-1j, -2+0j: -1+0j,
    1+2j: 1+1j, 2+1j: 1+1j, 2-1j: 1-1j, 1-2j: 1-1j,
    -1-2j: -1-1j, -2-1j: -1-1j, -2+1j: -1+1j, -1+2j: -1+1j,
}

with open("input.txt") as file:
    input = [
        ((motion := line.split())[0], int(motion[1]))
        for line in file.read().splitlines()
    ]

head_pos = 0+0j
tail_pos = 0+0j

tail_trail = {0+0j}

for direction, steps in input:
    for _ in range(steps):
        head_pos += DIRECTION_DELTAS[direction]

        delta = head_pos - tail_pos
        tail_pos += TAIL_MOVEMENTS.get(delta, 0)

        tail_trail.add(tail_pos)

print(len(tail_trail))
