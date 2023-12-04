with open("input.txt") as file:
    inp = file.read().splitlines()

total = 0

for line in inp:
    winning, given = (
        {int(num) for num in lst.split()}
        for lst in line.split(": ")[1].split(" | ")
    )

    won_n = len(winning & given)

    if won_n:
        total += 2 ** (won_n - 1)

print(total)
