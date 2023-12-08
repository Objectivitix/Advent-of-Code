import functools
from collections import Counter
from enum import IntEnum

JOKER = "J"

CARD_VALUES = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


class Tier(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0


@functools.total_ordering
class Hand:
    def __init__(self, cards):
        self.cards = cards

        self.jokers_n = cards.count(JOKER)
        self.cards_n = Counter(cards.replace(JOKER, ""))

    def __eq__(self, other):
        return self.strength == other.strength

    def __lt__(self, other):
        return self.strength < other.strength

    @property
    def strength(self):
        return (self.tier, self.order)

    @property
    def tier(self):
        if self.jokers_n == 5:
            return Tier.FIVE_OF_A_KIND

        tier_determinants = [n for _, n in self.cards_n.most_common(2)]
        tier_determinants[0] += self.jokers_n

        match tier_determinants:
            case [5]:
                return Tier.FIVE_OF_A_KIND
            case [4, *_]:
                return Tier.FOUR_OF_A_KIND
            case [3, 2]:
                return Tier.FULL_HOUSE
            case [3, 1]:
                return Tier.THREE_OF_A_KIND
            case [2, 2]:
                return Tier.TWO_PAIR
            case [2, 1]:
                return Tier.PAIR
            case _:
                return Tier.HIGH_CARD

    @property
    def order(self):
        return tuple(CARD_VALUES[card] for card in self.cards)


with open("input.txt") as file:
    inp = file.read().splitlines()

hands = []

for line in inp:
    hand_raw, bid_raw = line.split()

    hands.append((Hand(hand_raw), int(bid_raw)))

print(sum(bid * rank for rank, (_, bid) in enumerate(sorted(hands), start=1)))
