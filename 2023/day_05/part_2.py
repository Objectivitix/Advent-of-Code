from copy import copy


def chunk(iterable, n):
    iterators = [iter(iterable)] * n

    return zip(*iterators)


class Range:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __bool__(self):
        return self.stop > self.start

    def __and__(self, other):
        return Range(
            max(self.start, other.start),
            min(self.stop, other.stop),
        )

    def __hash__(self):
        return hash((self.start, self.stop))


def convert(range_, map_):
    to_process = copy(range_)
    dest_ranges = []

    for source, offset in map_.items():
        inter = source & to_process

        if not inter:
            continue

        if inter.start > to_process.start:
            dest = Range(to_process.start, inter.start)
            dest_ranges.append(dest)

        dest = Range(inter.start + offset, inter.stop + offset)
        dest_ranges.append(dest)

        to_process.start = inter.stop

    if to_process:
        dest_ranges.append(to_process)

    return dest_ranges


with open("input.txt") as file:
    inp = file.read().split("\n\n")

maps = []

for map_raw in inp[1:]:
    map_ = {}

    for entry in map_raw.splitlines()[1:]:
        dest_start, source_start, length = map(int, entry.split())
        offset = dest_start - source_start

        map_[Range(source_start, source_start + length)] = offset

    sorted_map = {
        range_: offset
        for range_, offset
        in sorted(map_.items(), key=lambda entry: entry[0].start)
    }

    maps.append(sorted_map)

ranges_raw = inp[0].split(": ")[1].split()

ranges = [
    Range(start, start + length)
    for start, length in chunk(map(int, ranges_raw), 2)
]

for map_ in maps:
    new_ranges = []

    for range_ in ranges:
        new_ranges += convert(range_, map_)

    ranges = new_ranges

print(min(range_.start for range_ in ranges))
