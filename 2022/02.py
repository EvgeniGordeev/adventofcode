#!/usr/bin/env python3
from collections import namedtuple
from typing import List


def parser(text) -> list:
    return [line.strip().split(' ') for line in text.strip().split('\n')]


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN FUNCTIONS
Shape = namedtuple('Shape', 'label score')

Rock = Shape('Rock', 1)
Paper = Shape('Paper', 2)
Scissors = Shape('Scissors', 3)

aka = {
    'A': Rock,
    'X': Rock,
    'Rock': Rock,
    'B': Paper,
    'Y': Paper,
    'Paper': Paper,
    'C': Scissors,
    'Z': Scissors,
    'Scissors': Scissors,
}

win_rules = {
    'Rock': 'Scissors',
    'Paper': 'Rock',
    'Scissors': 'Paper',
}


def part1(given: List[str]) -> int:
    def play(sh1: Shape, sh2: Shape) -> int:
        if win_rules[sh2.label] == sh1.label:  # win
            outcome = 6
        elif sh2.score == sh1.score:  # draw
            outcome = 3
        elif win_rules[sh1.label] == sh2.label:  # loss
            outcome = 0
        else:
            raise ValueError
        return outcome + sh2.score

    count = 0
    for opponent, me in given:
        count += play(aka[opponent], aka[me])

    return count


def part2(given: List[str]) -> int:
    loss_rules = {v: k for k, v in win_rules.items()}

    def play_reverse(sh1: Shape, outcome: str) -> int:
        if outcome == 'X':  # loss
            return aka[win_rules[sh1.label]].score
        elif outcome == 'Y':  # draw
            return 3 + sh1.score
        elif outcome == 'Z':  # win
            return 6 + aka[loss_rules[sh1.label]].score
        else:
            raise ValueError

    count = 0
    for opponent, me in given:
        count += play_reverse(aka[opponent], me)

    return count


# TEST
def test():
    # GIVEN
    given = parser("""
A Y
B X
C Z
    """)
    assert part1(given) == 15
    # part 2
    assert part2(given) == 12

    return True


if __name__ == '__main__':
    assert test()
    given = parser(read_input())
    # ONE #1
    part_1 = part1(given)
    print(part_1)
    assert part_1 == 9651
    # # TWO #2
    part_2 = part2(given)
    print(part_2)
    assert part_2 == 10560

