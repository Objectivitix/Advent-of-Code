LOWER_OFFSET = 96
UPPER_OFFSET = 38

def calculate_priority(item):
    return ord(item) - (LOWER_OFFSET if item.islower() else UPPER_OFFSET)

with open("input.txt") as file:
    input = file.read().splitlines()

priorities = 0

for line in input:
    middle = int(len(line) / 2)
    unique_a = set(line[:middle])
    unique_b = set(line[middle:])

    for item in {*unique_a, *unique_b}:
        if item in unique_a and item in unique_b:
            priorities += calculate_priority(item)

print(priorities)
