# My first encounter with Dijkstra's algorithm.
# Two cool notes:
#
#    1. We can easily reconstruct the path by
#       keeping track of a `prev` dictionary.
#
#    2. We don't need a `visited` set. Dijks
#       guarantees that nodes are popped from
#       the PQ at most once. When a node V is
#       processed, we'll have found a shortest
#       path from source to V.

from collections import defaultdict
from queue import PriorityQueue

DELTAS_4 = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def get_neighbors(mat, mat_dimensions, target_pos):
    mat_h, mat_w = mat_dimensions
    target_y, target_x = target_pos

    for dy, dx in DELTAS_4:
        new_y = target_y + dy
        new_x = target_x + dx

        if 0 <= new_y < mat_h and 0 <= new_x < mat_w:
            yield (new_y, new_x), mat[new_y][new_x]


def alter_risk_levels(incr):
    def inner(risk_level):
        result = risk_level + incr

        if result > 9:
            result = result % 10 + 1

        return result

    return inner


def expand_mat(mat):  # modifies IN-PLACE
    for row in mat:
        original_row = row.copy()

        for i in range(1, 5):
            row.extend(map(alter_risk_levels(i), original_row))

    original_mat = mat.copy()

    for i in range(1, 5):
        mat.extend([
            [alter_risk_levels(i)(risk) for risk in row]
            for row in original_mat
        ])


with open("input.txt") as file:
    raw = [
        [int(char) for char in line]
        for line in file.read().splitlines()
    ]

expand_mat(raw)

height = len(raw)
width = len(raw[0])

adj_list = defaultdict(list)

for i, row in enumerate(raw):
    for j, _ in enumerate(row):
        curr_pos = (i, j)
        neighbors = get_neighbors(raw, (height, width), curr_pos)

        for neighbor_pos, neighbor_value in neighbors:
            adj_list[curr_pos].append((neighbor_pos, neighbor_value))

source = (0, 0)
target = (height - 1, width - 1)

dist = defaultdict(lambda: float("inf"))
pq = PriorityQueue(maxsize=0)

dist[source] = 0
pq.put((dist[source], source))

while not pq.empty():
    _, curr_node = pq.get()

    if curr_node == target:
        break

    for neighbor, weight in adj_list[curr_node]:
        alt_dist = dist[curr_node] + weight

        if alt_dist < dist[neighbor]:
            dist[neighbor] = alt_dist
            pq.put((alt_dist, neighbor))

print(dist[target])
