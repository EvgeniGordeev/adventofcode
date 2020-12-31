#!/usr/bin/env python3

# HELPER FUNCTIONS
from copy import deepcopy
from functools import lru_cache


def parser(text) -> list:
    slice_1d = [list(line) for line in text.strip().split('\n')]
    return [[['.'] * 3 for i in range(3)], slice_1d, [['.'] * 3 for i in range(3)]]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
DIRS = [(z, y, x)
        for x in range(-1, 2)
        for y in range(-1, 2)
        for z in range(-1, 2)
        if not (z == 0 and y == 0 and x == 0)]


@lru_cache()
def neighbors(x, y, z, size):
    cells, c = [], sum((x, y, z))
    for dz, dy, dx in DIRS:
        for i in range(1, 2):
            nz, ny, nx = z + i * dz, y + i * dy, x + i * dx
            if -1 < nz < size and -1 < ny < size and -1 < nx < size:
                    # and abs(sum((nz, ny, nx)) - c) in (0, 1)\
                cells.append((nz, ny, nx))
    return cells


def expand_visible_area(old_cube: list) -> list:
    cube = deepcopy(old_cube)
    size = len(cube)
    if any('#' in xy for xy in cube[0]) or any('#' in sublist for sublist in cube[size - 1]):
        new_size = size + 2
        for z in cube:
            for y in z:
                y.insert(0, '.')
                y.append('.')
            z.insert(0, ['.'] * new_size)
            z.append(['.'] * new_size)
        cube.insert(0, [['.'] * new_size for i in range(new_size)])
        cube.append([['.'] * new_size for i in range(new_size)])
        return cube
    return cube


def simulate_cycle(cube: list) -> list:
    _cube = expand_visible_area(cube)
    new_cube, size = deepcopy(_cube), len(_cube)
    for z in range(size):
        for y in range(size):
            for x in range(size):
                val, neibors = _cube[z][y][x], neighbors(x, y, z, size)
                active = sum(1 for a, b, c in neibors if _cube[a][b][c] == '#')
                if val == '#' and active not in (2, 3):
                    new_cube[z][y][x] = '.'
                elif val == '.' and active == 3:
                    new_cube[z][y][x] = '#'

    return new_cube


def part1(cube, cycles=1) -> int:
    res = cube
    for i in range(cycles):
        res = simulate_cycle(res)
    return sum(x.count('#') for z in res for y in z for x in y)


# TEST
def test() -> bool:
    # GIVEN
    given = parser("""
.#.
..#
###
""")
    assert part1(given, 1) == 11
    assert part1(given, 2) == 21
    return True


if __name__ == '__main__':
    assert test()

    model = parser(read_input())
    # ONE #1
    part_1 = part1(model)
    print(part_1)
    assert part_1 == 28884
    # # TWO #2
    part_2 = part2(model)
    print(part_2)
    # assert part_2 == 3443997590975

# INPUT
"""🎅
.......#
....#...
...###.#
#...###.
....##..
##.#..#.
###.#.#.
....#...
⛄"""
