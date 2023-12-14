def yield_diagonals(rows, cols):

    for i in range(cols - 1, -1, -1):
        diagonal = []
        r, c = 0, i
        while r < rows and c < cols:
            diagonal.append((r, c))
            r += 1
            c += 1
        yield diagonal

    for i in range(1, rows):
        diagonal = []
        r, c = i, 0
        while r < rows and c < cols:
            diagonal.append((r, c))
            r += 1
            c += 1
        yield diagonal

print(list(yield_diagonals(5, 5)))