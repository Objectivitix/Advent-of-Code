import math

def get_rays(i, j, mat, mat_prime):
    yield mat[i][j - 1::-1] if j != 0 else []
    yield mat[i][j + 1:]
    yield mat_prime[j][i - 1::-1] if i != 0 else []
    yield mat_prime[j][i + 1:]

def get_viewing_dist(target_height, ray):
    viewing_dist = 0
    for height in ray:
        viewing_dist += 1
        if height >= target_height:
            break

    return viewing_dist

with open("input.txt") as file:
    trees = [list(map(int, line)) for line in file.read().splitlines()]
    trees_prime = [list(tup) for tup in zip(*trees)]

highest_scenic_score = float("-inf")

for i, row in enumerate(trees):
    for j, target_height in enumerate(row):
        curr_scenic_score = math.prod(
            get_viewing_dist(target_height, ray)
            for ray in get_rays(i, j, trees, trees_prime)
        )

        if curr_scenic_score > highest_scenic_score:
            highest_scenic_score = curr_scenic_score

print(highest_scenic_score)
