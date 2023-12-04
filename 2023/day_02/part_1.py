BAG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

with open("input.txt") as file:
    inp = file.read().splitlines()

possible_games = []

for i, line in enumerate(inp, 1):
    game = line.split(": ")[1].split("; ")
    possible = True

    for round in game:
        reveals = round.split(", ")

        for reveal in reveals:
            quantity, color = reveal.split()

            if int(quantity) > BAG[color]:
                possible = False

    if possible:
        possible_games.append(i)

print(sum(possible_games))
