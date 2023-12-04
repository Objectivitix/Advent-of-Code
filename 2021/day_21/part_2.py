# This problem essentially asks: Out of all possible
# games, in how many does each player win? And who
# wins more?

from collections import Counter, defaultdict
from itertools import product

DICE_TOTALS = Counter(map(sum, product((1, 2, 3), repeat=3)))

# For RUNNING_STATES, the order matters so the
# DP loop traverses correctly. We want to make
# sure that once we encounter a game state, the
# number of ways to reach it is final.
#
# Notice that some game states - running or
# winning - are impossible, and so have a value
# of 0 throughout in the `dp` dict.

RUNNING_STATES = product(
    range(0, 21),   # 20 possible scores each
    range(1, 11),   # 10 possible pos each
    range(0, 21),
    range(1, 11),
    (True, False),  # is Player 1 going next
)

WINNING_STATES_1 = product(
    range(21, 31),  # Player 1's final score (win)
    range(1, 11),   # they can be anywhere
    range(0, 21),   # Player 2's final score (lose)
    range(1, 11),
    (True, False),  # anyone can be going next
)

WINNING_STATES_2 = product(
    range(0, 21),
    range(1, 11),
    range(21, 31),  # vice versa
    range(1, 11),
    (True, False),
)

with open("input.txt") as file:
    initial_pos1, initial_pos2 = (
        int(line.split(": ")[1])
        for line in file.read().splitlines()
    )

dp = defaultdict(int)

dp[0, initial_pos1, 0, initial_pos2, True] = 1

for score1, pos1, score2, pos2, next in RUNNING_STATES:
    curr = dp[score1, pos1, score2, pos2, next]

    if next:
        for dpos, freq in DICE_TOTALS.items():
            new_pos = (pos1 + dpos - 1) % 10 + 1
            dp[score1 + new_pos, new_pos, score2, pos2, False] += curr * freq

    else:
        for dpos, freq in DICE_TOTALS.items():
            new_pos = (pos2 + dpos - 1) % 10 + 1
            dp[score1, pos1, score2 + new_pos, new_pos, True] += curr * freq

print(max(
    sum(dp[game_state] for game_state in WINNING_STATES_1),
    sum(dp[game_state] for game_state in WINNING_STATES_2),
))
