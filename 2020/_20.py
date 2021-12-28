#!/usr/bin/env python3
import os
import re
# HELPER FUNCTIONS
from itertools import starmap

from math import isqrt


class Tile(object):
    def __init__(self, num, grid):
        self.num = num
        if len(grid) == 4:
            self.sides = grid
        else:
            self.grid = grid
            self.sides = {
                'n': grid[0],
                'e': ''.join([r[0] for r in grid]),
                's': grid[-1],
                'w': ''.join([r[-1] for r in grid]),
            }

    def flip(self):
        return Tile(self.num, {k: v[::-1] for k, v in self.sides.values()})

    def __repr__(self):
        return f"Tile({self.num})"

    def __hash__(self):
        return hash(self.num)

    def __eq__(self, other):
        return self.num == other.num


def read_txt(path: str) -> str:
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_, path), 'r') as file:
        data = file.read()
        return data


def parser(text) -> list:
    nums = list(map(int, re.findall(r'Tile (\d+):\n', text)))
    grids = [tuple(l.strip().split('\n')) for l in re.split(r'Tile \d+:\n', text) if l.strip()]
    return list(starmap(Tile, zip(nums, grids)))


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


def print_grid(grid):
    print('====')
    for l in grid:
        print(l)


# MAIN FUNCTIONS

def backtrack(square: list[Tile], tiles: list[Tile], side_size: int) -> list[Tile]:
    if len(square) == side_size ** 2 or len(tiles) == 0:
        return square

    def can_assemble(s: list[Tile], tile: Tile) -> bool:
        return s[-1].sides[1] == tile.sides[3]

    for i, t in enumerate(tiles):
        for j in range(4):
            new_t = Tile(t.num, t.sides[j:] + t.sides[:j])
            if len(square) == 0 or can_assemble(square, new_t):
                image = backtrack(square[:] + [new_t], tiles[:i] + tiles[i + 1:], side_size)
                if len(image) == side_size ** 2 == 0:
                    return image

    return []


def part1(tiles) -> int:
    l = len(tiles)
    n = isqrt(l)
    image = backtrack([], tiles, n)

    if len(image) == l:
        # multiply corners of the image tiles
        return image[0].num * image[n - 1].num * image[-1].num * image[-n].num

    return -1


#
#
# def part2(model: Model) -> int:
#     not_in = set()
#     for rule in model.rules:
#         not_in.update(range(rule[0], rule[1] + 1))
#         not_in.update(range(rule[2], rule[3] + 1))
#     non_valid = [v for t in model.tickets
#                  for v in t if v not in not_in]
#     return sum(non_valid)


# TEST
def test() -> bool:
    # GIVEN
    given = parser(read_txt('./20_test.txt'))
    # 1951    2311    3079
    # 2729    1427    2473
    # 2971    1489    1171
    # ====================
    # 1951 * 3079 * 2971 * 1171
    assert part1(given) == 20899048083289
    return True


if __name__ == '__main__':
    assert test()

    model = parser(read_input())
    # ONE #1
    part_1 = part1(model)
    print(part_1)
    # assert part_1 == 15919415426101
    # # TWO #2
    # part_2 = part2(boot_code)
    # print(part_2)
    # assert part_2 == 3443997590975

