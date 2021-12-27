#!/usr/bin/env python3


# HELPER FUNCTIONS
import math
from functools import cache


def parser(text) -> list:
    return [int(s) for s in text.strip().split("\n")]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
@cache
def public_key(subject_num: int, loop_size: int) -> int:
    res = 1
    for _ in range(loop_size):
        res *= subject_num
        res %= 20201227
    return res


def divisors(n):
    divs = [1]
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.extend([i, n // i])
    divs.extend([n])
    return list(sorted(set(divs)))


def get_creds(key) -> tuple:
    divs = divisors(key)[1:-1]
    for x in divs:
        y, switcher = 1, 0
        while y < key:
            public_ = public_key(x, y)
            if public_ == key:
                return x,y
            if public_ > key:
                pass

    return - 1, -1


def part1(keys: list) -> int:
    assert len(keys) == 2
    key1, key2 = keys[0], keys[1]
    subject_num1, loop_size1 = get_creds(key1)
    subject_num2, loop_size2 = get_creds(key2)
    encryption = public_key(key1, loop_size2)
    assert public_key(key2, loop_size1) == encryption
    return encryption


# TEST
def test() -> bool:
    given = parser("5764801")
    assert given == [5764801]
    assert public_key(7, 8) == 5764801
    assert public_key(7, 11) == 17807724
    assert public_key(17807724, 8) == 14897079
    assert public_key(5764801, 11) == 14897079
    print(f"divisors of 5764801={divisors(5764801)}")
    print(f"divisors of 17807724={divisors(17807724)}")
    d = {}
    for i in range(1, 12):
        for j in range(1, 12):
            public_ = public_key(i, j)
            d[public_] = (i, j)
            if public_ in (5764801, 17807724):
                print("Bingo")
            # print(f"public_key({i},{j})={public_}")
    print({k: d[k] for k in sorted(d)})
    assert part1(parser("5764801\n17807724")) == 14897079
    return True


if __name__ == '__main__':
    assert test()

    input = parser(read_input())
    # ONE #1
    part_1 = part1(input)
    print(part_1)
    # assert part_1 == 74698532
    # # TWO #2
    # part_2 = part2(input)
    # print(part_2)
    # assert part_2 == 286194102744

# INPUT
"""🎅
8458505
16050997
⛄"""
