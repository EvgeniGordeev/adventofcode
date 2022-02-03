#!/usr/bin/env python3


import math
import sys
from collections import namedtuple
from functools import reduce


# HELPER FUNCTIONS
def parser(text) -> list:
    return [l for l in text.strip().split("\n")]


def read_input() -> list:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return parser(data)


# SANDBOX
def part2_brute_force(bus_ids):
    """
    works for smaller input like in test(), but not for a bigger one
    """
    buses = [int(s) for s in bus_ids.split(',') if s != 'x']
    constraint = [i for i, s in enumerate(bus_ids.split(',')) if s != 'x']

    first = buses.pop(0)
    del constraint[0]
    # using step bus as the step in the sequence - no need to verify the constraint
    assert len(buses) == len(constraint)
    size = len(buses)
    earliest = first

    step, valid, limit = earliest, 0, sys.maxsize

    while earliest < limit:
        valid = 0
        for j in range(size):
            if abs(earliest % buses[j] - buses[j]) != constraint[j]:
                break
            valid += 1
        if valid == size:
            return earliest
        earliest += step

    raise ValueError("earliest timestamp not found")


def establish_range_pattern(a, b, rule) -> tuple:
    """
    Establish pattern ranges, e.g.:
    tuple(a_sequence, b_sequence, a_index, b_index)
    1)  a=17, b=13, rule=2
    [(102, 104, 5, 7), (323, 325, 18, 24), (544, 546, 31, 41)]
    2)  a=17, b=19, rule=3
    [(187, 190, 10, 9), (510, 513, 29, 26), (833, 836, 48, 43)]
    Range for 1 - range(5, inf, 13)
    Range for 2 - range(10, inf, 19)
    Common Rule is range(first_intersection, inf, b)
    So this
    """
    print(f"a={a}, b={b}, diff={rule}")

    lcm = _lcm(a, b)
    l1 = range(a, lcm + rule + 1, a)
    l2 = range(b, lcm + rule + 1, b)
    i, j, n = 0, 0, max(len(l1), len(l2))

    debug = 0
    while i < n and j < n:
        diff = l2[j] - l1[i]

        if diff == rule:

            debug += 1
            if debug == 1:
                print(f"range({l1[i]}, sys.maxsize, {lcm})")
            print(f"({l1[i]}, {l2[j]}, {i}, {j})")
            if debug == 5:
                break
            return l1[i], lcm
        if diff > rule:
            i += 1
        else:
            j += 1
    return -1, -1


# MAIN FUNCTIONS
def part1(timestamp, bus_ids):
    ts = int(timestamp)
    buses = [int(s) for s in bus_ids.split(',') if s != 'x']
    next_departures = [ts - ts % bus + bus for bus in buses]
    closest = min(next_departures)
    return buses[next_departures.index(closest)] * (closest - ts)


Schedule = namedtuple('Schedule', 'start interval diff')


def _lcm(*nums):
    return reduce(lambda a, b: a * b // math.gcd(a, b), nums)


def _find_intersection(s1: Schedule, s2: Schedule) -> Schedule:
    lcm = _lcm(s1.interval, s2.interval)
    rule = s2.diff - s1.diff
    r1 = range(s1.start, lcm + rule + 1, s1.interval)
    r2 = range(s2.start, lcm + rule + 1, s2.interval)

    i1, i2, n1, n2 = 0, 0, len(r1), len(r2)

    # debug = 0
    while i1 < n1 and i2 < n2:
        diff = r2[i2] - r1[i1]
        if diff == rule:
            return Schedule(r1[i1], lcm, 0)
        if diff > rule:
            increment = abs(diff // r1.step) or 1
            i1 += increment
        else:
            increment = abs(diff // r2.step) or 1
            i2 += increment
    return Schedule(0, 1, 0)


def part2(lines):
    buses = [int(s) for s in lines.split(',') if s != 'x']
    constraint = [i for i, s in enumerate(lines.split(',')) if s != 'x']

    schedules = [Schedule(0, buses[i], constraint[i]) for i in range(len(buses))]
    # using step bus as the step in the sequence - no need to verify the constraint
    assert len(schedules) == len(constraint)
    combined = schedules[0]
    for s in schedules[1:]:
        combined = _find_intersection(combined, s)

    return combined.start


# TEST
def test():
    # GIVEN
    given = parser("""
939
7,13,x,x,59,x,31,19
""")
    # WHEN
    minutes_to_wait = part1(given[0], given[1])
    # THEN
    assert minutes_to_wait == 295
    # test 2
    # establish_range_pattern(17, 13, 2)
    # establish_range_pattern(17, 19, 3)
    assert part2_brute_force('12,x,x,13,11') == 348
    assert part2('12,x,x,13,11') == 348
    assert part2_brute_force('17,7,10') == 748
    assert part2('17,7,10') == 748
    assert part2_brute_force('11,x,9,7') == 88
    assert part2('11,x,9,7') == 88
    assert part2_brute_force('18,x,x,x,x,x,17,x,x,x,13,11') == 198
    assert part2('18,x,x,x,x,x,17,x,x,x,13,11') == 198
    assert part2('11,x,9,7') == 88
    assert part2_brute_force('67,7,59,61') == 754018
    assert part2_brute_force('17,x,13,19') == 3417
    assert part2('17,x,13,19') == 3417
    assert part2('67,7,59,61') == 754018
    assert part2('67,x,7,59,61') == 779210
    assert part2('67,7,x,59,61') == 1261476
    assert part2('1789,37,47,1889') == 1202161486
    assert part2(given[1]) == 1068781
    return True


if __name__ == '__main__':
    assert test()

    lines = read_input()
    time_stamp = lines[0]
    bus_ids = lines[1]
    # ONE #1
    part_1 = part1(time_stamp, bus_ids)
    print(part_1)
    assert part_1 == 136
    # TWO #2
    part_2 = part2(bus_ids)
    print(part_2)
    assert part_2 == 305068317272992

# INPUT
"""🎅
1000340
13,x,x,x,x,x,x,37,x,x,x,x,x,401,x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,x,x,x,19,x,x,x,23,x,x,x,x,x,29,x,613,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41
⛄"""