# INPUT
"""🎅
Tile 1913:
##..#....#
.#.#.#.###
#...##.##.
.....#.#.#
.#......##
.........#
#...###..#
.#..#.....
.##...#..#
#.#...#...

Tile 2579:
##...####.
##..#....#
...#...#.#
#.....###.
##..#...##
#....#..#.
.#.....###
.##...#...
#.........
...##.....

Tile 1531:
.......###
.#....####
.#.#.#...#
....#..#.#
.#.#.##..#
.#.#.#...#
#.##...###
##..#.....
#...#.....
##.##.#..#

Tile 1493:
#.##.#.#..
#.#..#.##.
..#.....#.
#.#.#....#
....#....#
...#####..
#####.#.#.
#.##..##..
..#.....##
.##..#.###

Tile 3109:
########.#
......#.##
#....#...#
##.#.##...
....#.#...
#####...##
....#....#
..##...###
.......#.#
#.##.#....

Tile 3343:
###......#
#..#.#..##
...#....#.
#.........
..#.....##
.....#####
.....####.
##.......#
..#.......
#.......##

Tile 2609:
####..#.##
#.#..#....
....###..#
###..#..#.
#.#......#
##..#..#..
#....#..#.
#......###
#..#....##
.#..#.###.

Tile 1823:
###..#....
..###...#.
..#.###...
...#.....#
#....#.#.#
.#..#.#..#
#..##.#..#
...##.....
....#.#.#.
###.##...#

Tile 3391:
....#...#.
.#.#....#.
#......#..
#..#....#.
#.##...#.#
...##.####
....##..#.
##.#.#..##
.....#..##
#.#.#..#.#

Tile 2753:
....###..#
.#..##.#.#
...#......
..#.###.##
...#..##..
....#.....
#......#..
#........#
......#..#
#..#.#...#

Tile 3989:
.#.###.#..
#......##.
.##......#
.......###
###....###
##........
##....#.#.
...#.#..#.
........#.
###..#..#.

Tile 1877:
...###...#
#.#..##...
.##.###.#.
#.#....#..
#..#.#.##.
#.......##
####..#.#.
##.#....##
.##.......
.#..##..##

Tile 2729:
#...####.#
...#.....#
.###......
...#..#..#
...#.#.#.#
.#.....##.
..#.....##
........#.
###.......
#..##...##

Tile 1031:
##.#..####
#.##.#....
..#.......
#......###
.##.###.##
#...#...#.
#..##.....
#..#.#.#..
....###...
....#.###.

Tile 3803:
#..#..##..
...##..#..
...#.#....
#.....#..#
#........#
.#..#.#.##
..#..#.#..
#..#.#.#..
..##..#.#.
#####.###.

Tile 3541:
.##.#..#..
.##..#...#
.#.#..#...
...#..##.#
..#.....#.
..##......
.##......#
##.......#
.#..#.##.#
###.#.##.#

Tile 3821:
.#.#.#....
..#..##...
#.##......
..#...#.##
#.####..#.
##.##.#...
..#..#....
....#....#
...###.#.#
.#..#.#.##

Tile 3853:
#####..#.#
.....#..##
#...#.##.#
.##....#.#
#.#......#
###...#.#.
##....#.##
#.#.#.#..#
....###...
##.#.#....

Tile 1249:
###...####
..#....#..
##.##....#
.........#
#.........
.##.#.##..
...#...##.
..........
##...#.#..
##.####..#

Tile 3673:
...##..#.#
.#..#..#.#
###......#
#.....###.
..#.#.....
#.#..#.###
.#.##.##..
.##....#..
.#...##..#
#.###..#.#

Tile 3163:
##.#.#####
.##....#..
####......
#..#.#..##
.#.#..##.#
##.....#.#
.......#..
#...#.....
..#..#....
###.#...#.

Tile 1759:
###.#...##
...#..#...
###..###..
.#.#...#.#
.##...#...
..###....#
#.#.....#.
......###.
..#.####.#
##..##..#.

Tile 1831:
.#...#...#
...#.#..##
#...#.#...
#...##.#..
.#.#.#..#.
......##.#
.........#
#....##.#.
......#..#
#..#...##.

Tile 2179:
.###.....#
..######.#
....#....#
...#....#.
#.##..#...
#..#....##
.#..#.#..#
..#.#....#
#.#.#.....
###.##...#

Tile 2713:
..###.#..#
#.#.....#.
#....#.#..
#...##....
##...#.#.#
###..###.#
.##..#..##
.#...##.#.
#.#.......
#...#.....

Tile 1889:
....#....#
......#.#.
##.###...#
.#..##...#
##.##.#..#
...#...##.
#....#...#
.......#..
.#...#..##
.#.####.##

Tile 1999:
##....##.#
#..#.##.##
..#...#...
#.....#...
......#...
#.....#..#
.#.##..#.#
..#..##..#
#...#..#..
###..##..#

Tile 2039:
.#....####
.##..#....
.#.......#
#........#
#.......#.
.#..#.....
#.##......
##....#..#
.........#
#.#......#

Tile 2969:
...#####..
..#.#...##
##.....#..
##.....###
#...#..###
#..#....##
#..##...##
.........#
#...##...#
.#......##

Tile 2153:
.##..###..
#.#..#..##
.#####....
#.#..#.###
#.....#.##
####..#.#.
..........
.#......#.
...##...#.
.#....####

Tile 2837:
..###.....
###.#.###.
.#....#...
##.....###
##.##..###
..#..##.##
.#....##..
#..##.##..
#..#......
#..##...#.

Tile 1619:
##..###.##
##....####
.#..##.#..
##.#...#..
#..##.##..
...#.#.#.#
.....#.##.
..##..#..#
#..#..#..#
......#.#.

Tile 3943:
.#.##.#.#.
.......#.#
.........#
...#..#..#
...#....##
#.#.##....
##.......#
.#..#.##.#
...##.#..#
#.##....#.

Tile 3389:
#...#.##..
#.##..#...
#.#.#.....
##...#...#
##.....#..
.#..###..#
..###.....
#.##..#.##
####....##
##.#.#####

Tile 3631:
##.###.###
#...#.....
..#.......
#....#.###
#.........
#.#.......
....##...#
........#.
#....#....
.....#.#..

Tile 2081:
##..##.#..
.##......#
........##
#.......##
......##.#
#....#....
.#.#...##.
....##..#.
#.#..#####
...#####..

Tile 1579:
##........
.....#...#
#......#..
#..#.#...#
...#..#...
#.##....##
...#......
.#...#..#.
..#....#.#
.##...#...

Tile 3019:
.##..####.
...#....##
...##.#.#.
#....#....
.........#
##..#..#.#
...#.#...#
.#.##.#.##
##..#.....
#..#..###.

Tile 2089:
##.##.#...
..#.##...#
##...#....
#........#
#..#.....#
..######.#
.......#..
...#..##..
#.#....#..
...#.#####

Tile 2297:
#.#.###...
#.##......
#..#..#...
......#..#
#....#...#
###.#..##.
#....##.##
.......#.#
.........#
.###.#.#..

Tile 1373:
#..#.####.
........#.
....#....#
.##..#...#
.#.....#.#
#.....#...
#..#..#..#
.##...##.#
##.......#
.##..#.#..

Tile 1259:
...#..##.#
....#.#..#
#..#.##.##
##..##....
#..#.#..##
#.#...#...
..#......#
...###.#.#
..........
.###..##..

Tile 2411:
.###..#.#.
.#..#..#..
#.....#..#
.#.....#..
##..#...#.
.#........
#...##....
#.#..##...
.....#.#.#
....#.##..

Tile 3359:
.##..##.##
..#.#..#.#
#.......#.
.#..###..#
.#.....#..
#.........
...#.....#
.##....#..
.........#
.#.##..#..

Tile 2437:
.#.....#..
#.#.......
....##.#..
##.###.##.
##.#....#.
#...#....#
##..##..##
...#..#..#
....##.#.#
.##.#.#...

Tile 1367:
....#####.
..#.#....#
##......#.
..##...##.
..##..##.#
..##.##..#
#.#......#
##...#...#
.....#.#..
##.###.###

Tile 3533:
##..####..
##..#....#
...#.....#
#.##..####
###..##...
....###..#
..#.....##
.##.#..#..
....#.##..
##.#.##.##

Tile 1451:
.####.#...
..##.#.#..
...#.#....
.........#
....#...##
##...##...
..#...#...
#...#.####
...#.#.###
#######...

Tile 3457:
#.##.###.#
#..#.#....
###.#....#
.#....#.##
.......##.
#...####.#
#.#####..#
#.#..#..#.
#.#.......
.#.##.....

Tile 2657:
..#####..#
......###.
#.....#..#
.#..###..#
...#.##...
#.....#..#
#....#####
....#..#..
#.#.###..#
.#..##.#..

Tile 2347:
#.##.#.###
#...#....#
..........
#.#.#.....
#....#....
#..#...###
#.##...#..
#.....#..#
#.#.###.#.
#...###.##

Tile 3923:
#.####...#
###...#.##
......#..#
..#..#..##
#....#.#.#
.........#
.....#.#.#
#..####..#
....##.#..
#..#...#..

Tile 2593:
####...#..
#...####.#
#......##.
..#..#....
#..#.....#
...#......
....#.....
#.#...##.#
.......#.#
#.#####.#.

Tile 1103:
..##...#.#
..#.....#.
#....#...#
...##....#
#.#.....##
.#.#.#.#..
#....#####
.#.#.#####
.........#
.##...#.#.

Tile 2671:
.##.##.#.#
...#.#....
##....#...
#......#..
.#....#.##
........##
..#...###.
###...#...
....#.#..#
.#######.#

Tile 3907:
###....#..
..##.....#
..........
##...#..##
##..#..##.
##..##..#.
#.#.....##
..###..#.#
#..#..#..#
#.#.......

Tile 1327:
.#..#..#.#
.###.###..
..#..#....
.#...#.#..
#.##.....#
#..#.#..#.
###...#...
##..#..#.#
......#...
#.#...###.

Tile 1163:
..#.#...#.
####.#.#..
.##.....##
#...#.....
.....####.
#...#..###
...#.##.#.
##..#..#..
.....#.#.#
.###...#.#

Tile 2683:
.......#..
.#.#.##..#
##..#...##
...#......
##.##...#.
...#.#.###
.#.##.....
#..#....#.
.###..#...
.#.#.....#

Tile 3881:
#.#.#..##.
##.#...###
##......##
#.........
#..#......
...#.#...#
.#..##....
.....##.#.
##...#....
###.....#.

Tile 2711:
#...#.#.##
#..##.....
...#......
#.#.#....#
#...#.#...
...#......
.#.#......
..#....#.#
#.##..#...
#.#.#.....

Tile 3491:
.###..#.##
.....#....
.##..#..##
##.##..#.#
.###....##
..##..#..#
..#......#
..#..#...#
#...#.#..#
.......##.

Tile 2339:
###.#####.
.#....#...
##.#.....#
#.........
#.........
..##..##.#
.###......
#...##....
##........
#.....#..#

Tile 1543:
..##...#..
.....#..##
....##....
.........#
.#..#.#..#
..........
.........#
#.#.#.....
##.#.#....
#.#.###..#

Tile 2371:
#..#.#####
##.#..###.
#.#...##..
#...###.##
#...#..#.#
##.....###
.#.......#
.....#.#..
..#.#.####
.###..##..

Tile 2971:
..###.#...
#.........
##.#...###
....###...
###......#
..###....#
##.#.....#
.#.....#..
#.....####
..##.##.#.

Tile 2203:
#.###.#.##
.#...##.#.
#.#.....#.
..#.#....#
##..#....#
##..#.....
#..#..#...
##........
..#..#.#..
##....#..#

Tile 2113:
###...##.#
......#...
.....##.#.
....####.#
##..#..#..
#...#...##
.......#.#
......#..#
#.##.#..##
....##.#..

Tile 1321:
.#..#..#..
##...#...#
..........
.####..#.#
##.#.#.#.#
#..#.#....
#..#.....#
.#.......#
....###.#.
##.#.##.##

Tile 1667:
.#####...#
##....#..#
#..#.#....
..##..#...
#..##...##
...#......
..#..#...#
.....#...#
#..#...#.#
##..#.##..

Tile 3001:
.#.#######
...#.#...#
..##...#.#
#.........
....#.....
#.....##.#
.....####.
#.........
...#.##.##
##.##..###

Tile 1789:
..###.#..#
...##...#.
........#.
####...#.#
#..#..#...
##.##..##.
....#.....
#.#.#.....
#.#..#...#
######.#..

Tile 3677:
.#...#.###
#..##...##
#..#...#.#
##........
..#....###
..........
##..#.##.#
.#........
......##..
.##.##...#

Tile 2693:
#.#.###.#.
#.#..#..#.
.#....#...
#..#...#.#
.#.##..##.
.##......#
...#.....#
##...#.###
.#.#.....#
########..

Tile 2141:
#####.....
#.........
#...#....#
....#.....
.......#..
##..#.#..#
#....#..#.
..#....#..
.....##.#.
##..#.#.#.

Tile 3847:
#...######
#..#.##..#
..#...##.#
##..#.#..#
##..#..#.#
##.##....#
#........#
#....#.#..
#.........
#......#..

Tile 2333:
#.#..##.#.
####.....#
###..#...#
.........#
...##.#..#
###.......
..##...#.#
...###...#
.###.#...#
##..#.##..

Tile 2129:
#..###.###
....#....#
#.#.#..#.#
....#....#
#...#.#..#
..##.##...
#.##....#.
#...#.#...
.#..##...#
...###.##.

Tile 1283:
.#..#.###.
###.#.##.#
#..#..#.#.
.....#...#
.#.#.#....
#...#..#.#
.#.#..#.##
.#..##..#.
#....##.#.
.#..#...#.

Tile 2851:
.##.#.....
###......#
.#........
....#.#..#
.#..#..#..
.##....#..
.##...#.##
#.###.##.#
##........
.#.#.#.#.#

Tile 2311:
#..##....#
.#......#.
....#...##
....#...#.
.#...#...#
#...#....#
.....#.#.#
.....##..#
##..##.###
##..###.#.

Tile 3217:
#.##....##
#.......#.
#.#....#.#
..##.###..
....##...#
#.........
...#.#...#
..##....##
..#......#
##.###..##

Tile 2833:
####..#..#
#...##.#.#
........##
..##..#...
.......#..
......#...
###..#..#.
.##..#...#
##.#....#.
.####.....

Tile 3593:
#..#####..
.##.#....#
...#..#..#
##.#...##.
#######...
...#..#...
#.##..#.#.
#........#
#...##..##
........##

Tile 3299:
...#.#..#.
#.#......#
##......##
.#..#..#..
#.#####...
#...#....#
#.#.......
..#....#.#
.#........
#.#.#.##..

Tile 2719:
...#..#.#.
#..#.###..
......#.##
....#.#..#
#.#......#
....#.....
##..#.#...
...##.....
###.#....#
..####..##

Tile 2161:
..#.##..##
#........#
...#.#...#
...###....
......#..#
..##.##.#.
.#....#.##
#...#####.
#....#...#
.#....#...

Tile 3643:
...#...##.
##......##
....#.###.
.#.#..####
..#.#...##
.##.#.#.#.
#.#..#..#.
#..#.#..#.
.#........
.#.###....

Tile 3767:
.##.#....#
#...#...##
.#...##..#
.#.#......
..#..#..##
#..#.#.##.
#.....#.##
....##...#
.....#.##.
..#..###..

Tile 2377:
.#####.#.#
..#.....##
#...#...#.
##....##..
....#..#..
#.##..#..#
.#...#.##.
...##...#.
#....#....
..#.#..###

Tile 2441:
....#.###.
.#..#....#
.#.###....
#...#.....
#.#.##....
....##....
....##...#
...#..##..
#...###.##
.##.#.#.#.

Tile 2273:
...#..#.#.
#..#...###
..#....#..
...###.#..
.........#
..##.#..##
###.#....#
#..#.....#
....#...#.
.##..#####

Tile 1231:
....#####.
#.....#.#.
..#....#.#
.###..##.#
#..#....##
#..#.#.#..
..#.###...
##........
..#.....##
##.##..#.#

Tile 2879:
#####.###.
#..#..#..#
...#..#..#
#.........
.#.#.#...#
...#..#..#
#.#..#.###
#.....####
.......#.#
..##.#####

Tile 2473:
.##.###..#
....##.#.#
#..#..#..#
..#.#.#...
#..##.....
.##....#..
....##..##
...#.....#
....#.....
.#####.#..

Tile 3329:
#.#..###..
......###.
.###..##..
...#.##...
#..#.#.###
#.###..##.
##..##...#
..#####..#
.#...#....
#.##.#..#.

Tile 1489:
....#....#
#.##.....#
..#......#
..#...#..#
.#....#..#
#..##...#.
..####.##.
.#..##..##
..#.....#.
##.#.##..#

Tile 3259:
..####.###
##.##..#.#
.#..#..###
#.#.......
.....#.#..
##...#.#..
.....#...#
.#....#...
..#.#....#
######....

Tile 1123:
....#.#.#.
...##.....
...##....#
#.##....##
..#...#..#
.#..#.....
.#......##
.........#
.....#...#
.##.###...

Tile 1381:
.###..#.##
#..##..#..
#.....#..#
#..#..#..#
#....#.#.#
.......#.#
#...#.#..#
##..###..#
..#..##...
..##.#..#.

Tile 2903:
#.###.###.
#..###..#.
##.......#
.#....#...
#..#..##.#
...#...#.#
#.#...##.#
......#..#
##.#..#..#
##.#..##.#

Tile 1049:
#....#.###
####.....#
#.##....#.
.#....##..
.##..#..##
#.#.#..#.#
.##...#..#
...#..#.##
.....#..##
..#.#.###.

Tile 3137:
...#.#.#.#
#.#....#..
..###...#.
..#..##..#
.#.#.##.#.
#.#..##..#
#.....#...
##...##.##
#.#...#...
.##.#.....

Tile 2131:
.#......##
...#...##.
.#.#.#.#.#
..........
...#....#.
#.#.#..#.#
..#.#....#
....##....
....##..#.
##.##..#..

Tile 3733:
.#.#....##
.#..#....#
..###.#..#
.....#...#
...#.....#
###..#....
#...#.####
......#...
..#..#....
.#####.#..

Tile 1973:
.#.#.##...
#.....#..#
#......#..
...#...#.#
..#..#...#
####.#....
....#..#.#
.#.....#.#
....#..#.#
..#..#.#..

Tile 3889:
#.##.#...#
#....##..#
.###..#.##
..#...###.
#....##...
#.##......
#.#..#..#.
...#.#...#
........##
##.#..#.#.

Tile 1129:
#...######
#...#.##.#
###.....#.
#.#..#..#.
.#....#...
..#...#..#
#....#.###
......#.#.
#.#..##.##
.###..#..#

Tile 1549:
.#..##.#..
#.#....###
...#..#...
##....#...
..##...#.#
#.#....###
..#.##.##.
.....#...#
#.##.....#
#..#.##...

Tile 2213:
#...#.#.##
#........#
...##...##
.#..##.#.#
#..##....#
...##...##
##........
....#....#
...#.#.#.#
..#.###..#

Tile 1597:
..###..#..
#......#..
.......#.#
#.#....###
#.###..#.#
##.#.##...
#.##.#..##
.#.#..##..
.##..#...#
##...#####

Tile 1777:
#..#....#.
.........#
..#.....#.
..#......#
.##....#..
#...#...#.
.#..#.....
#.....#..#
.#..##...#
#.#...#...

Tile 2503:
#..###.#..
.#..##.#..
....##....
..#..#....
#....#.#..
#.#....#.#
...#.#....
..##.#....
#.#.#....#
#.######..

Tile 3499:
.####...##
.#.##..#..
#........#
..#......#
##..#...#.
#...##....
#......#..
.#.#....##
...#..#...
.##.#...#.

Tile 1811:
#.###...##
..##...#..
..#.#..###
##.#....#.
.#...#....
##.......#
#....#...#
...##.##..
...#.....#
.####..#..

Tile 3793:
###.####..
##...###.#
...#.###..
#....#....
.....#....
...#.....#
###.####..
#.##.##.##
......#...
#.#.###...

Tile 2341:
.##..#.###
.#........
..####..#.
.#..####.#
#....#...#
......##.#
#.....#...
..........
#..###....
####.#####

Tile 3613:
..#.#.#.#.
#....###..
#......#..
#.#...#.##
#..#.....#
##.#.#.#..
...####..#
##...###.#
#.#.#....#
#..####...

Tile 3701:
..##.####.
#.##...###
.###.#....
#..#.....#
##........
###..#.###
..#...#.#.
.##...#..#
##.......#
###.#...##

Tile 1483:
#####..##.
....#..#.#
...#####.#
#.##...#..
........#.
........##
##..##.###
.###....##
...###..#.
...#.#..#.

Tile 3571:
#.#.##.##.
#......##.
#...#.#...
.#.#....#.
#.#....#..
#.#...#...
##.....#.#
##.#.#...#
#....#...#
#.#..#..##

Tile 2521:
##.##..#.#
......#..#
.#.#.#.##.
#........#
.#.##....#
.#....#.#.
##......#.
#....#....
.#..#...#.
.#..#..###

Tile 3413:
.##.##..#.
#...#..#..
##....#..#
..........
#..#...#..
##..#....#
....#.#...
#.....#...
......#.##
..##.##.#.

Tile 1933:
#..#....##
#...#..###
.#......##
......#..#
..........
##.##..###
.......###
...#...###
.#....#..#
#.#..#.#.#

Tile 1021:
.#..##.#.#
##....#...
.#........
.#.#....##
.#......##
##........
.....#..#.
#....#.#.#
#.........
..#.#.##.#

Tile 3323:
...###.#..
.#..####..
....#.....
#.....##.#
###......#
..########
.#....##.#
....##.##.
#..##....#
#.##.#..#.

Tile 1607:
....####..
##.#...#.#
.......#.#
#.........
..#..####.
..#..#.##.
.###.#...#
##...#....
#.######..
##.#.#.###

Tile 1481:
.###...#..
.#......##
.....#...#
...#...##.
#.###.##..
#......###
#.........
###...###.
.#....##..
#....###.#

Tile 1879:
###.##....
#.#.....##
#.#..#.#.#
.#...#..##
......####
#.###.....
......###.
#..#.#..##
..#......#
.#..#.....

Tile 2927:
###..##.#.
#..#....#.
##..#.....
#.#...####
#.........
..###...##
#.####...#
#.##.##..#
...#......
#....#.##.

Tile 1867:
..#..####.
##.##..#.#
.##......#
###..#....
..#......#
#..##..#.#
#.........
...#..#..#
#......#..
.#....#.#.

Tile 2647:
#####.##.#
...#...#..
#.......##
...#..#..#
..#.###...
...##.....
..#......#
.##.......
#...#.....
##...##.#.

Tile 2207:
#.#####.#.
#..#.#..##
...##....#
..#..#.#.#
#...###..#
.##.#...##
#..##..###
#.........
###.#..#.#
.#....##.#

Tile 1223:
###.....#.
#.....#.##
##.##.#...
#...##...#
#....#....
..#.##....
##....##..
..#..#....
.#.##..#..
###.#.####

Tile 1931:
##.#...###
#...##....
#..#....#.
..##..#...
#...#.....
.........#
###.##....
...##.#..#
.#.#.....#
..#..##.##

Tile 3917:
.##.#..#..
.......##.
#.##....##
...#....##
###....#.#
.##.#...##
###.......
##.....#..
....###.##
....#...#.

Tile 1663:
#.#.....##
.#.##.#..#
....#...#.
#...##...#
#..#......
.#..#.#..#
..#..#..##
...#......
#...##....
.##.######

Tile 3373:
#..###.###
##...#.#..
#..#..#..#
.#....##.#
..###..##.
...#.#...#
#.....#..#
##..#.....
.#..#.#...
.#...###.#

Tile 1319:
.#.#.#.#.#
.....#..##
..#.#.#.#.
.#.##...#.
..##......
...#......
.#........
#..#.....#
#..##....#
.#.##.#..#

Tile 2687:
#...###.#.
##.#...##.
#...#...##
#..##....#
......#.#.
.###.#.#..
##...#..##
......#..#
..........
#.....##.#

Tile 2003:
.######...
.##...###.
....#.....
#.###.#.#.
......#..#
..##.#.#.#
#.##..#.#.
####.#....
#...#.#.##
......##.#

Tile 1453:
###.#.####
...###..#.
.#..#..###
..#......#
#.#..#..##
..#..#.#..
#.#...#.#.
..##..#.#.
#..###....
..#..#..##

Tile 1871:
..#..#####
##..#....#
##.......#
#..#..#..#
#.....#.#.
#..###....
..........
.#........
.#.##.##.#
#.#..#.###

Tile 3709:
.##.#.##..
.#..##...#
.##.......
..##.#....
.........#
....#.....
###.#.##..
.#####....
#####.#...
..#..#####
⛄"""