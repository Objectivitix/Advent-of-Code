from collections import Counter
from math import prod

with open("input.txt") as file:
    inp = file.read().splitlines()

powers = []

for line in inp:
    game = line.split(": ")[1].split("; ")
    cubes = Counter()

    for round in game:
        reveals = round.split(", ")

        for reveal in reveals:
            quantity, color = reveal.split()

            cubes |= {color: int(quantity)}

    powers.append(prod(cubes.values()))

print(sum(powers))
