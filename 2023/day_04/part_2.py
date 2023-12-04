with open("input.txt") as file:
    inp = file.read().splitlines()

cards_n = [1 for _ in enumerate(inp)]

for i, line in enumerate(inp):
    winning, given = (
        {int(num) for num in lst.split()}
        for lst in line.split(": ")[1].split(" | ")
    )

    won_n = len(winning & given)

    for k in range(1, won_n + 1):
        cards_n[i + k] += cards_n[i]

print(sum(cards_n))
