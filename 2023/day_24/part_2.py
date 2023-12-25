# "Any sufficiently advanced technology
#  is indistinguishable from magic."
#                        - Arthur C. Clarke
#
# Today I learned about constraint solvers.
# Seems pretty magical to me.

import re
from typing import NamedTuple
from z3 import Int, Solver, sat


class Stone(NamedTuple):
    x: int
    y: int
    z: int
    xv: int
    yv: int
    zv: int


with open("input.txt") as file:
    HAIL = [
        Stone(*map(int, re.findall(r"(-?\d+)", line)))
        for line in file.read().splitlines()
    ]

rock_x = Int("x")
rock_y = Int("y")
rock_z = Int("z")

rock_xv = Int("xv")
rock_yv = Int("yv")
rock_zv = Int("zv")

collision_times = [Int(f"t_{i}") for i, _ in enumerate(HAIL)]

solver = Solver()

for stone, t in zip(HAIL, collision_times):
    solver.add(
        rock_x + rock_xv * t == stone.x + stone.xv * t,
        rock_y + rock_yv * t == stone.y + stone.yv * t,
        rock_z + rock_zv * t == stone.z + stone.zv * t,
    )

assert solver.check() == sat

model = solver.model()

solved_x = model[rock_x].as_long()
solved_y = model[rock_y].as_long()
solved_z = model[rock_z].as_long()

print(solved_x + solved_y + solved_z)
