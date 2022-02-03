#!/usr/bin/env python3


# HELPER FUNCTIONS
from collections import namedtuple
from math import cos, radians, sin
from typing import Callable


def splitter(text) -> list:
    return [l for l in text.strip().split("\n")]


def read_data() -> list:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return splitter(data)


# MAIN FUNCTIONS
# dir=0 means facing N, 90 - E, 180 - S, 270 - W
Position = namedtuple('Position', ['x', 'y', 'dir'])

DIRECTIONS = {
    0: 'N',
    90: 'E',
    180: 'S',
    270: 'W'
}

MOVES = {
    'N': lambda p, val: Position(p.x, p.y + val, p.dir),
    'S': lambda p, val: Position(p.x, p.y - val, p.dir),
    'E': lambda p, val: Position(p.x + val, p.y, p.dir),
    'W': lambda p, val: Position(p.x - val, p.y, p.dir),
    'L': lambda p, val: Position(p.x, p.y, (p.dir - val) % 360),
    'R': lambda p, val: Position(p.x, p.y, (p.dir + val) % 360),
    'F': lambda p, val: _forward(p, val),
}


def _move1(p: Position, op: str, val: int) -> Position:
    return MOVES[op](p, val)


def _rotate(point: Position, center: Position, degrees: int, clockwise: bool = True) -> Position:
    """
    Rotate a point around a given center.
    """
    angle_r = radians(degrees)
    x, y = point.x, point.y
    ox, oy = center.x, center.y
    direction = 1 if clockwise else -1

    qx = ox + cos(angle_r) * (x - ox) + direction * sin(angle_r) * (y - oy)
    qy = oy + - direction * sin(angle_r) * (x - ox) + cos(angle_r) * (y - oy)

    return Position(int(qx), int(qy), point[2])


def _move2(p: Position, op: str, val: int) -> Position:
    """
    Part 2 - we don't care about p.dir, so let's use the third position in the tuple for storing waypoint
    """
    start, finish = p, None
    # convert to wp
    if type(p[2]) is int:
        start = Position(p.x, p.y, Position(p.x + 10, p.y + 1, None))
    waypoint = start[2]
    if op == 'F':
        finish = Position(start.x + waypoint.x * val, start.y + waypoint.y * val, waypoint)
    elif op in DIRECTIONS.values():
        finish = Position(start.x, start.y, MOVES[op](waypoint, val))
    elif op in ('R', 'L'):
        # remember that waypoint is always relative to the ship, so before rotating we have to convert it to the absolute point
        wp_abs = Position(waypoint.x + start.x, waypoint.y + start.y, None)
        wp_rotated = _rotate(wp_abs, start, val, op == 'R')
        wp_relative = Position(wp_rotated.x - start.x, wp_rotated.y - start.y, None)
        finish = Position(start.x, start.y, wp_relative)
    return finish


def _forward(p: Position, val: int) -> Position:
    return _move1(p, DIRECTIONS[p.dir], val)


def manhattan(p1: tuple, p2: tuple = None) -> int:
    if p2 is None:
        p2 = (0, 0)
    return int(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))


def navigate(instructions: list, navigator: Callable[[Position, str, int], Position]) -> Position:
    # that's a start and a finish
    finish = Position(0, 0, 90)
    for instr in instructions:
        operation, val = instr[0], int(instr[1:])
        finish = navigator(finish, operation, val)

    return finish


def part1(lines):
    return manhattan(navigate(lines, _move1))


def part2(lines):
    return manhattan(navigate(lines, _move2))


# TEST
def test():
    # GIVEN
    given = splitter("""
F10
N3
F7
R90
F11
""")
    # WHEN
    finish = navigate(given, _move1)
    # THEN
    assert finish == Position(17, -8, 180)
    assert manhattan(finish) == 25
    assert part1(given) == 25
    # TEST 2
    # clockwise
    assert Position(0, 2, None) == _rotate(Position(-2, 0, None), Position(0, 0, None), 90, True)
    # counterclockwise
    assert Position(0, -2, None) == _rotate(Position(-2, 0, None), Position(0, 0, None), 90, False)
    finish = navigate(given, _move2)
    assert finish == Position(214, -72, Position(4, -10, None))
    assert part2(given) == 286


if __name__ == '__main__':
    test()
    lines = read_data()
    # ONE #1
    part_1 = part1(lines)
    print(part_1)
    assert part_1 == 757
    # TWO #2
    part_2 = part2(lines)
    print(part_2)
    # assert part_2 == 1995

