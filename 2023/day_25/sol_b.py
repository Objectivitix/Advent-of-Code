# Trivial networkx solution.

import networkx as nx

with open("input.txt") as file:
    apparatus: nx.Graph = nx.parse_adjlist(
        file.read().replace(":", "").splitlines(),
    )

cutset = nx.minimum_edge_cut(apparatus)
assert len(cutset) == 3

apparatus.remove_edges_from(cutset)

s, t = nx.connected_components(apparatus)

print(len(s) * len(t))
