#!/usr/bin/env python3

from copy import deepcopy
from typing import List


# HELPER FUNCTIONS
def parser(text) -> list:
    return [[int(card) for card in deck.split("\n") if card.isdigit()] for deck in text.strip().split("\n\n")]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
def _calc_deck(winner):
    return sum(card * multiplier for card, multiplier in zip(winner, range(len(winner), 0, -1)))


def part1(players: List[list]) -> int:
    assert len(players) == 2

    deck1, deck2 = deepcopy(players)
    while len(deck1) > 0 and len(deck2) > 0:
        # playing round
        x, y = deck1.pop(0), deck2.pop(0)
        if x > y:
            deck1.extend([x, y])
        else:
            deck2.extend([y, x])
    return _calc_deck(deck1 or deck2)


def _log(deck1, deck2):
    print("""
Player 1's deck: %s
Player 2's deck: %s
Player 1 plays: %s
Player 2 plays: %s
    """ % (deck1, deck2, deck1[0], deck2[0]))


def _play(deck1, deck2) -> bool:
    prev_rounds = set()
    while len(deck1) > 0 and len(deck2) > 0:
        # _log(deck1, deck2)
        # _hash = (deck1[0], deck1[-1], len(deck1), deck2[0], deck2[-1], len(deck2),)
        # _hash = (deck1[0], len(deck1), deck2[0], len(deck2),) # returns incorrect result for part 2
        _hash = (deck1[0], deck1[-1], deck2[0], deck2[-1])
        if _hash in prev_rounds:
            # Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order
            # in the same players' decks, the game instantly ends in a win for player 1. Previous rounds from other games are not considered.
            # (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea).
            return True
        prev_rounds.add(_hash)

        # playing round
        x, y = deck1.pop(0), deck2.pop(0)
        res = x > y
        if len(deck1) >= x and len(deck2) >= y:
            # If both players have at least as many cards remaining in their deck as the value of the card they just drew,
            # the winner of the round is determined by playing a new game of Recursive Combat.
            res = _play(deck1.copy()[:x], deck2.copy()[:y])
        if res:
            deck1.extend([x, y])
        else:
            deck2.extend([y, x])

    return bool(deck1)


def part2(players: List[list]) -> int:
    assert len(players) == 2

    deck1, deck2 = deepcopy(players)
    res = _play(deck1, deck2)
    return _calc_deck(deck1 if res else deck2)


# TEST
def test() -> bool:
    given = parser("""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""")
    assert given == [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]
    assert part1(given) == 306
    assert part2(given) == 291
    given = parser("""
Player 1:
43
19

Player 2:
2
29
14
""")
    # test recursive decks
    assert part2(given) == 105
    return True


if __name__ == '__main__':
    assert test()

    input = parser(read_input())
    # ONE #1
    part_1 = part1(input)
    print(part_1)
    assert part_1 == 32401
    # TWO #2
    part_2 = part2(input)
    print(part_2)
    assert part_2 == 31436

# INPUT
"""🎅
Player 1:
40
26
44
14
3
17
36
43
47
38
39
41
23
28
49
27
18
2
13
32
29
11
25
24
35

Player 2:
19
15
48
37
6
34
8
50
22
46
20
21
10
1
33
30
4
5
7
31
12
9
45
42
16
⛄"""
