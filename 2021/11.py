#!/usr/bin/env python3


# INPUT
import copy
import sys
from functools import cache


def parser(text) -> list:
    return [list(map(int, line)) for line in text.strip().splitlines()]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN
@cache
def neighbors(x, y, h, w):
    return [(x + i, y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if
            (i, j) != (0, 0) and -1 < x + i < h and -1 < y + j < w]


def flash(grid, x, y, flashed):
    if (x, y) in flashed:
        return
    flashed.add((x, y))
    grid[x][y] = 0
    for xn, yn in neighbors(x, y, len(grid), len(grid[0])):
        if grid[xn][yn] == 9:
            flash(grid, xn, yn, flashed)
        elif (xn, yn) not in flashed:
            grid[xn][yn] += 1


def gain_energy(grid: list) -> set:
    flashed = set()
    for x, row in enumerate(grid):
        for y, octopus in enumerate(row):
            if octopus == 9:
                flash(grid, x, y, flashed)
            elif (x, y) not in flashed:
                grid[x][y] += 1
    return flashed


def part1(grid: list, steps=100) -> int:
    res = 0
    for _ in range(steps):
        res += len(gain_energy(grid))
    return res


def part2(grid: list) -> int:
    in_sync = sum(len(r) for r in grid)
    step, limit = 1, 2 ** 32
    while step < limit:
        if in_sync == len(gain_energy(grid)):
            return step
        step += 1
    print("Octopuses never synced")
    sys.exit(1)


# TEST
def test():
    # GIVEN
    sample_input = """
11111
19991
19191
19991
11111
"""
    given = parser(sample_input)
    assert part1(given, 2) == 9
    assert given == parser("""
45654
51115
61116
51115
45654
    """)
    sample_input2 = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
    """
    assert part1(parser(sample_input2), 10) == 204
    assert part1(parser(sample_input2), 100) == 1656
    # part 2
    assert part2(parser(sample_input2)) == 195
    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    part_1 = part1(copy.deepcopy(input_))
    print(part_1)
    assert part_1 == 1757
    # TWO #2
    part_2 = part2(input_)
    print(part_2)
    assert part_2 == 422

# INPUT
"""🎅
7232374314
8531113786
3411787828
5482241344
5856827742
7614532764
5311321758
1255116187
5821277714
2623834788
⛄"""
