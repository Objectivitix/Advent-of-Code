import re
from itertools import cycle

START = "AAA"
END = "ZZZ"

def parse_adj_list(raw):
    adj_list = {}

    for line in raw:
        node, *neighbors = re.findall(r"[A-Z]{3}", line)
        adj_list[node] = neighbors

    return adj_list

with open("input.txt") as file:
    inp = file.read().split("\n\n")

INSTRUCTIONS = inp[0]
NETWORK = parse_adj_list(inp[1].splitlines())

curr = START

for steps_n, instruction in enumerate(cycle(INSTRUCTIONS)):
    if curr == END:
        break

    curr = NETWORK[curr][instruction == "R"]

print(steps_n)
