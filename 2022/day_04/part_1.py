import re

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __le__(self, other):
        return (
            self.start >= other.start
            and self.end <= other.end
        )

with open("input.txt") as file:
    raw = file.read().splitlines()

    input = []
    for line in raw:
        s1, e1, s2, e2 = map(int, re.findall(r"\d+", line))
        input.append((Interval(s1, e1), Interval(s2, e2)))

print(sum(itv1 <= itv2 or itv2 <= itv1 for itv1, itv2 in input))
