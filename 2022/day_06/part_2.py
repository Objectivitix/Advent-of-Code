SLIDING_WINDOW_SPAN = 14

with open("input.txt") as file:
    input = file.read()

marker = None

length = len(input)

for start in range(length):
    end = start + SLIDING_WINDOW_SPAN

    window = input[start:end]
    if len(set(window)) == SLIDING_WINDOW_SPAN:
        marker = end
        break

print(marker)
