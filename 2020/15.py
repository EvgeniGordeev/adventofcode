#!/usr/bin/env python3

# HELPER FUNCTIONS


def parser(text) -> list:
    return [int(i) for i in text.split(',')]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
def part1(nums: list, end: int = 2020) -> int:
    size, memo = len(nums), dict()

    debug_sequence = []
    for i, n in enumerate(nums):
        # times spoken, last, before
        memo[n] = [1, i, i]
        debug_sequence.append(n)
    last = nums[-1]
    for i in range(size, end):
        if last not in memo:
            memo[last] = [1, i - 1, i - 1]
            spoken = 0
        elif memo[last][0] == 1:
            memo[last][0] = 2
            spoken = 0
        else:
            spoken = memo[last][1] - memo[last][2]
            memo[last][2] = i - 1
        if spoken in memo:
            memo[spoken][0] += 1
            memo[spoken][1] = i
        last = spoken
    #     debug_sequence.append(spoken)
    #     if i > 1_000_000 and i % 1_000_000 == 0:
    #         print(f"Running for {i}th time, {'{:.1%}'.format(i / end)} completed")
    # print(debug_sequence)
    return last


# TEST
def test():
    # GIVEN
    given = parser("""
0,3,6
""")
    assert part1(given, 2020) == 436
    assert part1([1, 3, 2], 2020) == 1
    assert part1([2, 1, 3], 2020) == 10
    assert part1([2, 3, 1], 2020) == 78
    assert part1([3, 2, 1], 2020) == 438
    assert part1([3, 1, 2], 2020) == 1836
    # part 2
    # assert part1([0, 3, 6], 30000000) == 175594

    return True


if __name__ == '__main__':
    assert test()
    exit(0)
    nums = parser(read_input())
    # ONE #1
    part_1 = part1(nums)
    print(part_1)
    assert part_1 == 234
    # # TWO #2
    part_2 = part1(nums, 30000000)
    print(part_2)
    # assert part_2 == 3443997590975

# INPUT
"""🎅
0,13,1,16,6,17
⛄"""