# INPUT
"""🎅
A Y
B X
B X
C Y
B X
A Z
B X
B X
C Z
A Z
C Z
A X
A Y
A Y
B X
C Y
B Z
A X
B X
C Y
C Y
A Y
A Y
C Y
B X
B X
B X
A X
B X
B X
C Y
C Y
B X
A Z
A Z
B X
A Z
C Y
B X
B X
B X
B X
B X
B Z
A Z
B X
A Z
A X
B X
A Z
B X
C Y
A Z
A Z
B X
B X
B Z
C Y
A Y
B Z
A Z
C Z
B X
C Y
C Y
B Z
B X
B X
B Z
B X
B X
A Y
A Z
B Z
B X
B Y
B Z
B X
C X
B Z
B X
A Z
B Z
B Z
B X
A Y
A Z
A Y
B X
B Z
B X
B X
A Y
A Y
B X
B X
B X
C X
C Y
B X
B X
B Z
B X
B X
B X
C Y
B X
C Y
A Z
B X
B Z
B X
C Y
C Y
A Z
A Y
C Y
B X
B X
B Z
A Y
B X
B X
B X
A Y
B Z
B X
A Y
B Z
C Y
A X
B X
B X
A Z
C Y
B X
B Z
A Y
A Y
C Y
A Y
C Y
B X
B Z
B X
C Y
A Y
B X
C Z
A Z
C Y
B X
B Z
B X
B X
B Z
B Y
A Y
B X
A Y
A Z
A Z
B X
C Y
B Z
A X
A Y
B X
A Z
B X
A Y
B Y
B X
A Y
B X
B X
B X
B X
B X
B X
B X
A Z
B X
B X
B Z
B Z
B Z
B Z
A Y
B Z
C Z
B X
B X
B X
A Z
B Z
C Y
B X
C Y
B Z
B X
B Z
B X
C Z
A Z
A Y
A X
B X
B Z
A Y
B X
B X
B X
B X
C Y
C Y
A Z
A Y
A X
B X
B X
A Y
B X
C Y
A X
B X
B X
B X
A Z
C Y
B Z
C Y
A Y
C Y
A X
A Z
C Z
A Z
B X
B Z
B X
B X
A X
B X
B X
B Z
A Y
C Y
A Z
C Z
A Z
A Z
A Z
B Z
B Z
B Z
C Z
B Y
C Y
C Y
C X
B X
C Y
B X
B X
C Y
B Z
B X
C Z
B X
A Z
B Z
C X
C Y
B X
A Y
A Z
B X
A Z
A Z
B X
B X
C Z
B Z
A Z
A Z
C Z
B X
A Z
A X
B X
B X
C Y
B X
B Z
A Z
B X
B X
B X
B X
B X
B X
B X
B X
C Y
C Y
B X
B X
B X
C Y
A X
B Z
B X
B X
C Z
B X
B Z
B Z
A Z
B X
B Z
B X
A Z
B X
B X
B X
B X
B X
C Z
B X
B X
B X
B Z
C Y
C Y
A Y
B X
B Z
C Y
B X
B X
C Y
C Y
B X
B X
B X
B X
C X
B Z
B X
B Z
C Y
A X
A Z
B X
B X
A Z
B X
C Z
B X
A Y
A Z
B X
B X
B X
B Z
B X
A Y
C Y
B Z
B Z
C Y
B X
A Y
C Y
B X
C Z
B X
B X
A Z
B Z
B Z
B X
A Z
A Z
A Y
B Z
B X
B X
B X
B X
B Z
B X
B Z
B X
A Z
B X
B X
C Z
C Z
B X
C Y
A Z
B X
B Z
C Z
C X
B X
A Y
A Y
B X
B X
C Y
A X
C Y
A Y
A Z
C Z
B Z
A Z
B X
B X
B Z
C Y
A Y
A Y
B Z
A Z
A Z
B Z
A Z
B X
A Y
A Y
C Y
B X
B X
A X
B X
C X
A Y
A Z
B X
B X
B X
B X
B X
B Z
B Z
B Z
B X
B X
A Z
B X
C Z
A Z
C Y
B Z
C Y
A Y
C Y
B X
B X
B X
A Y
B Z
B Z
B X
B Z
B X
B X
B X
C Y
B X
B Z
A Z
B X
B X
B X
C Z
C Z
B Z
B X
A Z
A X
B X
B X
B Y
A Y
B X
B X
C Z
A Z
B X
B Z
B Z
A Y
A Z
B Z
B Z
A Y
A Y
A Z
C Y
C Y
B X
B X
A Z
B X
C Y
C X
A Z
B X
B X
B X
A Y
C Y
B Y
C Y
C X
A X
A Y
B Z
B X
B Z
A X
B X
C Z
B X
B X
A Y
B Z
B X
A Y
A Y
B X
C Y
B X
B X
C Y
B X
C Z
B Z
B X
A X
C Y
C Y
B X
B Z
B X
B X
A Z
B X
A Z
B Z
B X
B X
B Z
A Y
C Y
B Z
B X
A Y
B X
A X
C Z
B X
B Z
B Z
A X
C Y
A Z
B X
B Z
A Y
B X
C Y
A Y
B Z
C Y
B X
B X
B X
B X
B X
B X
C Y
B X
C Z
A Y
C Y
B X
C Y
B Z
B X
A X
B Z
B X
C X
B X
A Z
B X
A Y
B X
C Z
B X
B Z
A Y
B X
A Z
A Z
A Z
A Y
A Y
B X
A Z
B X
B X
A Y
A Y
A Y
B Z
C Y
B Z
B X
C Z
A Y
C Y
B X
B X
B Z
B X
B X
B X
C Y
C Y
A Y
B Z
B Z
B X
B X
B Z
B X
A Y
C Y
B X
C X
B Z
B X
B Z
B Z
C Y
B Z
B X
C X
B X
C Y
B X
A Z
B X
B X
B X
B X
B X
C Y
A Y
B X
C Y
B Z
B Z
B X
C X
B Z
C Y
C X
C Y
A Z
B Z
C Y
C X
B X
A Y
C Y
B X
C Z
B Z
A Y
C Z
C X
B X
B X
A Y
C X
B X
B X
A X
A Z
A X
A Y
A Y
C Y
B X
C Z
B X
C Y
A Y
B X
B X
B X
B X
A Z
C X
B X
B Z
B X
B X
C Y
B X
C Z
B X
B X
B X
B X
B X
C Y
B X
B X
A Y
B X
C Y
C Y
A Y
B X
A X
A Y
B X
B Z
B X
B Z
A X
A Y
A X
B X
C Z
A Y
B Z
A Y
B Z
B Z
B X
B Z
B X
B X
B X
B Z
B X
B X
B X
A Z
C Z
C Z
A X
A X
B X
B X
A X
B X
A X
A Z
B Z
B X
C Y
B X
C Y
A Y
C X
A X
A Y
B Z
B X
B X
C Z
B Y
A Y
B Y
C Y
A Y
B X
B X
C X
B Z
A Y
B Z
A Z
B X
B X
A Z
C Z
A Y
B X
B X
B Z
B X
B X
B Z
A X
A Z
C Y
A Y
A Z
B X
C Y
B Z
C Y
B X
B X
B Z
B X
A Y
B X
A Y
B X
A Y
B X
A Y
C Y
A Y
B Z
A Y
B X
A Z
C Y
B X
B X
B X
A X
B X
B Z
A Z
A Z
B X
B Z
B X
A Y
B Z
B X
B X
A Y
A Y
C Z
C Y
B X
A X
A Y
A X
C Y
B X
C X
B X
B X
A Y
A Y
A Y
B Y
B X
B X
B X
C Z
B Z
C Z
A X
B X
B X
A Y
A Z
B X
A Y
B Z
B Z
C Y
B X
B X
C X
B X
C X
B X
B Z
A X
B X
A Z
A X
B Z
A Y
B X
B X
B X
B X
B Z
A Z
B X
B Z
B X
B Z
C Y
B X
C Y
B X
B X
B X
A Y
B X
A Y
B X
B X
A X
C Z
C Y
A Z
B X
A Y
C Z
C Y
C Y
B Z
A Y
B X
A Y
B X
B X
B Z
B Z
B X
C X
B Z
A X
A Y
A Y
B Z
A Z
C Y
B X
B Z
A Y
C Y
A Y
A X
A Z
B X
B X
C Y
B X
C Y
B X
A X
B Z
C X
B Y
A Y
C Y
B X
A X
B X
B X
B X
A Z
A Y
B X
C Z
B X
C X
C Z
B X
B X
C Y
B X
B Z
A Y
A Y
B X
B X
B Z
C Y
B X
B X
B X
A Y
C Y
B X
A Y
A Z
C Y
B X
A Y
A Z
B Z
A Z
B X
C X
B Z
A Y
B Z
A Y
C Y
A X
A Y
B X
C Y
C Y
B X
A X
B Z
B X
B X
A Z
A Z
A Y
A Y
B X
B X
B X
A X
B X
B X
B X
A X
B Z
C Z
A Y
C Y
C Y
C X
B X
B Z
B Z
B X
B X
C Y
A X
C Y
A X
B X
B X
B Z
B Z
C Y
C Y
A Z
C Y
A Z
B X
A Z
A Y
B Z
B Z
B X
B X
A Y
B Z
B X
C Z
A Z
B Z
B X
B Z
B X
C Y
B X
A Y
B Z
C Y
B Z
C Z
B X
C Z
B X
B X
B X
C Y
B X
B X
B Z
A Y
B X
B Z
A Z
B X
C Y
C X
C Y
A Z
B X
A Z
B X
C Z
A Y
B Z
B Z
A Y
C Z
C X
A Y
B X
B Z
B X
B X
B X
B X
A X
B X
B X
A Z
B X
B X
A Z
C Y
A X
B Z
B X
B X
A Z
B X
A Y
B Z
C Y
B X
A Y
C Y
B Z
B X
A Z
A Z
B X
B X
B Z
B X
B X
A Z
B X
B Z
B Z
C Y
A Z
B X
A Y
B X
B X
B X
B Z
A X
C Y
B Z
B X
B X
B X
B X
B X
B Z
B X
B Z
A Z
B Z
B X
C Z
B Z
C Z
A Z
C X
A Y
B Z
B Z
B X
B Z
B Z
A Z
C Z
A X
C Y
C Y
A Y
A X
A Z
B X
A Y
B X
B X
C Y
C Y
B X
B Z
A Y
B X
B Z
B X
B X
A Z
C Y
B X
C Y
A Y
B Z
A Z
A Y
B X
A Z
B Z
B X
A Y
A Y
A Z
A X
B Z
C Z
B X
C Z
B X
B Z
A X
B X
B X
B X
B X
C Y
B X
A X
B Z
A Y
B X
A Z
B X
B Z
A Y
A Y
A Y
A Y
A Z
C Y
C Z
B X
B Z
A Y
B X
B X
B X
A Y
B Z
B X
B Z
B X
B X
B X
C Y
C Y
C X
B X
A Y
A Y
C Z
A Y
A Y
C X
A Z
B X
B X
B X
B X
C Y
A Y
B Z
A Z
B X
C X
A Z
B X
C Y
B X
B X
C Y
B X
B X
B X
A Y
B X
B X
C Z
B X
C Y
C Y
B X
A Z
B X
B X
C Y
A Y
B X
B Z
B X
B X
B X
C Y
C Z
B Z
C Y
B X
B Z
B X
B X
B X
C Y
C X
B X
A Y
A Z
B Z
A Y
B X
B X
B Y
C Y
C X
B Z
A Z
B X
B X
A Y
C Z
C Y
B X
C Y
A Z
A Y
B Z
B X
B X
B X
B X
A Z
A X
A X
A X
C Y
B Z
B X
C Y
B X
B X
A Z
C Z
C Z
B X
A Y
B X
B Z
B X
A Y
A Y
A Z
C Y
A Y
A Z
A Y
A Y
B X
A Y
B X
A Z
A Z
C Y
B X
B X
C Y
B X
B X
B X
C Y
A Y
B X
A Y
B Z
C Y
B X
A Y
B Z
A Z
B Z
A Z
B X
C Y
B X
B X
B X
C Y
A Y
B X
A Y
C X
A Z
B X
B Y
B X
B X
A Z
B X
B X
B Z
B X
C Y
B X
B X
B Z
B X
C Y
B X
C Y
B X
B Z
A Y
B X
B X
C Z
B X
C Y
A Y
C Y
B X
B Z
B X
B X
B X
B X
A Y
B X
A Z
A Y
A X
C Y
B X
C Y
B X
A Z
C Y
C Y
B Z
B X
A Y
B Z
A Y
A Y
B Z
B Z
B X
C Y
C Y
B X
A X
A Z
B X
C Y
B X
B X
B Z
B X
B Z
C Y
C Z
C Y
A Y
A Z
B X
C Y
A Y
C X
B X
B X
A Y
B X
B X
B X
B Z
B Y
A X
A Y
C Y
C Y
A Y
C Y
B Z
B Z
C Y
B X
C Y
C Z
A Y
C X
A Y
A Y
C Y
C Y
B X
A Y
A X
B X
B X
B Z
B X
A Z
A Y
A Y
B X
B X
B Z
B Z
B X
B Z
A Z
A Y
A Z
B X
C Y
B Z
B X
A Y
B X
C X
B X
B X
C Y
B X
B X
B X
A Y
A X
A Y
B X
B X
A Y
A Y
A Z
A Z
C X
C Y
A Z
C Y
B Z
B X
A Y
B X
B Z
C Z
A Y
A Z
A Y
B X
B Z
B X
A X
B Z
B X
C Y
B X
A Z
C Z
A X
B X
B X
A Y
C Y
B X
B X
B X
B X
B X
A X
B X
A Z
C Z
B Z
B X
C X
A X
C Y
A Y
A Z
B X
A X
A Z
A Z
B X
B X
A Z
C Y
A Z
B X
C Y
B X
C Z
C Y
C X
A Z
C X
B Z
B X
B X
C Y
B X
C Y
A Z
A Z
A Z
A Y
A Z
B X
B X
B X
B Z
C Y
C Z
C Y
C Y
C Y
A Y
B Z
A X
B X
B X
B X
A X
A Y
B X
B Z
A Z
A Y
A Y
B Z
B X
B X
C Y
C Y
C Y
B X
C Y
B X
B X
B X
C Y
A Y
A Y
C Z
C Y
B X
A X
A Y
B X
C Y
B X
A Y
C Y
A Y
B X
B X
B Z
A Y
B Z
B Z
B X
B X
C X
C Y
B X
B X
A X
C Y
B X
B Z
B X
B X
A Y
B X
B Z
B Z
C Y
B X
B Z
B Z
B Z
B X
B X
A Y
B X
B X
B Z
C Y
A Y
B X
B Z
B X
B X
A X
B X
B X
B X
B Z
B Z
B Z
B X
A Z
B X
A Z
A Y
B Z
B X
A Y
B X
B Z
B X
A Z
B X
B Z
C Z
A X
B X
B X
B X
C Y
B X
B X
A Y
A Z
B X
C Y
B X
C Y
B X
B Y
B X
C Z
B X
C Z
A Y
B X
C Z
B X
A Y
C Y
B X
B X
B Z
C X
B Z
B X
A Z
B X
B X
B X
B Z
B X
A Z
C Y
A Y
B X
B X
A Z
B X
A Y
B X
C Y
B Z
B Z
B X
B Z
B X
B X
B X
B X
B X
C Y
A Z
A Z
B Z
A Y
B Z
C Y
A Y
A Y
C Y
A Y
B Z
A Y
A Y
B X
B X
A X
B X
C Y
C Y
B Z
B X
A Z
B Z
B X
A Z
B Z
A Y
A Y
A Y
A Y
A Z
A Y
B X
B Z
A Y
B X
A Z
B Z
C X
B X
B X
B Z
B Z
B X
B X
B X
B X
B X
B X
B X
B Z
B X
B X
B X
B X
B X
B Z
B X
B X
B Z
B Z
B X
A Y
B Z
B X
A Z
A Y
A Z
B X
B X
A X
B Y
A Z
B X
C Z
A Z
B X
B Z
B X
B X
B X
A Y
C Y
B X
B X
B X
A Y
B X
A Z
B X
B X
B X
B Z
B Z
C X
C Y
B X
B X
C Y
B X
B X
B X
A X
A Z
A Z
B Z
B Z
B X
A Y
B X
C Y
B Z
C Y
C Z
A Y
A Y
B X
B X
A Z
B X
B X
B Z
B X
B X
A Z
B X
B X
B X
C Y
B X
B X
C Y
B X
B X
B Z
B X
B X
A Y
C Y
A X
C Y
B X
B X
A Z
A Y
B X
A X
B Z
A Y
B X
B X
A Y
B X
C X
B X
B X
B Z
B Z
B X
B Z
B X
B X
A Y
A Y
B X
B Z
C Y
B X
B X
B X
A Z
B X
A Y
B X
C Y
A X
A Y
B X
B X
C Y
B X
B X
B X
A Z
B Z
B X
C X
A Z
C Y
B X
B Z
B X
B X
A Z
B X
A Y
C Y
B X
B Z
C X
A Z
A Z
B Z
B Z
A X
B X
A Y
B X
B X
B X
B X
A Z
B Z
B Z
C Y
A X
A Y
A Y
A Z
B X
A Y
B Z
C Y
B Z
B X
A Z
B Z
B X
B Z
B Z
B Z
B X
C Y
B X
B X
A Y
B X
C X
A Y
A Z
A Y
B X
C Y
B Z
B X
B X
A X
B X
B X
A Y
A Z
C Z
A Y
B X
B X
C Y
A X
A Z
B X
B Z
B Z
C Y
A Z
C Y
A Z
C Y
C Y
B Z
C Y
B X
C Y
C Y
B X
B Z
C X
C Y
A Y
B X
C Y
B X
B X
C Y
B Z
B Z
A Z
A Z
C Y
B X
B Z
B X
B X
B X
C Y
B X
C Y
A Z
A Z
B X
B X
A Y
A X
B X
A Z
A Y
C Y
B X
A Y
A Y
B X
A X
A Z
A Y
A Z
C Y
C Y
C Y
A Y
B X
B X
A Y
C Y
B X
A X
C Y
C Y
A Y
C Y
C Y
B Z
C Y
B X
C Y
B X
B X
B X
A Y
B Y
B X
C X
B X
A X
A Y
C Y
C Y
B X
B X
A Y
B X
B X
A Y
C Y
C X
A Y
B X
B Z
B Z
B Z
B X
A Z
B X
B X
A Y
B X
B X
A Y
B Z
A Y
B X
B X
B Z
A Z
A Y
A Z
A Y
C Y
B X
C X
B X
B X
A Z
B X
B Z
B X
A Z
C Y
B X
B X
B Z
A Z
A Y
B X
B Y
A Y
A Z
A Y
C Z
B X
B X
B X
A Z
B X
B X
B X
A Y
B Z
C Y
C Y
A Z
A Z
A Y
B X
A Y
B Z
C Y
B X
B Z
A Y
B X
A Y
C Y
B X
B X
A Y
A Z
A Z
A Z
B X
B X
A Z
B X
B X
B Z
A X
B Z
A Z
B X
C Y
C X
A Z
B X
A Y
B Y
B Z
B X
B X
A Y
B X
A Z
A Z
C X
B X
B Z
A Y
C Y
A Y
B X
B Z
B X
A Z
B Z
C Y
B Z
B X
B X
B X
A Y
B X
B X
A Z
C Y
B X
C Y
B X
C Y
A Z
A Y
A X
C Y
B X
B X
B Z
B X
A Y
A Y
B X
B X
A Z
C Y
B Z
B X
B X
A X
A Y
B Z
C Y
A Z
C Y
A Z
B X
A Y
B X
A Y
B X
B X
C X
B Y
C Z
A Z
C Y
B X
B X
B Z
C Z
A X
A Y
A Z
B X
C Y
B Z
B Z
A Y
B X
B X
A Y
A Z
B X
B X
A Z
B X
B X
B Z
A X
B X
A X
A Y
C Y
B X
B Z
A Y
B X
A X
B X
B X
B Z
B X
B X
A Y
B X
B X
A Y
A Y
C Y
B Z
B X
A X
A Z
B X
B X
C Z
B X
B X
B X
B X
B X
C Y
C Y
C X
B X
B X
B Z
B Z
B X
A Y
B Z
B Z
B Z
B X
B X
B X
B X
A Y
A Y
B X
C Y
C Y
B X
B X
A Y
C Y
A Z
C Y
B X
C Z
B X
B Z
B X
C Y
C Y
B X
B X
B X
C Y
B X
B X
A X
B X
C Y
A Y
B X
B X
B X
C X
C Y
A Y
B X
B X
C Y
A Y
B X
A Y
A Y
B Z
C Y
B Z
A Y
A Z
C Y
B X
C Y
B X
C Y
C Y
B X
B X
B X
B Z
A Y
B X
B X
B X
A Y
B X
B X
A Y
B X
A Y
C Y
A Z
B X
B X
C Y
B X
B X
A Y
A Z
C Y
B X
B Z
B Z
B X
C Y
B X
A Y
C X
C Y
B X
B X
B Z
C Y
B X
B X
C Y
C Y
B X
C Y
B Z
C Y
C X
B Z
C Y
B Z
C Y
A X
B Z
B Z
B X
B X
C Y
B X
C Y
B X
B X
B X
A Y
B X
C Y
B Z
C Y
C Y
A Y
C Z
A Y
B X
A Z
C Z
C Y
B X
B X
A Y
B Z
B X
C Y
B X
B Z
A Z
B Z
A Y
C Y
A Z
B X
B X
C Y
C Y
B X
B X
⛄"""
