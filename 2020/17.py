#!/usr/bin/env python3

# HELPER FUNCTIONS


def parser(text) -> set:
    data = text.strip().split('\n')
    slice_1d = set()
    for r, l in enumerate(data):
        for c, p in enumerate(l):
            if p == '#':
                slice_1d.add((r, c, 0))
    return slice_1d


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
DIRS = [(z, y, x)
        for x in range(-1, 2)
        for y in range(-1, 2)
        for z in range(-1, 2)
        if not (z == 0 and y == 0 and x == 0)]


def part1(active, cycles=6):
    for _ in range(cycles):
        new = set()
        xs, ys, zs = list(zip(*active))

        for x in range(min(xs) - 1, max(xs) + 2):
            for y in range(min(ys) - 1, max(ys) + 2):
                for z in range(min(zs) - 1, max(zs) + 2):
                    neighbors = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                if dx != 0 or dy != 0 or dz != 0:
                                    if (x + dx, y + dy, z + dz) in active:
                                        neighbors += 1

                    if (x, y, z) not in active and neighbors == 3:
                        new.add((x, y, z))
                    if (x, y, z) in active and neighbors in [2, 3]:
                        new.add((x, y, z))

        active = new

    return len(active)


def part2(active, cycles=6):
    for _ in range(cycles):
        new = set()
        xs, ys, zs, ws = list(zip(*active))

        for x in range(min(xs) - 1, max(xs) + 2):
            for y in range(min(ys) - 1, max(ys) + 2):
                for z in range(min(zs) - 1, max(zs) + 2):
                    for w in range(min(ws) - 1, max(ws) + 2):
                        neighbors = 0
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                for dz in [-1, 0, 1]:
                                    for dw in [-1, 0, 1]:
                                        if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                                            if (x + dx, y + dy, z + dz, w + dw) in active:
                                                neighbors += 1

                        if (x, y, z, w) not in active and neighbors == 3:
                            new.add((x, y, z, w))
                        if (x, y, z, w) in active and neighbors in [2, 3]:
                            new.add((x, y, z, w))

        active = new

    return len(active)


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
    assert part1(given) == 112
    given_4d = list(p + (0,) for p in given)
    assert part2(given_4d, 1) == 29
    assert part2(given_4d) == 848
    return True


if __name__ == '__main__':
    assert test()

    model = parser(read_input())
    # ONE #1
    ans_1 = part1(model)
    print(ans_1)
    assert ans_1 == 232
    # # TWO #2
    model_4d = list(p + (0,) for p in model)

    part_2 = part2(model_4d)
    print(part_2)
    assert part_2 == 1620

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
