import re

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def is_overlap(itv1, itv2):
        return (
            itv1.start <= itv2.end
            and itv2.start <= itv1.end
        )

with open("input.txt") as file:
    raw = file.read().splitlines()

    input = []
    for line in raw:
        s1, e1, s2, e2 = map(int, re.findall(r"\d+", line))
        input.append((Interval(s1, e1), Interval(s2, e2)))

print(sum(Interval.is_overlap(itv1, itv2) for itv1, itv2 in input))
