def get_rays(i, j, mat, mat_prime):
    yield mat[i][j - 1::-1] if j != 0 else []
    yield mat[i][j + 1:]
    yield mat_prime[j][i - 1::-1] if i != 0 else []
    yield mat_prime[j][i + 1:]

with open("input.txt") as file:
    trees = [list(map(int, line)) for line in file.read().splitlines()]
    trees_prime = [list(tup) for tup in zip(*trees)]

visible_trees = 0

for i, row in enumerate(trees):
    for j, target_height in enumerate(row):
        for ray in get_rays(i, j, trees, trees_prime):
            if not ray or all(height < target_height for height in ray):
                visible_trees += 1
                break

print(visible_trees)
