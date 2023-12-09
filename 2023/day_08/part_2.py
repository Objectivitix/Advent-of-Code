# A hacky solution based on two major assumptions
# that happen to hold true for all puzzle inputs:
#
#    1. for every start node, traversal falls into
#       a cycle, in which there is one unique
#       corresponding end node every period;
#
#    2. the number of steps from a start node to its
#       corresponding end node is equal to that from
#       the end node to itself (offset = period).
#
# Then it is simply a matter of synchronizing large
# loops, i.e. using LCM.

import math
import re
from itertools import cycle

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

currs = [node for node in NETWORK if node.endswith("A")]

periods = []

for curr in currs:
    for steps_n, instruction in enumerate(cycle(INSTRUCTIONS)):
        if curr.endswith("Z"):
            break

        curr = NETWORK[curr][instruction == "R"]

    periods.append(steps_n)

print(math.lcm(*periods))
