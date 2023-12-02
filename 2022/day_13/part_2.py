TIE = "tie"

DIVIDER_PACKETS = [[[2]], [[6]]]

import math
from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest

def is_ordered_correctly(packet1, packet2):
    for value1, value2 in zip_longest(packet1, packet2):
        if value1 is None:
            return -1
        if value2 is None:
            return 1

        value1_is_int = isinstance(value1, int)
        value2_is_int = isinstance(value2, int)

        if value1_is_int and value2_is_int:
            if value1 == value2:
                continue
            return value1 - value2

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
        literal_eval(packet)
        for pair in file.read().split("\n\n")
        for packet in pair.splitlines()
    ]

sorted_packets = sorted(
    input + DIVIDER_PACKETS,
    key=cmp_to_key(is_ordered_correctly)
)

decoder_key = math.prod(
    sorted_packets.index(divider_packet) + 1
    for divider_packet in DIVIDER_PACKETS
)

print(decoder_key)
