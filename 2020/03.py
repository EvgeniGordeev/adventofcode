#!/usr/bin/env python3
from collections import namedtuple
from typing import List


# common functions
def read_data():
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


def parse(_input: str):
    return [l for l in _input.split("\n") if len(l) > 0]


# solution
Slope = namedtuple('Slope', ['right', 'down'])


def count_trees(matrix: list, sl: Slope) -> int:
    # the same pattern repeats to the right many times - multiply each line by the slope
    _matrix = [str(line * int(sl.right * len(line) / sl.down)) for line in matrix]

    h = len(_matrix)
    w = len(_matrix[0])
    counter, i, j = 0, sl.down, sl.right

    while i < h and j < w:
        if _matrix[i][j] == '#':  # that's a tree
            counter += 1
        i += sl.down
        j += sl.right
    return counter


def count_trees_for_slopes(_matrix: List[str], _slopes: List[Slope]) -> int:
    counter = 1
    for sl in _slopes:
        counter *= count_trees(_matrix, sl)
    return counter


# test
test_input = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""
forest = parse(test_input)

# test 1
part_one = count_trees(forest, Slope(3, 1))
assert part_one == 7

# test 2
SLOPES_TWO = [Slope(1, 1), Slope(3, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)]
part_two = count_trees_for_slopes(forest, SLOPES_TWO)
assert part_two == 336

# given
forest = parse(read_data())
# solve
part_one = count_trees(forest, Slope(3, 1))
print(part_one)
assert part_one == 250

part_two = count_trees_for_slopes(forest, SLOPES_TWO)
print(part_two)
assert part_two == 1592662500

