# Solution uses a directed, unweighted graph.

from collections import deque

START_INDICATOR = "S"
END_INDICATOR = "E"

START_ELEVATION = 1
END_ELEVATION = 26
MAX_ELEVATION_GAP = 1

LOWERCASE_OFFSET = 96

class Node:
    def __init__(self, pos):
        self.pos = pos
        self.neighbors = []

        self.dist = float("inf")
        self.prev = None

class Graph:
    def __init__(self):
        self.nodes = {}

    def reset_nodes(self):
        for node in self.nodes.values():
            node.dist = float("inf")
            node.prev = None

    def get_shortest_path(self, start_node, end_node):
        self.reset_nodes()
        start_node.dist = 0

        node_queue = deque([start_node])

        while node_queue:
            working_node = node_queue.popleft()
            if working_node is end_node:
                return working_node.dist

            for neighbor in working_node.neighbors:
                if neighbor.dist == float("inf"):
                    neighbor.dist = working_node.dist + 1
                    neighbor.prev = working_node
                    node_queue.append(neighbor)

        return -1

def get_adjacents(i, j, width, height):
    if i:
        yield (i - 1, j)
    if i < height:
        yield (i + 1, j)
    if j:
        yield (i, j - 1)
    if j < width:
        yield (i, j + 1)

with open("input.txt") as file:
    raw = file.read().splitlines()

# PART 1: parse input
heightmap = []

start_pos = None
end_pos = None

for i, line in enumerate(raw):
    row = []

    for j, char in enumerate(line):
        if char == START_INDICATOR:
            start_pos = (i, j)
            row.append(START_ELEVATION)
        elif char == END_INDICATOR:
            end_pos = (i, j)
            row.append(END_ELEVATION)
        else:
            row.append(ord(char) - LOWERCASE_OFFSET)

    heightmap.append(row)

width = len(heightmap[0]) - 1
height = len(heightmap) - 1

# PART 2: create graph
graph = Graph()

for i, line in enumerate(heightmap):
    for j, _ in enumerate(line):
        graph.nodes[(i, j)] = Node((i, j))

for i, line in enumerate(heightmap):
    for j, elevation in enumerate(line):
        for adj_i, adj_j in get_adjacents(i, j, width, height):
            adj_elevation = heightmap[adj_i][adj_j]

            if adj_elevation - elevation <= MAX_ELEVATION_GAP:
                neighbor = graph.nodes[(adj_i, adj_j)]
                graph.nodes[(i, j)].neighbors.append(neighbor)

# PART 3: traverse graph
start_node = graph.nodes[start_pos]
end_node = graph.nodes[end_pos]

print(graph.get_shortest_path(start_node, end_node))