# INPUT
"""🎅
F40
N1
W1
F95
W2
N5
R90
N3
E3
F21
E3
F44
W3
R90
N2
L180
E5
F99
W1
F11
R90
N4
F45
S5
L180
W1
R180
E5
R90
F5
S4
E3
S4
L180
W5
F26
F1
S3
L180
F79
R90
S5
R90
E5
L180
W4
F12
N5
E4
F31
S5
W2
F93
W2
F8
S2
E5
F100
L90
F10
R90
N1
F15
S3
E4
L90
L180
S3
E5
R90
F13
N4
F15
L90
W4
N4
W1
S5
F44
W4
F68
N2
W4
F58
L90
E5
F81
S5
L90
S1
F95
R90
E3
R180
F81
R90
S3
E3
L180
W4
W3
N1
W5
R270
W3
N4
W3
N4
F47
E3
R90
F86
S4
N1
R180
E2
N1
S5
R90
N4
L90
E3
R180
N1
W1
N3
E5
N2
F9
N4
R90
F36
E2
S1
R90
N2
F76
F88
E5
F78
W4
F53
N1
W1
R90
R180
N4
W5
S1
N2
E3
F83
L90
E3
L90
W2
L90
N1
W2
F21
R90
F58
S3
F100
S5
F78
S5
R90
E5
R90
W5
W1
L90
F23
L90
F56
W3
F8
W2
N5
F39
S5
F84
N4
R90
N4
F18
S4
F50
S1
E3
S5
L90
N2
W2
N1
F86
R90
S1
R90
L90
W2
F100
E4
L180
F100
E1
S5
W2
L90
N4
E4
R90
F94
W5
S5
L180
W5
S5
L90
S3
R180
E2
F22
R90
E4
F65
N1
E5
F82
W3
F100
E1
F87
L90
S4
W1
F10
W3
S2
F9
E2
F49
F35
E1
R90
F6
W4
F60
R90
S1
F45
W4
F44
E3
L90
W2
N3
L90
N2
W1
N2
W2
S4
E4
W5
R90
E4
L90
F16
W5
S3
N5
L90
F83
W4
L90
E2
F25
W3
R270
W3
L90
N5
F36
S4
R90
F15
R90
S2
L90
E5
F25
S3
F2
N4
W1
N2
F6
S3
R90
L90
W2
N2
E5
S3
L90
F31
W4
L90
N4
F30
S3
R90
S3
L180
W4
N4
F72
W3
S1
R90
F60
E4
R180
W4
S1
W4
R90
F10
E3
F58
E5
N2
W5
L180
N1
E1
R90
W5
N1
E3
L90
N2
R90
E2
R180
S1
R90
F91
L90
W4
N3
L270
F52
W2
R90
F92
N4
E5
F46
N2
F36
W3
L90
N5
F60
N1
S3
F94
L180
S1
R270
R180
F26
S1
F23
E5
R90
F27
S3
L90
F8
E5
F5
S1
R90
F99
W3
F47
W3
S3
W1
L180
W3
R180
F41
L180
E2
L180
N5
R90
F17
S2
E2
F2
R90
N2
F53
S4
L90
F87
R180
E1
S4
F43
R90
F45
W4
F7
W5
L90
W4
L90
E3
L90
E3
R90
F14
N1
F23
E4
N1
N1
R90
F98
L180
E5
F92
R180
E4
S2
R270
W3
L180
E1
S5
N3
E5
R90
E3
L90
F21
F84
L90
S5
R90
F68
L180
E3
L90
W4
F18
S4
W5
L90
R180
W1
L180
F88
E3
N3
W3
S3
L90
F69
R180
W4
F98
S3
L90
E2
N2
F26
E2
E1
N2
W5
R90
W1
F13
W4
R180
N2
F25
W4
F89
W4
F76
S5
F73
E1
N3
L90
E4
F97
L180
N2
R180
E1
F88
E3
N5
W2
F62
S3
E5
R180
N1
N3
N4
F3
W2
R180
F28
L90
S4
E1
L90
E4
F63
R90
N2
R90
F22
N3
L90
W4
S1
F67
W5
N4
F44
S4
F64
L180
W3
N2
W1
F63
N3
R90
S5
R90
F20
L180
L270
S1
L90
F66
W5
R90
N1
L180
W4
F94
S3
R180
F18
L90
F29
S3
L90
S4
F74
L90
F85
F35
R90
S4
F68
R90
F44
S2
W4
S2
F27
R90
E5
F30
E1
L90
W4
F39
N3
L90
E1
S4
F87
W2
L90
N3
W1
F51
W1
L180
F24
N2
E1
N2
F4
R90
E3
S1
F69
R90
E4
F31
L90
S3
E3
E5
L90
F75
E4
L90
F14
L90
N1
R90
F36
S4
F49
L90
N5
W3
R90
F35
L180
R180
F26
W3
F16
R90
F90
E3
N3
F87
N5
L180
F4
R90
N1
E4
N5
F93
W1
N4
L90
F35
L90
W1
E3
N5
W5
F5
S1
W1
N1
F61
S1
W2
N1
R90
F26
R90
L90
W4
F12
R90
W1
R90
F18
E1
F14
N3
W3
S2
F25
E5
F89
W5
L90
S4
F38
L180
F98
W3
S1
F77
R270
E2
F95
W1
F56
N4
R180
E3
L270
E1
F6
S3
L180
E5
R180
E1
N2
L180
E4
S3
E2
L180
F72
N4
R90
L90
W4
F82
S3
R270
F32
F39
L90
N5
W1
L90
N3
F95
L180
S5
L90
F46
E1
L90
W2
S5
L90
S5
F77
L90
N4
E3
N1
F39
R90
R90
F40
L90
N4
W1
F7
E4
S5
E5
N1
F96
E4
F10
F8
S5
E5
F26
S4
R90
S2
F61
W4
S4
R90
E2
F39
S5
R90
S4
F83
S5
F18
S3
E5
R180
F7
⛄"""
