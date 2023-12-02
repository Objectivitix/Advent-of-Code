import operator
import re
from ast import literal_eval
from collections import deque

STARTING_ITEMS_REGEX = r"Starting items: ((\d+, )+(\d+)|(\d+))"
OPERATION_REGEX = r"Operation: new = old ([+*]) ((\d+)|old)"
DIVIS_NUM_REGEX = r"Test: divisible by (\d+)"
TRUE_MONKEY_REGEX = r"If true: throw to monkey (\d+)"
FALSE_MONKEY_REGEX = r"If false: throw to monkey (\d+)"

OPERATORS = {
    "+": operator.add,
    "*": operator.mul,
}

ROUNDS_N = 20

class Monkey:
    def __init__(
        self, starting_items, operation,
        divis_num, true_monkey, false_monkey
    ):
        self.inspections_n = 0
        self.items = deque(starting_items)
        self.operation = operation

        self.predicate = lambda x: x % divis_num == 0
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

    def inspect(self):
        self.inspections_n += 1
        return self.operation(self.items.popleft())

    def get_recipient_monkey_index(self, worry_level):
        return (
            self.true_monkey
            if self.predicate(worry_level)
            else self.false_monkey
        )

def create_operation(operator, operand):
    # factory function forces early binding
    return (
        lambda x:
        OPERATORS[operator]
        (x, x if operand == "old" else int(operand))
    )

def turn(monkey, monkeys):
    while monkey.items:
        worry_level = monkey.inspect()
        worry_level //= 3

        index = monkey.get_recipient_monkey_index(worry_level)
        monkeys[index].items.append(worry_level)

def round(monkeys):
    for monkey in monkeys:
        turn(monkey, monkeys)

    return monkeys

with open("input.txt") as file:
    raw = file.read().split("\n\n")

monkeys = []

for i, monkey_properties in enumerate(raw):
    starting_items_match = re.search(STARTING_ITEMS_REGEX, monkey_properties)
    operation_match = re.search(OPERATION_REGEX, monkey_properties)
    divis_num_match = re.search(DIVIS_NUM_REGEX, monkey_properties)
    true_monkey_match = re.search(TRUE_MONKEY_REGEX, monkey_properties)
    false_monkey_match = re.search(FALSE_MONKEY_REGEX, monkey_properties)

    starting_items_string = f"[{starting_items_match.group(1)}]"
    starting_items = literal_eval(starting_items_string)

    operator, operand, *_ = operation_match.groups()
    operation = create_operation(operator, operand)

    divis_num = int(divis_num_match.group(1))
    true_monkey = int(true_monkey_match.group(1))
    false_monkey = int(false_monkey_match.group(1))

    monkey = Monkey(starting_items, operation, divis_num, true_monkey, false_monkey)
    monkeys.append(monkey)

for _ in range(ROUNDS_N):
    monkeys = round(monkeys)

monkey_inspections = [monkey.inspections_n for monkey in monkeys]
monkey_inspections_sorted = sorted(monkey_inspections, reverse=True)

print(monkey_inspections_sorted[0] * monkey_inspections_sorted[1])
