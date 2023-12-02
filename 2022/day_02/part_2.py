class Move:
    def __init__(self, *, beats, loses_to):
        self._beats = beats
        self._loses_to = loses_to

    @property
    def beats(self):
        return getattr(Moves, self._beats.upper())

    @property
    def loses_to(self):
        return getattr(Moves, self._loses_to.upper())

class Moves:
    ROCK = Move(beats="scissors", loses_to="paper")
    PAPER = Move(beats="rock", loses_to="scissors")
    SCISSORS = Move(beats="paper", loses_to="rock")

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

ROUND_RESULTS = {
    "X": Results.LOSS,
    "Y": Results.TIE,
    "Z": Results.WIN,
}

with open("input.txt") as file:
    input = [line.split() for line in file.read().splitlines()]

total_score = 0

for opponent, result in input:
    opponent_move = OPPONENT_MOVES[opponent]
    result_needed = ROUND_RESULTS[result]

    my_move = None

    if result_needed == Results.TIE:
        my_move = opponent_move
    elif result_needed == Results.WIN:
        my_move = opponent_move.loses_to
    else:
        my_move = opponent_move.beats

    total_score += MOVE_POINTS[my_move] + RESULT_POINTS[result_needed]

print(total_score)
