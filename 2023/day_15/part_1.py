def hash_(string):
    num = 0

    for char in string:
        num += ord(char)
        num *= 17
        num %= 256

    return num

with open("input.txt") as file:
    SEQUENCE = file.read().split(",")

print(sum(hash_(string) for string in SEQUENCE))
