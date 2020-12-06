#!/usr/bin/env python3
from collections import namedtuple


# HELPER FUNCTIONS
def splitter(text) -> list:
    return [l for l in text.strip().split("\n")]


def read_data() -> list:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return splitter(data)


# SANDBOX
def parse_naive(boarding_pass: str) -> tuple:
    """
    original approach for better visibility
    """
    assert len(boarding_pass) == 10

    lower, upper = 0, 127  # row range
    row = 0
    for direction in boarding_pass[0:7]:
        if direction == 'F':
            row = upper = (lower + upper) // 2
        if direction == 'B':
            row = lower = (lower + upper + 1) // 2

    lower, upper = 0, 7  # column range
    col = 0
    for direction in boarding_pass[7:]:
        if direction == 'L':
            col = upper = (lower + upper) // 2
        if direction == 'R':
            col = lower = (lower + upper + 1) // 2

    return row, col


# MAIN FUNCTIONS
def parse(boarding_pass: str) -> int:
    assert len(boarding_pass) == 10

    row = int(boarding_pass[0:7].replace('F', '0').replace('B', '1'), 2)
    col = int(boarding_pass[7:].replace('L', '0').replace('R', '1'), 2)

    return row * 8 + col


def find_missing(seats: list) -> int:
    # sort to find the available seat
    _seats = sorted(seats)

    missing = _seats[0]
    for seat in _seats:
        if missing != seat:
            return missing
        missing += 1

    return -1


# TEST
def test():
    Seat = namedtuple('Seat', ['row', 'column'])

    def get_row_col(seat_id: int) -> tuple:
        return Seat(seat_id // 8, seat_id % 8)

    # GIVEN
    given = """
FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
    """
    # WHEN
    actual = [get_row_col(parse(s)) for s in splitter(given)]
    # THEN
    expected = [(44, 5), (70, 7), (14, 7), (102, 4)]
    assert actual == expected


if __name__ == '__main__':
    test()
    lines = read_data()
    seats = [parse(p) for p in lines]

    part_1 = max(seats)
    print(part_1)
    assert part_1 == 858

    part_2 = find_missing(seats)
    print(part_2)
    assert part_2 == 557

# INPUT
"""🎅
FBBFFBBLLL
⛄"""
