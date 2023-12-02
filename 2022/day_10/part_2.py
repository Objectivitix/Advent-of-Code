import re

ADD_REGEX = r"addx (-?\d+)"
NOOP_REGEX = r"noop"

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6
DARK_PIXEL = ".."
LIT_PIXEL = "##"

SPRITE_WIDTH = 3
SPRITE_SPAN_OFFSETS = [
    SPRITE_WIDTH // 2 - i
    for i in range(SPRITE_WIDTH)
]

with open("input.txt") as file:
    input = file.read().splitlines()

values_per_cycle = []
curr_value = 1

for line in input:
    if out := re.match(ADD_REGEX, line):
        values_per_cycle.extend([curr_value] * 2)
        curr_value += int(out.group(1))
    elif re.match(NOOP_REGEX, line):
        values_per_cycle.append(curr_value)

screen = [
    [DARK_PIXEL] * SCREEN_WIDTH
    for _ in range(SCREEN_HEIGHT)
]

crt_pos = (0, 0)  # y, x

for cycle, sprite_center_pos in enumerate(values_per_cycle):
    sprite_posset = tuple(
        sprite_center_pos + offset
        for offset in SPRITE_SPAN_OFFSETS
    )

    if crt_pos[1] in sprite_posset:
        screen[crt_pos[0]][crt_pos[1]] = LIT_PIXEL

    crt_pos = divmod(cycle + 1, SCREEN_WIDTH)

print("\n".join("".join(row) for row in screen))
