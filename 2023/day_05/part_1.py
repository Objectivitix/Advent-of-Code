def convert(number, map_):
    for source, offset in map_.items():
        if number in source:
            return number + offset

    return number

with open("input.txt") as file:
    inp = file.read().split("\n\n")

maps = []

for map_raw in inp[1:]:
    map_ = {}

    for entry in map_raw.splitlines()[1:]:
        dest_start, source_start, length = map(int, entry.split())
        offset = dest_start - source_start

        map_[range(source_start, source_start + length)] = offset

    maps.append(map_)

*numbers, = map(int, inp[0].split(": ")[1].split())

for map_ in maps:
    for i, number in enumerate(numbers):
        numbers[i] = convert(number, map_)

print(min(numbers))
