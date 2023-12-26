# Karger's algorithm, a randomized algo for finding
# the global minimum cut in an undirected, unweighted
# graph. With |V| choose 2 trials, the probability
# of NOT finding the min cut is about 1 over |V|.
#
# I'm not sure if I implemented the algo right,
# because my solution is WAY too slow to run even |V|
# trials, let alone |V| choose 2 trials. So since we
# know the min cut size is 3 ... I "bogosort" it :P
#
# This is my initial solution. See sol_b and sol_c.

import random
from collections import defaultdict
from copy import deepcopy


class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def _contract_edge(self, u, v):
        u_adjs = self.cut[u]
        v_adjs = self.cut[v]

        del self.cut[u]
        del self.cut[v]

        proto = []

        for node in (u, v):
            if isinstance(node, frozenset):
                proto.extend(node)
            else:
                proto.append(node)

        supernode = frozenset(proto)

        self.cut[supernode] = [
            neighbor
            for neighbor in [*u_adjs, *v_adjs]
            if neighbor not in (u, v)
        ]

        for neighbor in self.cut[supernode]:
            self.cut[neighbor] = [
                supernode if node in (u, v) else node
                for node in self.cut[neighbor]
            ]

    def sample_karger_cut(self):
        self.cut = deepcopy(self.adj_list)

        while len(self.cut) > 2:
            u = random.choice(list(self.cut))
            v = random.choice(self.cut[u])

            self._contract_edge(u, v)

        s, t = self.cut

        return s, t, len(self.cut[s])


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
    s, t, size = APPARATUS.sample_karger_cut()

    if size == 3:
        break

print(len(s) * len(t))
