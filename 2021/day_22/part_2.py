# Solution based on
# - https://observablehq.com/@jwolondon/advent-of-code-2021-day-22
# - https://beny23.github.io/posts/advent_of_code_2021_day_22/
#
# When adding every cuboid, I optimize by deleting
# identical intersections of opposite signs.

from __future__ import annotations
from math import prod
from typing import Literal, Optional
import re

CUBOID_REGEX = (
    r"(.+) "
    r"x=(-?\d+)..(-?\d+),"
    r"y=(-?\d+)..(-?\d+),"
    r"z=(-?\d+)..(-?\d+)"
)

Vertex = tuple[int, int, int]


class Cuboid:
    def __init__(
        self,
        top_left: Vertex,
        bottom_right: Vertex,
        sign: Literal[1, -1]
    ) -> None:
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.sign = sign

    @property
    def volume(self) -> int:
        return self.sign * prod(
            max(0, end - start + 1)
            for start, end
            in zip(self.top_left, self.bottom_right)
        )

    def __and__(self, other: Cuboid) -> Cuboid:
        candidate = Cuboid(
            tuple(map(max, zip(self.top_left, other.top_left))),
            tuple(map(min, zip(self.bottom_right, other.bottom_right))),
            -self.sign,  # mindblowing
        )

        return candidate if candidate.volume else None


def cancel_out(c1: Cuboid, c2: Cuboid) -> bool:
    return (
        c1.top_left == c2.top_left
        and c1.bottom_right == c2.bottom_right
        and c1.sign + c2.sign == 0
    )


def cancel_out_index(c: Cuboid, cuboids: list[Cuboid]) -> Optional[int]:
    for i, other in enumerate(cuboids):
        if cancel_out(c, other):
            return i

    return None


with open("input.txt") as file:
    inp = file.read().splitlines()

cuboids: list[Cuboid] = []

for line in inp:
    match = re.match(CUBOID_REGEX, line)

    cuboid = Cuboid(
        tuple(map(int, match.group(2, 4, 6))),
        tuple(map(int, match.group(3, 5, 7))),
        1 if match.group(1) == "on" else -1,
    )

    intersections = []

    for existing in cuboids:
        intersection = existing & cuboid

        if not intersection:
            continue

        cancel = cancel_out_index(intersection, intersections)

        if cancel is not None:
            del intersections[cancel]
            continue

        intersections.append(intersection)

    cuboids += intersections

    if cuboid.sign == 1:
        cuboids.append(cuboid)

print(sum(cuboid.volume for cuboid in cuboids))
