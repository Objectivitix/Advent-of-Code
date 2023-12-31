from collections import defaultdict
from queue import PriorityQueue
from typing import NamedTuple


# Subclassing to add a comparison throwaway,
# enabling membership in a PriorityQueue.
class P(complex):
    def __lt__(self, _):
        return True


class State(NamedTuple):
    node: P
    dir: P
    streak: int


DELTAS_4 = [P(-1, 0), P(0, 1), P(1, 0), P(0, -1)]


def get_adj(pos, height, width):
    for delta in DELTAS_4:
        adj_pos = pos + delta

        adj_i = int(adj_pos.real)
        adj_j = int(adj_pos.imag)

        if 0 <= adj_i < height and 0 <= adj_j < width:
            yield adj_i, adj_j, delta


def parse_raw(file):
    raw = file.read().splitlines()
    dims = len(raw), len(raw[0])

    yield dims

    adj_list = defaultdict(list)

    for i, row in enumerate(raw):
        for j, _ in enumerate(row):
            curr = P(i, j)

            for adj_i, adj_j, dir in get_adj(curr, *dims):
                adj_pos = P(adj_i, adj_j)
                adj_val = int(raw[adj_i][adj_j])

                adj_list[curr].append((adj_pos, adj_val, dir))

    yield adj_list


with open("input.txt") as file:
    (HEIGHT, WIDTH), ADJ_LIST = parse_raw(file)

SOURCE = P(0, 0)
TARGET = P(HEIGHT - 1, WIDTH - 1)

# Even with these restrictions, Dijkstra's algorithm
# still guarantees that every state popped from the
# PQ has its distance finalized. Thus it is correct. 
dist = defaultdict(lambda: float("inf"))
pq = PriorityQueue()

start_state = State(SOURCE, 0, 0)

dist[start_state] = 0
pq.put((0, start_state))

while not pq.empty():
    _, curr = pq.get()

    if curr.node == TARGET:
        break

    for neighbor, weight, new_dir in ADJ_LIST[curr.node]:
        # Disallow reversing direction, which can lead to
        # shorter paths unsuitable to the problem statement.
        if new_dir == curr.dir * -1:
            continue

        if curr.streak < 4 and curr.dir and new_dir != curr.dir:
            continue

        new_streak = curr.streak + 1 if new_dir == curr.dir else 1

        if neighbor == TARGET and new_streak < 4:
            continue

        if new_streak > 10:
            continue

        new = State(neighbor, new_dir, new_streak)

        alt_dist = dist[curr] + weight

        if alt_dist < dist[new]:
            dist[new] = alt_dist
            pq.put((alt_dist, new))

print(dist[curr])
