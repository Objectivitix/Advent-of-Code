import functools
import re

CONTIGUOUS_GROUP_RE = (
    r"(?=("
    r"^[?#]{{{length}}}(?=[?\.])"
    r"|(?<=[?\.])[?#]{{{length}}}$"
    r"|^[?#]{{{length}}}$"
    r"|(?<=[?\.])[?#]{{{length}}}(?=[?\.])"
    r"))"
)


def parse_raw(file):
    for line in file.read().splitlines():
        springs, condition = line.split()

        yield (
            "?".join(springs for _ in range(5)),
            tuple(map(int, condition.split(","))) * 5
        )


def clear(springs):
    return springs.replace("?", ".")


def contains_contiguous_group(springs):
    pattern = CONTIGUOUS_GROUP_RE.replace(r"{{{length}}}", r"+")

    return bool(re.search(pattern, springs))


def get_possible_placements(springs, length):
    pattern = CONTIGUOUS_GROUP_RE.format(length=length)

    for match in re.finditer(pattern, springs):
        capture_start, capture_end = match.span(1)

        processed = clear(springs[:capture_start])
        if contains_contiguous_group(processed):
            continue

        yield capture_end + 1


@functools.cache
def count_ways(springs, condition):
    if not springs and condition:
        return 0

    if not condition:
        return not contains_contiguous_group(clear(springs))

    ways_n = 0

    for end in get_possible_placements(springs, condition[0]):
        sub_springs = springs[end:]
        sub_condition = condition[1:]

        ways_n += count_ways(sub_springs, sub_condition)

    return ways_n


with open("input.txt") as file:
    RECORD = list(parse_raw(file))

print(sum(
    count_ways(springs, condition)
    for springs, condition in RECORD
))
