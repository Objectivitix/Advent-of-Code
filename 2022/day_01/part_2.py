with open("input.txt") as file:
    input = [
        elf.split("\n")
        for elf in file.read().split("\n\n")
    ]

calorie_sums = [sum(int(line) for line in elf) for elf in input]

print(sum(sorted(calorie_sums)[-3:]))
