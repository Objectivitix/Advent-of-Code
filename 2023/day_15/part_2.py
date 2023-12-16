# In Python >=3.7, dicts are guaranteed insertion order.
# But CCC habits die hard :P
# (And I can argue OrderedDict is more explicit lol)

import re
from collections import OrderedDict

def hash_(string):
    num = 0

    for char in string:
        num += ord(char)
        num *= 17
        num %= 256

    return num

with open("input.txt") as file:
    SEQUENCE = re.findall(r"([a-z]+)(=\d|-)", file.read())

boxes = [OrderedDict() for _ in range(256)]

for label, operation in SEQUENCE:
    index = hash_(label)

    if operation == "-":
        if label in boxes[index]:
            del boxes[index][label]
        continue

    boxes[index][label] = int(operation[1])

print(sum(
    box_num * slot_num * focal_length
    for box_num, box in enumerate(boxes, 1)
    for slot_num, focal_length in enumerate(box.values(), 1)
))
