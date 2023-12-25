import re
from itertools import combinations
from math import isclose
from typing import Iterator, NamedTuple

AREA_MIN = 200_000_000_000_000
AREA_MAX = 400_000_000_000_000


class Point(NamedTuple):
    x: float
    y: float


class Velocities(NamedTuple):
    xv: float
    yv: float


class Line(NamedTuple):
    m: float
    b: float


def parse_raw(file) -> Iterator[tuple[Point, Velocities, Line]]:
    for line in file.read().splitlines():
        stone = map(int, re.findall(r"(-?\d+)", line))
        px, py, _, xv, yv, _ = stone

        m = yv / xv
        b = py - m * px

        yield Point(px, py), Velocities(xv, yv), Line(m, b)


def are_parallel(p: Line, q: Line) -> bool:
    return isclose(p.m, q.m)


def solve(p: Line, q: Line) -> Point:
    x = (q.b - p.b) / (p.m - q.m)
    y = p.m * x + p.b

    assert isclose(y, q.m * x + q.b)

    return Point(x, y)


def is_valid_intersection(
    r: Point,
    s: Point,
    t: Point,
    sv: Velocities,
    tv: Velocities,
) -> bool:
    in_area = all(AREA_MIN <= n <= AREA_MAX for n in r)

    in_future = all(
        rn > n and nv > 0
        or rn < n and nv < 0
        or rn == n and nv == 0
        for p, pv in zip((s, t), (sv, tv))
        for rn, n, nv in zip(r, p, pv)
    )

    return in_area and in_future


with open("input.txt") as file:
    HAIL = list(parse_raw(file))

total = 0

for (p_start, pv, p), (q_start, qv, q) in combinations(HAIL, 2):
    if are_parallel(p, q):
        continue

    r = solve(p, q)
    total += is_valid_intersection(r, p_start, q_start, pv, qv)

print(total)
