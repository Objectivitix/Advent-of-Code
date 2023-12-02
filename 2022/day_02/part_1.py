class Moves:
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class Results:
    WIN = 1
    TIE = 0
    LOSS = -1

MOVE_POINTS = {
    Moves.ROCK: 1,
    Moves.PAPER: 2,
    Moves.SCISSORS: 3,
}

RESULT_POINTS = {
    Results.WIN: 6,
    Results.TIE: 3,
    Results.LOSS: 0,
}

OPPONENT_MOVES = {
    "A": Moves.ROCK,
    "B": Moves.PAPER,
    "C": Moves.SCISSORS,
}

MY_MOVES = {
    "X": Moves.ROCK,
    "Y": Moves.PAPER,
    "Z": Moves.SCISSORS,
}

with open("input.txt") as file:
    input = [line.split() for line in file.read().splitlines()]

total_score = 0

for opponent, me in input:
    opponent_move, my_move = OPPONENT_MOVES[opponent], MY_MOVES[me]

    total_score += MOVE_POINTS[my_move]

    if opponent_move == my_move:
        total_score += RESULT_POINTS[Results.TIE]
    elif (
        opponent_move == Moves.ROCK and my_move == Moves.PAPER
        or opponent_move == Moves.PAPER and my_move == Moves.SCISSORS
        or opponent_move == Moves.SCISSORS and my_move == Moves.ROCK
    ):
        total_score += RESULT_POINTS[Results.WIN]
    else:
        total_score += RESULT_POINTS[Results.LOSS]

print(total_score)
