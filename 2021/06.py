#!/usr/bin/env python3

# HELPER FUNCTIONS
from functools import lru_cache


def parser(text) -> list:
    return list(map(int, text.strip().split(',')))


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN FUNCTIONS
@lru_cache(maxsize=None)
def count_fish(fish: tuple, days: int):
    """
    divide-and-conquer days and list
    """
    if len(fish) == 1:
        school = list(fish)
        batch = 8
        for d in range(days):
            new_school, new_fish = [], []
            for f in school:
                if f == 0:
                    new_school.append(6)
                    new_fish.append(8)
                else:
                    new_school.append(f - 1)
            school = new_school + new_fish
            if d != 0 and d % batch == 0:
                ans = len(school)
                for f in school:
                    ans += count_fish((f,), days - d - 1) - 1
                return ans
        return len(school)
    else:
        middle = len(fish) // 2
        return count_fish(fish[:middle], days) + count_fish(fish[middle:], days)


def part1(fish: list, days=80) -> int:
    return count_fish(tuple(fish), days)


def part2(fish: list, days: int) -> int:
    return part1(fish, days)


# TEST
def test():
    # GIVEN
    given = parser("3,4,3,1,2")
    assert part1(given, 18) == 26
    assert part1(given) == 5934
    # part 2
    assert part1([1], 32) == 21
    assert part1([1], 34) == 27
    assert part1([1], 128) == 90763
    assert part2([1], 32) == 21
    assert part2([1], 34) == 27
    assert part2([1], 128) == 90763

    assert part2(given, 18) == 26
    assert part2(given, 80) == 5934
    assert part2(given, 256) == 26984457539

    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    part_1 = part2(input_, 80)
    print(part_1)
    assert part_1 == 343441
    # TWO #2
    part_2 = part2(input_, 256)
    print(part_2)
    assert part_2 == 1569108373832

# INPUT
"""🎅
3,5,2,5,4,3,2,2,3,5,2,3,2,2,2,2,3,5,3,5,5,2,2,3,4,2,3,5,5,3,3,5,2,4,5,4,3,5,3,2,5,4,1,1,1,5,1,4,1,4,3,5,2,3,2,2,2,5,2,1,2,2,2,2,3,4,5,2,5,4,1,3,1,5,5,5,3,5,3,1,5,4,2,5,3,3,5,5,5,3,2,2,1,1,3,2,1,2,2,4,3,4,1,3,4,1,2,2,4,1,3,1,4,3,3,1,2,3,1,3,4,1,1,2,5,1,2,1,2,4,1,3,2,1,1,2,4,3,5,1,3,2,1,3,2,3,4,5,5,4,1,3,4,1,2,3,5,2,3,5,2,1,1,5,5,4,4,4,5,3,3,2,5,4,4,1,5,1,5,5,5,2,2,1,2,4,5,1,2,1,4,5,4,2,4,3,2,5,2,2,1,4,3,5,4,2,1,1,5,1,4,5,1,2,5,5,1,4,1,1,4,5,2,5,3,1,4,5,2,1,3,1,3,3,5,5,1,4,1,3,2,2,3,5,4,3,2,5,1,1,1,2,2,5,3,4,2,1,3,2,5,3,2,2,3,5,2,1,4,5,4,4,5,5,3,3,5,4,5,5,4,3,5,3,5,3,1,3,2,2,1,4,4,5,2,2,4,2,1,4
⛄"""
