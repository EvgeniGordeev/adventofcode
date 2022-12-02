#!/usr/bin/env python3
from typing import List


def parser(text) -> list:
    return [line.strip() for line in text.split('\n')]


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN FUNCTIONS
def part1(given: List[str]) -> int:
    def wrapping_paper(prism):
        # we don't care what dimension is length, width or height
        l, w, h = sorted(prism)
        return 2 * l * w + 2 * w * h + 2 * h * l + l * w

    return sum(wrapping_paper(map(int, gift.split('x'))) for gift in given)


def part2(given: List[str]) -> int:
    def ribbon_and_bow(prism):
        # we don't care what dimension is length, width or height
        l, w, h = sorted(prism)
        return 2 * (l + w) + l * w * h

    return sum(ribbon_and_bow(map(int, gift.split('x'))) for gift in given)


# TEST
def test():
    # GIVEN
    assert part1(["2x3x4"]) == 58
    # assert part1(["1x1x10"]) == 43
    # part 2
    # assert part2(["2x3x4"]) == 34
    # assert part2(["1x1x10"]) == 14

    return True


if __name__ == '__main__':
    assert test()
    given = parser(read_input())
    # ONE #1
    # part_1 = part1(given)
    # print(part_1)
    # assert part_1 == 1598415
    # # TWO #2
    # part_2 = part2(given)
    # print(part_2)
    # assert part_2 == 3812909

# INPUT
"""🎅

⛄"""
