import re

ADD_REGEX = r"addx (-?\d+)"
NOOP_REGEX = r"noop"

SIGNAL_START_CYCLE = 20
SIGNAL_GAP = 40
SIGNAL_N = 6

SIGNAL_INDICES = [
    SIGNAL_START_CYCLE - 1 + SIGNAL_GAP * i
    for i in range(SIGNAL_N)
]

with open("input.txt") as file:
    input = file.read().splitlines()

values_per_cycle = []
curr_value = 1

for line in input:
    if out := re.match(ADD_REGEX, line):
        values_per_cycle += [curr_value] * 2
        curr_value += int(out.group(1))
    elif re.match(NOOP_REGEX, line):
        values_per_cycle.append(curr_value)

print(sum(
    values_per_cycle[index] * (index + 1)
    for index in SIGNAL_INDICES
))
