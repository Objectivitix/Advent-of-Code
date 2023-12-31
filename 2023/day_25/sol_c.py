# Karger's with a disjoint-set structure. Kind
# of like Kruskal's algorithm.
#
# A lot faster than Solution A, but still can't
# run |V| choose 2 trials.

import random


class UnionFind:
    def __init__(self, iterable=None):
        self.link = {}
        self.size = {}

        if iterable:
            for item in iterable:
                self.make(item)

    def make(self, item):
        self.link[item] = item
        self.size[item] = 1

    def find(self, item):
        root = item

        while self.link[root] != root:
            root = self.link[root]

        while self.link[item] != root:
            item, self.link[item] = self.link[item], root

        return root

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        assert root_a != root_b

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.link[root_b] = root_a
        self.size[root_a] += self.size[root_b]


class Graph:
    def __init__(self):
        self.edge_list = []

    def add_edge(self, u, v):
        self.edge_list.append((u, v))

    def sample_karger_cut(self):
        nodes = {node for edge in self.edge_list for node in edge}
        edges = random.sample(self.edge_list, len(self.edge_list))

        components = UnionFind(nodes)
        components_n = len(nodes)

        while components_n > 2:
            u, v = edges.pop()

            if components.find(u) != components.find(v):
                components.union(u, v)
                components_n -= 1

        s_size = components.size[components.find(next(iter(nodes)))]
        t_size = len(nodes) - s_size

        cut_size = sum(
            components.find(u) != components.find(v)
            for u, v in self.edge_list
        )

        return s_size, t_size, cut_size


def parse_raw(file):
    apparatus = Graph()

    for line in file.read().splitlines():
        component, neighbors = line.split(": ")

        for neighbor in neighbors.split(" "):
            apparatus.add_edge(component, neighbor)

    return apparatus


with open("input.txt") as file:
    APPARATUS = parse_raw(file)

while True:
    s_size, t_size, cut_size = APPARATUS.sample_karger_cut()

    if cut_size == 3:
        break

print(s_size * t_size)
