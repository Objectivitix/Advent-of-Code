import re

def parse_crates(line, stacks_n):
    for i in range(stacks_n):
        yield line[i * 4 + 1]

with open("input.txt") as file:
    stacks_raw, procedure_raw = (
        raw.splitlines()
        for raw in file.read().split("\n\n")
    )

    stacks_n = int(stacks_raw[-1][-2])
    stacks = [[] for _ in range(stacks_n)]

    for line in stacks_raw[-2::-1]:
        for i, crate in enumerate(parse_crates(line, stacks_n)):
            if crate != " ":
                stacks[i].append(crate)

    procedure = [
        tuple(map(int, re.findall(r"\d+", line)))
        for line in procedure_raw
    ]

for qty, from_index, to_index in procedure:
    from_crate = stacks[from_index - 1]
    to_crate = stacks[to_index - 1]

    for _ in range(qty):
        to_crate.append(from_crate.pop())

print("".join(stack[-1] for stack in stacks))
