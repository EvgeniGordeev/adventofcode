#!/usr/bin/env python3
import copy
import re
import string
from collections import deque, defaultdict


def parser(text) -> tuple:
    crates, rearrangements = text.strip('\n').split('\n\n')

    model = defaultdict(deque)

    for level in crates.split('\n'):
        pos, step, = 0, 4
        limit = len(level) // step
        while pos <= limit:
            ind = pos * step + 1
            if level[ind] in string.ascii_uppercase:
                model[pos + 1].append(level[ind])
            elif level[ind] in string.digits:
                break
            pos += 1

    return model, [tuple(map(int, re.findall(r'\d+', instruction))) for instruction in rearrangements.split('\n')]


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN FUNCTIONS
def part1(given: dict, steps: list) -> str:
    crates = copy.deepcopy(given)
    for how_many, from_, to in steps:
        for _ in range(how_many):
            # move one by one
            crates[to].appendleft(crates[from_].popleft())
    return ''.join([crates[i + 1][0] for i in range(len(crates)) if crates[i + 1]])


def part2(given: dict, steps: list) -> str:
    crates = copy.deepcopy(given)
    for how_many, from_, to in steps:
        # move multiple crates at once preserving order
        crates[to] = deque(crates[from_].popleft() for _ in range(how_many)) + crates[to]
    return ''.join([crates[i + 1][0] for i in range(len(crates)) if crates[i + 1]])


# TEST
def test():
    # GIVEN
    given = parser("""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""")
    assert part1(*given) == 'CMZ'
    # part 2
    assert part2(*given) == 'MCD'

    return True


if __name__ == '__main__':
    assert test()
    given = parser(read_input())
    # ONE #1
    res1 = part1(*given)
    print(res1)
    assert res1 == 'TDCHVHJTG'
    # TWO #2
    res2 = part2(*given)
    print(res2)
    assert res2 == 'NGCMPJLHV'

