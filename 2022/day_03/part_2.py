ELF_CHUNKS = 3
LOWER_OFFSET = 96
UPPER_OFFSET = 38

def calculate_priority(item):
    return ord(item) - (LOWER_OFFSET if item.islower() else UPPER_OFFSET)

with open("input.txt") as file:
    raw = file.read().splitlines()
    input = [raw[i:i+ELF_CHUNKS] for i in range(0, len(raw), ELF_CHUNKS)]

priorities = 0

for chunk in input:
    unique_chunk = [set(rucksack) for rucksack in chunk]

    for item in set("".join(chunk)):
        if all(item in rucksack for rucksack in unique_chunk):
            priorities += calculate_priority(item)

print(priorities)
