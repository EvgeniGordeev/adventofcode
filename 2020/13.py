#!/usr/bin/env python3


# HELPER FUNCTIONS


def splitter(text) -> list:
    return [l for l in text.strip().split("\n")]


def read_data() -> list:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return splitter(data)


# MAIN FUNCTIONS

def part1(lines):
    timestamp = int(lines[0])
    bus_ids = [int(s) for s in lines[1].split(',') if s != 'x']
    next_departures = [timestamp - timestamp % bus + bus for bus in bus_ids]
    closest = min(next_departures)
    return bus_ids[next_departures.index(closest)] * (closest - timestamp)


# TEST
def test():
    # GIVEN
    given = splitter("""
939
7,13,x,x,59,x,31,19
""")
    # WHEN
    minutes_to_wait = part1(given)
    # THEN
    assert minutes_to_wait == 295


if __name__ == '__main__':
    test()
    lines = read_data()
    # # ONE #1
    part_1 = part1(lines)
    print(part_1)
    assert part_1 == 136
    # # TWO #2
    # part_2 = part2(lines)
    # print(part_2)
    # # assert part_2 == 1995

# INPUT
"""🎅
1000340
13,x,x,x,x,x,x,37,x,x,x,x,x,401,x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,x,x,x,19,x,x,x,23,x,x,x,x,x,29,x,613,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41
⛄"""