# INPUT
"""🎅
[F]         [L]     [M]            
[T]     [H] [V] [G] [V]            
[N]     [T] [D] [R] [N]     [D]    
[Z]     [B] [C] [P] [B] [R] [Z]    
[M]     [J] [N] [M] [F] [M] [V] [H]
[G] [J] [L] [J] [S] [C] [G] [M] [F]
[H] [W] [V] [P] [W] [H] [H] [N] [N]
[J] [V] [G] [B] [F] [G] [D] [H] [G]
 1   2   3   4   5   6   7   8   9 

move 6 from 4 to 3
move 5 from 8 to 9
move 1 from 4 to 5
move 1 from 4 to 5
move 2 from 2 to 7
move 2 from 1 to 6
move 9 from 6 to 1
move 12 from 3 to 5
move 1 from 8 to 4
move 3 from 1 to 5
move 1 from 6 to 7
move 10 from 5 to 2
move 14 from 5 to 1
move 8 from 7 to 9
move 11 from 2 to 9
move 1 from 3 to 9
move 11 from 1 to 5
move 2 from 1 to 9
move 1 from 4 to 8
move 6 from 1 to 5
move 1 from 8 to 3
move 16 from 5 to 1
move 4 from 1 to 3
move 1 from 5 to 6
move 4 from 3 to 4
move 1 from 6 to 7
move 21 from 9 to 6
move 2 from 1 to 9
move 2 from 4 to 9
move 5 from 9 to 4
move 9 from 1 to 6
move 6 from 4 to 6
move 1 from 6 to 2
move 1 from 7 to 6
move 1 from 3 to 2
move 8 from 6 to 9
move 3 from 1 to 8
move 1 from 2 to 1
move 13 from 6 to 3
move 1 from 1 to 9
move 2 from 1 to 6
move 3 from 8 to 4
move 4 from 4 to 9
move 3 from 1 to 3
move 22 from 9 to 8
move 1 from 2 to 9
move 6 from 8 to 9
move 15 from 6 to 5
move 5 from 8 to 9
move 11 from 9 to 8
move 13 from 5 to 1
move 1 from 6 to 5
move 1 from 9 to 3
move 21 from 8 to 3
move 3 from 5 to 3
move 11 from 1 to 2
move 25 from 3 to 1
move 5 from 1 to 7
move 20 from 1 to 7
move 1 from 6 to 7
move 16 from 3 to 9
move 8 from 9 to 6
move 1 from 1 to 5
move 5 from 9 to 4
move 2 from 2 to 1
move 2 from 9 to 4
move 1 from 9 to 4
move 1 from 8 to 4
move 1 from 5 to 2
move 3 from 4 to 6
move 1 from 4 to 7
move 9 from 7 to 6
move 5 from 4 to 6
move 7 from 7 to 2
move 1 from 1 to 6
move 11 from 2 to 5
move 10 from 5 to 1
move 1 from 6 to 8
move 1 from 5 to 7
move 24 from 6 to 1
move 12 from 1 to 4
move 12 from 4 to 8
move 2 from 2 to 7
move 3 from 7 to 2
move 5 from 2 to 8
move 9 from 8 to 9
move 9 from 8 to 5
move 1 from 9 to 1
move 14 from 1 to 8
move 11 from 7 to 9
move 4 from 1 to 3
move 7 from 1 to 2
move 3 from 3 to 7
move 12 from 9 to 7
move 8 from 7 to 2
move 4 from 9 to 2
move 1 from 3 to 6
move 5 from 5 to 9
move 14 from 2 to 1
move 8 from 9 to 4
move 6 from 4 to 5
move 5 from 5 to 7
move 1 from 8 to 2
move 2 from 4 to 6
move 4 from 7 to 3
move 10 from 8 to 4
move 2 from 3 to 6
move 7 from 7 to 6
move 10 from 4 to 8
move 5 from 1 to 6
move 8 from 2 to 1
move 7 from 6 to 8
move 9 from 6 to 5
move 16 from 1 to 6
move 2 from 3 to 9
move 1 from 7 to 4
move 2 from 9 to 1
move 14 from 6 to 7
move 1 from 6 to 3
move 2 from 6 to 3
move 9 from 5 to 7
move 3 from 1 to 6
move 3 from 3 to 7
move 5 from 5 to 9
move 3 from 6 to 2
move 1 from 6 to 2
move 12 from 8 to 2
move 5 from 2 to 1
move 2 from 1 to 3
move 25 from 7 to 1
move 1 from 4 to 6
move 2 from 3 to 9
move 26 from 1 to 9
move 2 from 1 to 8
move 1 from 6 to 8
move 1 from 7 to 1
move 7 from 8 to 1
move 7 from 1 to 5
move 1 from 1 to 2
move 2 from 8 to 6
move 32 from 9 to 8
move 1 from 6 to 5
move 5 from 2 to 9
move 1 from 9 to 7
move 24 from 8 to 3
move 1 from 6 to 9
move 3 from 2 to 5
move 1 from 7 to 9
move 4 from 9 to 3
move 8 from 8 to 7
move 18 from 3 to 7
move 20 from 7 to 8
move 6 from 8 to 9
move 6 from 5 to 1
move 8 from 9 to 4
move 3 from 5 to 4
move 8 from 8 to 4
move 2 from 5 to 2
move 3 from 1 to 5
move 4 from 3 to 7
move 6 from 2 to 9
move 3 from 3 to 6
move 6 from 4 to 5
move 2 from 6 to 3
move 1 from 3 to 1
move 4 from 3 to 8
move 8 from 4 to 3
move 4 from 3 to 7
move 4 from 4 to 5
move 4 from 9 to 5
move 3 from 3 to 4
move 3 from 4 to 9
move 1 from 1 to 4
move 2 from 1 to 5
move 7 from 7 to 8
move 4 from 7 to 4
move 1 from 6 to 7
move 1 from 1 to 5
move 1 from 3 to 8
move 11 from 5 to 9
move 17 from 9 to 8
move 13 from 8 to 4
move 1 from 4 to 8
move 4 from 7 to 1
move 4 from 8 to 3
move 6 from 5 to 4
move 3 from 3 to 6
move 2 from 1 to 9
move 1 from 9 to 5
move 1 from 3 to 5
move 5 from 5 to 9
move 2 from 1 to 8
move 21 from 8 to 6
move 2 from 8 to 4
move 4 from 9 to 6
move 1 from 9 to 7
move 19 from 4 to 1
move 28 from 6 to 5
move 7 from 4 to 2
move 28 from 5 to 3
move 1 from 9 to 4
move 1 from 4 to 2
move 1 from 7 to 8
move 1 from 8 to 9
move 13 from 1 to 3
move 8 from 2 to 8
move 3 from 1 to 2
move 5 from 8 to 5
move 1 from 2 to 7
move 1 from 9 to 7
move 1 from 2 to 3
move 2 from 7 to 9
move 1 from 2 to 6
move 1 from 9 to 1
move 9 from 3 to 9
move 3 from 9 to 1
move 1 from 6 to 8
move 21 from 3 to 7
move 7 from 9 to 4
move 2 from 4 to 2
move 1 from 8 to 6
move 7 from 1 to 4
move 7 from 7 to 8
move 4 from 5 to 9
move 10 from 7 to 1
move 7 from 3 to 9
move 1 from 7 to 9
move 1 from 5 to 3
move 3 from 3 to 5
move 10 from 4 to 2
move 1 from 3 to 7
move 2 from 4 to 9
move 3 from 9 to 1
move 3 from 7 to 1
move 1 from 6 to 4
move 1 from 1 to 2
move 1 from 3 to 4
move 2 from 4 to 3
move 1 from 7 to 4
move 4 from 8 to 9
move 1 from 4 to 9
move 3 from 1 to 9
move 12 from 1 to 7
move 2 from 9 to 5
move 12 from 9 to 7
move 5 from 5 to 1
move 1 from 8 to 5
move 4 from 1 to 4
move 1 from 9 to 6
move 1 from 3 to 4
move 3 from 8 to 3
move 1 from 1 to 7
move 8 from 2 to 5
move 2 from 8 to 1
move 10 from 7 to 1
move 4 from 9 to 5
move 2 from 5 to 8
move 11 from 5 to 4
move 6 from 7 to 2
move 2 from 2 to 1
move 1 from 7 to 5
move 1 from 5 to 1
move 2 from 4 to 8
move 1 from 6 to 9
move 8 from 4 to 3
move 8 from 1 to 7
move 7 from 1 to 2
move 4 from 3 to 9
move 1 from 9 to 6
move 7 from 2 to 1
move 5 from 2 to 3
move 2 from 7 to 8
move 5 from 8 to 4
move 2 from 9 to 3
move 1 from 8 to 1
move 6 from 3 to 5
move 10 from 3 to 1
move 3 from 5 to 3
move 3 from 2 to 1
move 1 from 5 to 4
move 6 from 4 to 5
move 1 from 6 to 2
move 3 from 4 to 7
move 1 from 9 to 4
move 2 from 3 to 1
move 1 from 9 to 8
move 1 from 3 to 7
move 4 from 4 to 8
move 2 from 7 to 4
move 8 from 5 to 9
move 2 from 8 to 6
move 2 from 4 to 3
move 2 from 3 to 4
move 4 from 9 to 7
move 1 from 8 to 7
move 2 from 6 to 9
move 2 from 8 to 9
move 1 from 2 to 9
move 1 from 7 to 8
move 1 from 2 to 7
move 19 from 7 to 6
move 1 from 8 to 1
move 2 from 4 to 8
move 5 from 6 to 1
move 2 from 7 to 2
move 2 from 2 to 8
move 2 from 1 to 8
move 4 from 8 to 2
move 3 from 2 to 8
move 6 from 9 to 5
move 8 from 6 to 3
move 26 from 1 to 6
move 1 from 5 to 3
move 1 from 1 to 5
move 8 from 3 to 1
move 1 from 3 to 7
move 3 from 9 to 2
move 4 from 2 to 6
move 26 from 6 to 1
move 1 from 7 to 5
move 3 from 8 to 4
move 2 from 8 to 2
move 7 from 1 to 2
move 1 from 5 to 9
move 2 from 4 to 6
move 9 from 6 to 2
move 18 from 1 to 7
move 6 from 7 to 1
move 6 from 5 to 6
move 1 from 1 to 2
move 19 from 2 to 7
move 1 from 4 to 2
move 9 from 7 to 1
move 3 from 6 to 7
move 1 from 9 to 4
move 1 from 2 to 3
move 8 from 7 to 8
move 4 from 6 to 5
move 2 from 6 to 3
move 1 from 4 to 2
move 4 from 5 to 1
move 8 from 8 to 7
move 17 from 7 to 8
move 3 from 3 to 1
move 1 from 2 to 8
move 8 from 8 to 4
move 8 from 8 to 7
move 1 from 8 to 2
move 7 from 7 to 6
move 1 from 2 to 7
move 5 from 7 to 8
move 7 from 1 to 6
move 10 from 6 to 1
move 4 from 7 to 9
move 3 from 9 to 7
move 1 from 7 to 2
move 6 from 4 to 2
move 7 from 1 to 5
move 4 from 2 to 5
move 16 from 1 to 9
move 3 from 2 to 7
move 2 from 4 to 9
move 4 from 1 to 6
move 5 from 7 to 4
move 4 from 6 to 3
move 1 from 7 to 4
move 1 from 6 to 9
move 1 from 8 to 5
move 4 from 3 to 2
move 2 from 5 to 3
move 3 from 6 to 2
move 3 from 2 to 1
move 9 from 5 to 8
move 1 from 3 to 1
move 10 from 8 to 1
move 1 from 8 to 5
move 16 from 9 to 2
move 1 from 3 to 2
move 12 from 1 to 9
move 1 from 9 to 2
move 3 from 1 to 6
move 2 from 1 to 9
move 3 from 6 to 8
move 20 from 2 to 7
move 16 from 9 to 7
move 1 from 7 to 5
move 2 from 5 to 9
move 2 from 2 to 3
move 2 from 8 to 5
move 3 from 9 to 7
move 2 from 5 to 2
move 1 from 4 to 6
move 2 from 1 to 4
move 23 from 7 to 5
move 4 from 8 to 5
move 7 from 7 to 1
move 16 from 5 to 7
move 1 from 6 to 5
move 1 from 2 to 4
move 2 from 3 to 9
move 1 from 2 to 3
move 13 from 5 to 1
move 1 from 3 to 8
move 1 from 9 to 4
move 19 from 1 to 9
move 2 from 1 to 9
move 22 from 9 to 8
move 14 from 8 to 5
move 12 from 5 to 3
move 21 from 7 to 9
move 14 from 9 to 7
move 1 from 8 to 6
move 9 from 3 to 7
move 1 from 3 to 2
move 4 from 4 to 1
move 1 from 2 to 4
move 1 from 3 to 9
move 6 from 8 to 9
move 4 from 1 to 7
move 2 from 5 to 9
move 6 from 4 to 5
move 4 from 7 to 4
move 1 from 5 to 3
move 5 from 9 to 7
move 2 from 3 to 1
move 6 from 9 to 6
move 1 from 1 to 6
move 2 from 4 to 2
move 8 from 7 to 5
move 20 from 7 to 5
move 2 from 5 to 6
move 4 from 9 to 5
move 1 from 1 to 3
move 1 from 3 to 4
move 1 from 2 to 7
move 1 from 4 to 9
move 9 from 6 to 3
move 2 from 4 to 3
move 28 from 5 to 3
move 1 from 8 to 3
move 1 from 8 to 1
move 1 from 2 to 8
move 1 from 6 to 2
move 1 from 8 to 1
move 6 from 5 to 7
move 1 from 5 to 1
move 1 from 9 to 2
move 1 from 1 to 3
move 1 from 9 to 7
move 2 from 1 to 2
move 11 from 3 to 8
move 3 from 8 to 6
move 3 from 6 to 9
move 25 from 3 to 7
move 4 from 3 to 8
move 4 from 2 to 3
move 9 from 8 to 9
move 2 from 3 to 7
move 3 from 8 to 2
move 11 from 9 to 7
move 1 from 9 to 1
move 4 from 7 to 3
move 1 from 1 to 5
move 23 from 7 to 2
move 12 from 2 to 3
move 2 from 3 to 9
move 12 from 2 to 1
move 2 from 3 to 9
move 1 from 5 to 4
move 1 from 2 to 5
move 1 from 9 to 4
move 1 from 5 to 9
move 2 from 4 to 2
move 3 from 1 to 4
move 1 from 2 to 1
move 10 from 3 to 2
move 7 from 7 to 3
move 11 from 7 to 9
move 5 from 3 to 1
move 1 from 4 to 5
move 11 from 2 to 3
move 9 from 9 to 3
move 3 from 9 to 4
move 2 from 4 to 8
move 1 from 5 to 6
move 13 from 1 to 5
move 3 from 3 to 8
move 3 from 7 to 2
move 1 from 7 to 4
move 3 from 8 to 3
move 8 from 3 to 8
move 4 from 4 to 5
move 2 from 8 to 2
move 8 from 8 to 3
move 1 from 6 to 3
move 2 from 2 to 8
move 6 from 5 to 2
move 3 from 2 to 8
move 1 from 1 to 7
move 2 from 9 to 3
move 3 from 5 to 4
move 2 from 8 to 6
⛄"""
