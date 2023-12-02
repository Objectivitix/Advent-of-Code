TIE = "tie"

from ast import literal_eval
from itertools import zip_longest

def is_ordered_correctly(packet1, packet2):
    for value1, value2 in zip_longest(packet1, packet2):
        if value1 is None:
            return True
        if value2 is None:
            return False

        value1_is_int = isinstance(value1, int)
        value2_is_int = isinstance(value2, int)

        if value1_is_int and value2_is_int:
            if value1 == value2:
                continue
            return value1 < value2

        if not value1_is_int and not value2_is_int:
            if (res := is_ordered_correctly(value1, value2)) == TIE:
                continue
            return res

        if value1_is_int:
            if (res := is_ordered_correctly([value1], value2)) == TIE:
                continue
            return res

        if value2_is_int:
            if (res := is_ordered_correctly(value1, [value2])) == TIE:
                continue
            return res

    return TIE

with open("input.txt") as file:
    input = [
        tuple(literal_eval(operand) for operand in pair.splitlines())
        for pair in file.read().split("\n\n")
    ]

indices_sum = sum(
    i + 1
    for i, pair in enumerate(input)
    if is_ordered_correctly(*pair)
)

print(indices_sum)
