import functools
import re

CONTIGUOUS_GROUP_RE = (
    r"^[?#]{{{length}}}(?=[?\.])"
    r"|(?<=[?\.])[?#]{{{length}}}$"
    r"|^[?#]{{{length}}}$"
    r"|(?<=[?\.])[?#]{{{length}}}(?=[?\.])"
)


def parse_raw(file):
    for line in file.read().splitlines():
        springs, condition = line.split()

        yield (
            "?".join(springs for _ in range(5)),
            tuple(map(int, condition.split(","))) * 5
        )


def overlap(regex):
    return r"(?=({}))".format(regex)


def get_possible_placements(springs, length):
    pattern = overlap(CONTIGUOUS_GROUP_RE.format(length=length))

    for match in re.finditer(pattern, springs):
        capture_start, capture_end = match.span(1)

        if "#" in springs[:capture_start]:
            continue

        yield capture_end + 1


@functools.cache
def count_ways(springs, condition):
    if not springs and condition:
        return 0

    if not condition:
        return "#" not in springs

    return sum(
        count_ways(springs[end:], condition[1:])
        for end in get_possible_placements(springs, condition[0])
    )


with open("input.txt") as file:
    RECORD = list(parse_raw(file))

print(sum(
    count_ways(springs, condition)
    for springs, condition in RECORD
))