# input
"""🎅
........#..#.##.#..............
...#...............#.#.........
...#..#...#..##....#...........
...#.............#....#.....#..
..#......#..#...#.......#......
..............##...............
#.......#.........#......#....#
.#.....###.....#...#.#.#...#...
#.....................#....#.#.
.......#...................#...
...#.#...................#....#
....#....#.......#...#.........
..##.#............#..#.........
.....##.#..............##..###.
...........#....#....#.........
#.....#...#...#.#.#.#.##.#...#.
.#...............#....##.......
.....#..#......#....#.......##.
.....#........#.......#........
...#...##...#..##...#.....##...
.....#.........#.###...##...#..
.#.##...#........#.#.#.#....#..
....#......##.#...#.....#....#.
.......###..........#..#..#....
......#...#.##.................
....#...#...#.........#......#.
.....#...........#...###....#..
.....#...#.#.#....##.#......#.#
......#...#.....#..#..#........
#......#..#...##........###....
##.....#....##..#.#.###.#...#..
........#....#.......#.....#..#
#.#.#.##.#.#...................
..#...##....#......#.....##....
.......#.##..#........##..#....
.#.#....##......#.#..........#.
#..............#............#..
.#.#.#.#.#.####.#.#...##.......
.#..#.....##.#.......#.##...#..
..#.#........#.............#.#.
..#.#..........#..#........#...
..#..#...#.......##...#.#....##
...#.....#.#.#.....#....#....#.
.#...#......#.....#..##........
...#.......##.#.#.....#......#.
...........#.....#.#.......#...
#...........#...#..#.#........#
....#......#..##........#..###.
.#..#........................#.
#.......#......#...#...#..#....
....#.#...#..#.#....#....##.#..
.....#......#..#..........##.#.
.#.....#...........#.........#.
...###.#...#.......#.#.........
.......#....#..........#..#...#
......##..#.......#...##.......
..#..........#.......#.........
..........#..#..#..#..#........
.#.................####...#.#.#
..##.....#............#........
....#.....###...#......#....#.#
...##.#...........#.##......#..
#..##..#..#....#...#..#........
......#....#........#.......#..
......#.....#......###.........
.#.....#.#......#.......#......
..#.........#..#..#........##.#
..#.#....#.....#....##....#.#..
...#.............##............
........#..#..#......#...#.....
.....#.#...#...##.....#.....#..
.#..#.#..........##...##.....#.
......##.#..........#...#.....#
#.#.##......#....#..........#..
................#.......#.##...
#.......#.....#.......#....#...
#..#.....#.##..##...........#..
.....#....#.#.##..........#..##
#.......#.....#.##...........#.
........#.##........###..#.#...
........#..................#...
#.........................#...#
....#.........#...#.#..#.....#.
.#............#....#...........
..#.#...#..##...#.#.......#....
.#.#....#...........#.........#
...#.#..........#.....#...#....
......#....#.#...............##
....##......###...##.##.....##.
............#.#....#.#.....#..#
.....#..#.....#.#...###....#...
.......##....##..#...##..#...##
.....#.......##..#...#...#....#
#.........##....#........###.#.
...#..##...#...#.........#.#.#.
....#.#.....#.....#............
#........#....#..#........#....
.......#....#...#..............
#...#.........##.....###.#.....
.#....##..#...#..##.........#..
....#.....#......##..#..#....#.
#.#..#.........#........#......
..#.......#.........#.....###..
..#..........#...........#....#
..#...............#......#..#..
....#..#...#....###.....#..#..#
#...#...#..#...........#....#..
.#....#.#..#....#.#...........#
.....#.....#..#....#..#....#...
#.#..#...........#.#...........
..................#.#.......#..
...#.........#.....#..##....#..
.........#.#...#.........##....
...#..#....#.....#...#..#......
.#.##.....#....#....#......##..
##..#.........#.#....#...#.....
#......#.#...#....#.#..#.......
.......#.....#.....###....#.#..
.#....##.#.....#...#.......#...
.#.......#..#...#......#..#..##
...............#...#...........
#..............#....#.#.#....#.
...........#..#.......#.##..#..
..#......#.#....#...#.#.....#..
#..............................
#..#....#..........#...#.......
......#.............#####......
.#...###......#.#.#.##..#......
............#.##.....#.........
.........#....##....#..........
###....#......#.......#........
.#.......##..........#..#....#.
#..#.....................#....#
........#...........#..........
..#..........#...#..#.........#
..#..#......##................#
.....##..#...#..#..............
.......#...##..#...............
.......##..#.####....#....#.#..
#.#..#..........#........##....
....##....#.#..#....#.#...#....
......#.......#...#.....#...#..
..#..#...#.....#.......###.....
...#.......#.#.#.......#.##....
...............#..#.#........#.
.#....###.#......#.............
.#..#...#....#.#..#.....#......
.......#.##....#.#.##.##...#.#.
..#...#....#.#..##.#.....#...##
..#...#......#...#......#...#..
....#..#...#.#..#......#.......
#..#...............#......#.##.
.#....#...#..........#.#.....#.
.#..#.#.#................#..#..
.#....#.#...#..##.###..#...###.
#.............#.....#.........#
...#.........#...#.......#..#..
......#..#.........#..........#
........##................#..#.
......#...#.#.....#......##....
...............#...#....#......
...#.#..#..#.....##.###..##..#.
.#....##......#...#..##..#.....
.....#.........##.##....#...#..
.....#.#..................####.
#.....#...#.............##....#
#.#..........#...#..#..#.......
#..#.#.........#...............
....#...#.........#...##.......
...........#.....#..##..#......
#.....#.......#.#........#.....
..##..#.....#...##......#......
....#....#.....................
............#......#.........##
.....##.............#.....##..#
.......#.............#..#.#.##.
.###...#......#..#........##.#.
..#.#...#.#....#.....#..#......
..#.#..#.##........#...#.......
........#.#...............#..#.
........##.......#...#.......#.
...#........##.#..........#.#.#
..#..###.#.#.......#.#......#..
....#..........#...#..#........
...#..#...#...#.#....#...#..#..
...#...#........#......##...#.#
#...........#..........#..#.##.
...#..##..................#.#..
...##.#...#....#.#...#.####....
.....#...#.#.#..#..............
.....#..#.#.#..#...............
..#..#..##...#.#..#.....##....#
.......#.#..#.....#....#.......
...#..#....#.........#...#.....
..............#.#...#...##.....
...................#...........
.#......#.#...................#
.##.....#........#.........#..#
.##..##...#...................#
...#....#.#..#.#.#..#.....##...
.......#..#....#......####.#...
.##..#..##....#.......#........
.#...#...........##............
.....#.....#........#..........
....##..#....#.....#...........
.#...#....................#....
....#.........#.......##.....#.
.#....#..#.....#.##....#.......
....#..#.........#.#....#.#....
.......#.........##....#.......
..#......#....#....#...#.......
........#..#.......#.##......#.
..#.....#......#...#..#.......#
#..#.....##...#...#............
.......##.......#........#...#.
..#......................#...#.
....##.#.............#......#..
#.#............................
...##.#.....#.#............#.##
......#...#..#.........##......
.#.......#.....##.......#.#....
...........#.#.........#..##...
...#..........#.##....#........
........#..#..#...#....#....#..
........##....#.#....#........#
..#........##....###....#......
#................###...#...#...
................#.#..###......#
..#.....##.#................#..
.....#...............#..#......
..#.......####.....#..#.#....##
..#.....#..#....#..............
#.#...........#.#.....#..##....
#.#..........#.......#...#.###.
........#....#...#..#.#........
.#.....#......#..#..#..###..#..
.#.........#.##.#.#......##....
..#.........#...##..#........#.
.#...................#.........
...#.#........#................
............#.....#..##........
..#.....#.#......#.......#...#.
........#....##..##...#.....##.
.#........#.#....#.#....#.#..#.
#.#.......#....................
.#..#...##.........#..#........
.........#...............#.....
...#...#.....#......#.......#..
###......................#.#..#
...#.....####........#..#.....#
#.#...#.#...................##.
.........#.....................
#..........##..#.....#....#....
.......#...#.#.##.#..##........
..........#..#.#..#.#.......#.#
.....................#.#...#...
...........#.#........#.#.#....
.......#......#........#...#.#.
.........#....................#
.##.##....#...#.#.#.#..........
#....##..#.##....#....#.......#
.##.#...#...............#....#.
.......#...#.###....#..........
.....#....#...#..#.............
#.........#.##....#.#.#........
..#...#.............##..#..#...
#..##.......#..........#...#.#.
.#..#.....#...........#......#.
......#......#..............##.
.#...#..#...#..####.....#.....#
....##.......#..........##.....
.#.....#.......#.....#.#...#...
..#..#..#.#...#......#.........
......#.#....#........#.......#
........#.......#..............
..#...#.#....#........#.......#
............#....#...##.#......
.........#.............#..#....
#.............#.#..##.......#..
#....#...........###....#......
...#.....................#.....
....#.#..........#...#.......#.
......#..#.......#...#...#....#
.#.#..#.....##.#........#......
...........#...#.#.............
...###............#...#..#.....
..#.#.......#...#.#..#.........
.#......##...........#.....#.##
.....##.....#....##...##.#.#...
..........#.#.#......#........#
..#.#........#....##....#.#....
.#....#...##...........#....#..
##......#...#.......#..........
.##...###..#...#......#..##.#.#
...........##.#..##...#.......#
..#..............##............
........#..#........#...#..#.#.
..#.............#......#...##..
#...##....#...#....#....#.#....
.#.#......#..##............#.#.
.....###.#....##....#....#.....
#.#.#..........#...#...#.#.#...
.....#.#...........####........
.....#....##...#.##..#......#..
#....#.......#.##.......#..#...
.....#.....#........#..........
.......#.......#...#.##......#.
...#.........##...#.#.#......##
#........#........#...#..#.....
.#......#.#......#.#...#....#..
#..#....##.....##..............
...#.##............#..........#
.....#.#....#..#.#............#
..#......#...###.##.......###..
........#....#.#.#.#...........
............#..#........#.....#
....#...............#..........
......#....#....###..#.......##
#...#...##....#.........#...#..
...........#.#.............#...
...#..#.....#..##.#....#......#
..#...#..#...#......#..........
....#..#....#.......#........#.
⛄"""
