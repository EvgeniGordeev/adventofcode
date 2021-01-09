#!/usr/bin/env python3


# HELPER FUNCTIONS
import re
from collections import defaultdict
from functools import cache


def parser(text) -> list:
    return [s for s in text.strip().split("\n")]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# SANDBOX
# https://www.redblobgames.com/grids/hexagons/#coordinates-offset
# “even-q” vertical layout
# shoves even columns down
HEX_GRID_EVEN_Q = """
/ -4,-2 \_____/ -2,-2 \_____/  0,-2 \_____/  2,-2 \_____/  4,-2 \ 
\       /     \       /     \       /     \       /     \       / 
 \_____/ -3,-1 \_____/ -1,-1 \_____/  1,-1 \_____/  3,-1 \_____/  
 /     \       /     \       /     \       /     \       /     \  
/ -4,-1 \_____/ -2,-1 \_____/  0,-1 \_____/  2,-1 \_____/  4,-1 \ 
\       /     \       /     \   nw  /     \       /     \       / 
 \_____/ -3,0  \_____/ -1,0  \_____/  1,0  \_____/  3,0  \_____/  
 /     \   w   /     \   w   /     \   ne  /     \       /     \  
/ -4,0  \_____/ -2,0  \_____/  0,0  \_____/  2,0  \_____/  4,0  \ 
\       /     \       /     \       /     \       /     \       / 
 \_____/ -3,1  \_____/ -1,1  \_____/  1,1  \_____/  3,1  \_____/  
 /     \   sw  /     \   sw  /     \   e   /     \       /     \  
/ -4,1  \_____/ -2,1  \_____/  0,1  \_____/  2,1  \_____/  4,1  \ 
\       /     \       /     \   se  /     \       /     \       / 
 \_____/ -3,2  \_____/ -1,2  \_____/  1,2  \_____/  3,2  \_____/  
 /     \       /     \       /     \       /     \       /     \  
/ -4,2  \_____/ -2,2  \_____/  0,2  \_____/  2,2  \_____/  4,2  \ 
 """

HEX_GRID_ODD_Q = """
 \_____/ -1,-3 \_____/  1,-3 \  
 /     \       /     \       /  
/ -2,-2 \_____/  0,-2 \_____/   
\       /     \       /     \   
 \_____/ -1,-2 \_____/  1,-2 \  
 /     \       /     \       /  
/ -2,-1 \_____/  0,-1 \_____/   
\       /     \   nw  /     \   
 \_____/ -1,-1 \_____/  1,-1 \  
 /     \   w   /     \   ne  /  
/  -2,0 \_____/  0,0  \_____/   
\       /     \       /     \   
 \_____/  -1,0 \_____/  1,0  \  
 /     \   sw  /     \   e   /  
/  -2,1 \_____/  0,1  \_____/   
\       /     \   se  /     \   
 \_____/  -1,1 \_____/  1,1  \ 
"""


def print_hex_grid(pattern: dict, range_x: range, range_y: range):
    hex_ = """
  _____       
 /     \      
/(x1,y1)\_____
\       /     
 \_____/(x2,y2)
""".split("\n")
    hex_ = [l for l in hex_ if l.strip()]
    # points are sorted by y ascending
    floor = [(x, y) for y in range_y for x in range_x]
    rows = floor[-1][1] - floor[0][1] + 1
    cols = len(floor) // rows
    points_by_rows = [list(zip(floor[start:end:2], floor[start + 1:end:2])) for r in range(0, rows)
                      # just using walrus
                      if (start := r * cols) < (end := (r + 1) * cols)]
    pattern = defaultdict(int, {k: pattern[k] for k in sorted(pattern, key=lambda tile: tile[1]) if pattern[k] == 1})
    str_list, r_size = [], len(points_by_rows[0])
    for r_i, r in enumerate(points_by_rows):
        l_start = 0 if r_i == 0 else 1
        for line in range(l_start, len(hex_)):
            print_line = ""
            for c_i, cell in enumerate(r):
                h_start = 1 if line == 4 and c_i != 0 else 0
                start = hex_[line][h_start:]
                start = start.replace("(x1,y1)", f"{cell[0][0]},{cell[0][1]}"[:7].center(7)) \
                    .replace("(x2,y2)", f"{cell[1][0]},{cell[1][1]}"[:7].center(7))
                if line == 1 and pattern[cell[0]] == 1:
                    start = start.replace("/     \\", "/*****\\")
                elif line == 3 and pattern[cell[1]] == 1:
                    start = start.replace("/     ", "/*****")
                print_line += start
                finish = ""
                if c_i == r_size - 1 and line > 0:
                    finish = "\\" if line in (3, 4) else " /" if line == 1 else "/"
                print_line += finish

            str_list.append(print_line)
    print("\n".join(str_list))


# MAIN FUNCTIONS
DIRS = "e, se, sw, w, nw, ne".split(", ")

HEX_COORDS_EVEN_Q = {
    'e': lambda x, y: (x + 1, y + abs((x + 1) % 2)),
    'se': lambda x, y: (x, y + 1),
    'sw': lambda x, y: (x - 1, y + abs((x + 1) % 2)),
    'w': lambda x, y: (x - 1, y - abs(x % 2)),
    'nw': lambda x, y: (x, y - 1),
    'ne': lambda x, y: (x + 1, y - abs(x % 2))
}

HEX_COORDS_ODD_Q = {
    'e': lambda x, y: (x + 1, y + abs(x % 2)),
    'se': lambda x, y: (x, y + 1),
    'sw': lambda x, y: (x - 1, y + abs(x % 2)),
    'w': lambda x, y: (x - 1, y - abs((x + 1) % 2)),
    'nw': lambda x, y: (x, y - 1),
    'ne': lambda x, y: (x + 1, y - abs((x + 1) % 2))
}

regex = re.compile(f"{'|'.join(DIRS)}")


def hex_move(origin: tuple, _dir: str) -> tuple:
    return HEX_COORDS_EVEN_Q[_dir](*origin)


def hex_move_odd_q(origin: tuple, _dir: str) -> tuple:
    return HEX_COORDS_ODD_Q[_dir](*origin)


def to_hex_coord(tile: str) -> tuple:
    moves = regex.findall(tile)
    _from = (0, 0)
    for m in moves:
        to = hex_move(_from, m)
        _from = to
    return _from


def flip(tiles):
    flipped = defaultdict(int)
    for t in tiles:
        xy = to_hex_coord(t)
        flipped[xy] ^= 1
    return flipped


def part1(tiles: list) -> int:
    flipped = flip(tiles)
    return sum(flipped.values())


@cache
def neighbors_even_q(tile: tuple) -> list:
    return [hex_move(tile, k) for k in HEX_COORDS_EVEN_Q]


@cache
def neighbors_odd_q(tile: tuple) -> list:
    return [hex_move_odd_q(tile, k) for k in HEX_COORDS_ODD_Q]


def part2(tiles: list, days=100) -> int:
    pattern = flip(tiles)
    for _ in range(days):
        # print(f"Day {_}\n\n")
        pattern, range_x, range_y = expand_area(pattern)
        new_day = defaultdict(int)
        for y in range_y:
            for x in range_x:
                tile = (x, y)
                color = pattern[tile]
                new_day[tile] = color
                counter = sum(pattern[nbr] for nbr in neighbors_even_q(tile))
                if color == 1 and counter == 0 or counter > 2:
                    new_day[tile] = 0
                if color == 0 and counter == 2:
                    new_day[tile] = 1
        pattern = new_day

    return sum(pattern.values())


def expand_area(pattern):
    """
    expand visible area
    """
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for x, y in pattern.keys():
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        elif y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y
    # take care of odd/even min_x left top cell x, odd - is even-q, even - is odd-q
    min_x, min_y, max_x, max_y = min_x - (1 if min_x % 2 else 2), min_y - 1, max_x + 2, max_y + 2,
    # print_hex_grid(pattern, range(min_x, max_x), range(min_y, max_y))
    return pattern, range(min_x, max_x), range(min_y, max_y)


# TEST
def test() -> bool:
    assert hex_move((3, -1), "ne") == (4, -2)
    assert hex_move((-2, 1), "ne") == (-1, 1)
    assert flip(parser("nwwswee")) == {(0, 0): 1}
    assert flip(parser("esew")) == {(0, 1): 1}
    given = parser("""
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""")
    assert part1(given) == 10
    # part 2
    assert neighbors_even_q((0, 0)) == [(1, 1), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, 0)]
    assert neighbors_odd_q((0, 0)) == [(1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    assert neighbors_even_q((3, -1)) == [(4, -1), (3, 0), (2, -1), (2, -2), (3, -2), (4, -2)]
    assert neighbors_even_q((-3, -1)) == [(-2, -1), (-3, 0), (-4, -1), (-4, -2), (-3, -2), (-2, -2)]
    assert neighbors_odd_q((1, -1)) == [(2, 0), (1, 0), (0, 0), (0, -1), (1, -2), (2, -1)]
    assert neighbors_odd_q((-2, 2)) == [(-1, 2), (-2, 3), (-3, 2), (-3, 1), (-2, 1), (-1, 1)]
    assert part2(given, 1) == 15
    assert part2(given, 2) == 12
    assert part2(given, 3) == 25
    assert part2(given, 4) == 14
    assert part2(given, 5) == 23
    assert part2(given, 10) == 37
    assert part2(given, 30) == 259
    assert part2(given, 40) == 406
    assert part2(given, 50) == 566
    assert part2(given, 90) == 1844
    assert part2(given, 100) == 2208
    return True


if __name__ == '__main__':
    assert test()

    input = parser(read_input())
    # ONE #1
    part_1 = part1(input)
    print(part_1)
    assert part_1 == 320
    # # TWO #2
    part_2 = part2(input)
    print(part_2)
    # assert part_2 == 286194102744

# INPUT
"""🎅
swseeneeswneenwneenwswenenwnewswnesw
neneswnwnwnenenenwnenenenenenwne
sweseeseeeeenwe
wswseneeenweeeeeeneeeseeseswe
nwnwnwnenwnwnwswnwnwswnwnwnwnwnwnwnenwee
ewnenenwnwenenwswsesenenweseeew
seswseseseseswneswsesesesesew
enenwneeneswnwswneneneswseneeneneenwne
sewsesesenwseneswsesenenenewseseesesesesw
eswwseswnwsesenweswnweseswsewsesese
nwnwnwwnwnwswnwnwwnwnwswnwnweenwnww
sewwsenwwwnwnewwwwwwnewnwsenww
swswnwswneseswswseswswwswswnenesweseeswnw
wwwsewswswwswsweswswswnwnweneswsww
swwwwwwwswwswsweswsw
seseswwwswswswseneseswseesenwse
nweeneseswswswswweswswneswswswnewne
nweenwseeseeseeeseseswseeswseese
wwnwswewnesewwwwwwwwswwsww
wseseeweenwesesesewnweeseswesesee
seeswnenwewneeeeeswenwnewswnee
wneseswswseesenwswnwesweeeneeene
neswswseseswsesesenwseseseswseswesewsesw
nwnwnwnwnwnenwwnwsenesenwnwnwnwnwnwswnwnw
esewwnwnewseswwwweswwww
wnwnwnwwneenwnwnwnwnewnwsenwnwenw
wsewwwwnewswwwwwewwswnenesw
seseswwseseswsweswesweswnwnwswswwswse
nenwnwnwsenenenwnwnwnwnwnwnwnwnw
nenenenenenwnesenewnewnewneseeeene
swneswswseseswseseswswseswwesenwswswsesw
wsweswwneswwswwnwswsweswsewsesww
swswnewwswwswnwwnwswsesenwwewww
nwwnwenwnwwwswsewwnwwnwnwnwnwnw
wswnesenwnwwseweswnweseseseesenesese
seswswswseswseswswnwesesenwseswswswnwsw
eenenwesweeneswneswewenwenesene
nwswnwenesesesenwseseeeneeweseseswwse
esenenwnweswnewwswenenesewswseesw
wwwswnwwwsenenwsenweswwneswwwnww
wswswswenweweseswneswnwswwseeswnese
neswneenwseeswnwsewnewnwwwesww
enwnwwsenwnwenwwnwenwwwnwnwnwnenesw
seeeneeeneseeewsewseweweese
ewwwewwswswswswsewwwswwnwsww
neneseseneeneneeneeeenwwe
nwnenwneneenwnenenenwnwswnwswseenenenew
swnenwnwswnwswnwnenwnenwnwnwnwnwnwnwswnwne
eseseswswswnwswseseswseswswsenesenwseswse
enwswnenweseneeeeesenwsweeswee
seswnwnwnenwnwnwnwswnwne
swesewseeseeeseweweseeenweee
nwsewseseweneseseneseseseenwseswseseese
ewnenwswwwwwwwwwwnwsewwwwsew
neswnwnwswswswseseweseseseeseswswwswse
eswnwnwneseenenwwnwnwsenwwnwsenenwne
seenwseswswswnwseswsenwswswswswseseesw
seneswenewsesenwswnesewseeseneewsese
nweewswswnwseswsweneseseeswnw
neneswnenenwneesenwseneneewewneene
nenwnenwnwnwwneneneenene
seweswseseneswswsewswswseswnenene
sewnwswsenweseweswenewse
seseseseseeswseseswsenwsesenwseswsesese
eenenweeneeeseee
swseswseseswnenesesenwnwneseneswwwnwsw
swewnewwwweswwsewswwswswswsww
seswswswswneswswswsw
senwseswswnwswswswswwswwwswwswwswnee
seseswswseesewwneswseneseseswsweswsw
swwswwswswsewwswswwsenwneswswwsww
wwswswnwwewwwswswswwwewswww
nwnenenenenenenenwneswnenewsenenenenwne
neswweeeeneeseeneneeeweeene
swswwswswswsweswswswswswneswsw
seseseeseeeneeeewnwnweeewsweese
swswswswswseswsewseeswswswswnwneswswsw
neesewseneswswnwswneswnwswwnwwswswne
swneswnenenenwneenee
neeseewseeeewnweswnweeweewe
seseswseseswswnenwneswsenenewswseesesw
swnwnwenwnwnwswwneswnwnewnwnenwnwswnenwse
nwwswseneneeswneewswwsesesenw
nenenwnwnwswswneenwnwnenwnenwnenwnwsenwne
sewsewnwneseenwseewsesesesesewseesene
seeesenenwseseseseenwseseseweeswsewse
nweenesenwneeeneneeneeeswnenene
ewwwwwewwnwwwwewswswew
seeseswesesesenenwnwswseenwnwsweeswnw
eseswswseneeswnenwwseseseseseseneswsww
sewseseseeesenweenewseeeseswesese
swseseseseneesesesesewseseeweseesese
seseseesesenwsesenwswsesesesesesesesenesw
eweeeneneswswsewsenee
wswwnewwwwsenwwnewswwewwwww
wwwnwwwwwswenewwwwwwnwnwwse
seseswseseseseseseseesesesenwsenwsesese
seseesenwnenwnewswswneesewswsesw
swnwswwwswsweswwe
wwswenewnewnwswweeswwsewnwswww
nwwneswswswswsweswwswswnewswswswswswswsw
wseswnwneswseeseeeeneeeseseeseew
wwwsewwwewwnewwwwnwwwww
wswswswseeswnwswweseseweswswswswne
nwnwnwnwnwnwsenwnenewnwwwnwnwsewnwww
swswseneswswswswswswsewswswswnwnwe
enenwswswseswseseswswswseswswsenenwsw
nwswneswnenwswsenenweeswsesesewseswse
neesewsweswewseswseseseswseswnwnwswsenw
neeneneeneneneneneeseeneneswwwnee
nwswsewnwswswenesenwneneewseweenwnw
nwnwnewwwsewswseeswenwnwnenwnwneenww
wwewwwnwwwwsewwne
seswesenweswswnwswswswneenw
eeeneeenenewneneeneneenee
swswswnwewwnwwwseswswwswewnwwswswsw
wwwnwnwwwnwwesesewwe
swesesesenwsesesesenwseswseswswsese
nwnwsenwsenwenwnwnewnenwnwnwsenenenew
neenwnenesesewnwnewnenewnenenenesenwne
nwnwseneesenwwnwnwnwnwnwnwnesewsenww
swswneswwswswswwnwswsewswwenwseswsw
wswnwsweweswsenwnwnenwwesenwnenesenwe
nenenenenenwnenenewswnenenwneneseneswnee
seseseenwenewsesesesesesesese
newwneenwsweewnesenee
sewnwnewsewnwwnwnwnenwwwnwenwnw
senwwnenwneswnwnwswnenwnwswnwwnenwwnwnw
wwswneswnwnwwwwsenwnwenwenwwnw
eseswnwnwseswweeseswnenesenwsesesenw
swwseeswswwnewwseswswswneswswswnew
seswseswseswswnwnewswseswseswnewswsesw
seseswnwnwneswswenwnwswswswsewwwwsw
wwwwswswnewswnenwwswswnwewseswe
eeneeeneneneeneesw
sewnenwswswswwswswswseeswswswneswswsw
wneneswnenwswseeswnenenenwseneswnewnene
nwnenwnenenesenewneneneneenwne
swsenwsenwseewewswseeswseeseswswsw
seeseneenwseneseseseseswsesesesesesew
wseswswswwnwsweswwwswwwwwwnew
swswswseswneswswseswswswswswsenwseswnese
nwnewsewwnwnesweswewswnwseswe
weneswsweewswsenwnwnwnwsenwnwwwnw
nenenenwwsenenenesenenwnenenene
swwswenwswseswseswswseswseswswneswswsw
nesenenenwsenenenesenenenenenenenwnenenww
nenwnenwnwnwwsenwnwnenenwsenenenwnenenw
seswswneswseseswswseseswseseenwwwswnw
seswseseesenwnesewnwnweseswenwwswe
eneeesenwenwwsweeseeseseseeesenwsw
swswnwswswseseseeswseseseswsweseswnwsese
nesenenenewnenenee
nwnenwenenwnwnwnwnwnenwnwnwneneswnwswnw
nwnesweswnwnewnenesenweneneeeswnene
seseseseseseseneswseswsw
wwnwsenwnwseneswwnewnwswwnwseswwenw
nwnwwewswswnwnwwwnwnwwnwsenwwnwnwnwne
neeneneeeeswsweeeenesweneeene
swswswsewseswswswnenwsewseswswsesesee
nwenenwwneseswneneneenenewswwnesenw
seseseswseeseseeneseesesenewsenesesww
eeeeeseseesenwse
nwnwnwnwwnenwnenesenwnwnenwnwnw
swnwneswsweseswsesenwswswswswswseswseswsw
neenwseseseweseseseeeeeeeeswne
ewseneseweeewsesesewse
senenwswnwnwenwsesenwnwnenwnenwswnenwnwnw
wswswswsweswswseswswwswswwswswnenesw
nwswswnenwenenenwnwnenene
wnewnwswwwneswweewewswwnewsew
eewnesenewneeeneneeeswneneenee
swswswswswswswneswneswneswswswwswneswne
swsenwwwwnwwsenewenenwwnwwnwnwnwnw
swnwnwwwwwwwwwnwwnwnwwe
nweeneseweeswneewneneneneeneeene
neneseneeneneeeenwneeweseneewse
nwswseeswswswsesesenwswseswseseswswsesw
neeneneneneneneesewneswneeweneenenee
wswwswnwwwswswswsesw
eneneeweeeenenenene
wwwnewswwnewwwwsesewwwwenwse
nwnwsewnwnwnwnwnwnw
neswseswswseswswseswswseesenenwnenenwne
nweeweenwneesenwswseswenw
swnewswswswseeneeswnweenenenwnewnwsene
swneneenewnenewnenwswneneswneenenenesw
nwsenwsewnenwsenwnwnenwnwwswswnwnwnwnwnwe
wewnwewwwewwwnwwswwwswswwsw
nwwwwsenwwnenesenewswwswewwswwsw
esweeneeesweeeneseenwneneeneswe
ewswswwswwwswswwwww
wwwsesenenwnwnewwewsewwswweswnew
nwneswnesenwneneesenwnwnenenwnewsenwnw
wsenenwnwnwseewsenwnwenweneswneseswwnw
swswswswseseswsenwsesweseesesesewswsw
eweeseesweneseeseesesesee
nwewseneswsewsenweseeseswsesenenenw
sesenwwswseeeeseeseseswneseseeesese
nenewneneneneneneneneenenwnwnesenenenesw
swseseeseseseseseseseesenwwswneese
seseseseseseseeeeseeseneseeweswnw
nwswwseneenewsesenenenwnenwsenesenwswnwe
nwnenwwsenwswewsenwnwnwnenwnwnwnwnwnwnwnw
sewswsweweswnwwneneswnese
nwswneseswseswseseseseswenwswswswswswswse
newenwnwswnwswnwnwneeswweswnwesenwsw
eenweeeeenwsenweseeeesewse
wseeeswswwwwwswsesenenenwswnwwwenw
eseeneenenweeesweeenwee
seswswswwseesesese
eeseseeeenwswnwseneseweseeeeseesw
seseseeseeneewwseswneseseneneswnwwe
wwwwwwwnewwwwseww
wseenwnwnwwsenwnewnwwwwweewsww
swwenwwwenwnwneseswesewwneswswse
swswnenenenenenenwnene
nwswneswwnwwswwsewsewnenwwwwenenw
nwswseseseeseswnweseswswseswswnwsesew
swnwswswsesenwsweseswsenwne
eneeneeneeeseeneneswswsweneenenewe
wsesweseswnweeeeeeenwesweenwe
nenenwwnweenenewneseneneswnwnenwswne
wwwweswwseswneswswnwwswneseswswswsw
eswenweseeeeeeweseneeneeseseee
seseseswseseneesesenwswsesesesesesesew
swswneseswswswseneswwwsesweseseseswse
weseeeseeeeeseseeneseeenwseswse
eseeneesenesewnesewseseswseseseesew
nwswswseswseseseseswseeeseneswswsewse
wnwnwsenenwnwsesenwwesewnenwseeswenenw
senweeseswwswseseseeneeese
neswseseseseseesesesesesesese
senwenwnwsweeswswseseseseeseneseeewse
eswnwswswseswsweswnwswnwwswnwswswsesw
seweswswsenwsenwseswsenesw
neneeneswnwnenenenwewnwnewneeswnwne
wswswswsenenwnwswswsweswswneneeswsesww
swnwnenwnenwnenenesesenenenenenenenwnene
enesweeenwswswnesweneneeneeeswee
nwnwnwsenwnwnwewnwnwnwnwnwnwneswnwnwnwnw
enwnesesewesenweseeewseenwesee
swsenewenesewwswwwsewnesw
eneeeneeeeeenwwneneeseeeewse
ewseeeenwnesewesweeeeeeseseee
nwwneneseswnenwnwnesesenesenenwnwswnwwne
eenwnwwwsewwwne
swenwnwnwnwnwewnwewnwswnwnwnwnwwnww
seesewseseswnesenwesenweeswswseswne
wwwweneneewseswsenwwswwwwwnew
enwnwnwwewseswwnwwnwnwnwwnwnwwee
enenenenenwnenenwwnwnenenwswneneenenw
eeweseeewseeesesweeenenwenesese
neswnwneneneneeneeeneneeneeneswnene
swwswwswewwswwswswwneswswwswsesw
neswneneseneneneneneneneneneneneswnwnenene
nwwnwnewnenweswnwweswseenwsewwnwse
eseeeweeeseeeenwswesenweeee
seswseseswswneseneseseseseswseseseseenenw
neseewswswweweeewwenwewsenwnw
seswnwseseseeesenwwseseseswnesesesese
swwnwswnwnwnwwnwnwnwenwenwnwnwnwnwnw
eneseneswewneseenwenwnweseneeneenw
swsenwwwseswswnwswswwenwswswsweswsw
neneneneneneenenewneseeneenenwswene
swswswswswswwswswenwwswswswswswswswe
swnwswwnenwswwneeseseswwnenesewsene
neeesweewneenwneseeeeneeenee
wnwwwswnwnewswnwswsewnwnenweeswnew
swneneneneneeneneeeneneeswnenene
weseswseeswewnwwseseese
eesweeseeeseeeenweee
seswswwsewseswneneswwwneswneewneswww
sewseswsewswwswwwwnwnesweswnwneswe
nwnwnenewnwnenwsenenenwneenwnwnesewnene
swnwswnwnwswesenesesesewnwsenwnwneese
wnwnwwnwwnwnwwenwnwnwenwwwnwseew
nesweseswwnwnwnwnwwswswseenenwwsesw
esesenwneneeneneseneeenewewe
wsesweswnwswneswswswwsesenwswneswswsw
eswnenwenenwneeeswewenweneeesw
wneneeneeswneenenenewneneenenenenwnese
wwnwwwsewnwwwwnenewsenwwwww
nwsenwsenwnwnenwnwwnwnwneswneneneenenwnene
wswnweneswswesweeewwnenwnenwnenwne
wewwwwwnwswwnenwnewswwewswnw
swwwnwweeswewswwwwsewwwnwnw
neeneeeenwneneeweneeseee
swenwneeneswneneewneneeneseseeswew
nweeeeeeseeeeeeswesweeene
nwnwenwnwneseneseswnwnewenwswnwenewnw
wsesesesesesesesesesenesesw
wwwwwnewweswswnwwewwewwsww
wnenwnwwwwwwnwnwwnwwnwnwsew
nwnenesenenenenenewneneweneneneenwnesw
esewnesenwneeswenenewswswwnwsesenwnw
eeeeeeeeeseneewswnweeeneswe
neneseseweswwwwswnwwswnwwsweswwww
seswswneswswswnewsweswswswsenenwwwsw
nenenweneneneneneswneneneeene
sewnwseeneseseeswseeenwseseseneseswee
enewneseeeseneeeeeneeeeneenew
esewswenweseenwseeeeeeesenesw
nwnwenwnwnwewnwswnwswseseneewnw
enwnwnenwnwwswnwnwnenwnwnenwnwsenenenw
nwsenwwnwenwenwnwwenwewswwenwww
senwsesesesesesenenwsesenwsenwneseseww
wsenwswseseswewswneseswswswesw
nwwnewwnwsewwwwwwsewwnwwseww
wsenesesenenwneswwseswswswneneswswseswsw
seseseseseseneseenwsesewseseseesesese
neneenenewnenenenenenenewneneenesew
ewwneswswnenenwswnwswseseeswnwesewsw
seswswewneswwnwnwnwswneneeseswnewe
nenwwnwwsenwswnwnwnwwnwwenwnwnwnwnwnw
wwwnwnwseswwnwwnwneeswwnwneswnwnw
swswwwnwnewwwweswswswwwwsewswsw
eeeeswesweeeeenweeenweenee
senwseweswnwnwswnenenwwnwsenwnwnenenw
nwnwwnwnwsesenwnwnwnwnwnwnwneswe
swseeseswseseseswneseswnwnwwseswnwsenw
nwwewewwnenwnweswsesee
swewwwsewwswswwnwwwswswnw
wnwweenewnwnwsweswwewwsewswse
swenesewsesewsesenesesewsenwesesewnw
eseseeeesenwesenweseseseseswswesese
nwnwnwnwnwnwnwnwnwnwsenwnwwnwnwnwnwsesenw
seeseenwnwwseneswseseseseswsesenwsee
swswswsweswwwswswnwswwswswswwswese
wswwwwnewwnwwswswwnwwsewsesewne
swswnwswneswenwswseswseseneseswwesww
swswneswswswswewswnwswww
nwnwnwnwnenwwnwenwnwnwnwnwnwnwnwseesw
swnwseneenenwneneseneneneeeenewnene
neeeeeseneneneneeeswnwneeswenene
enwwnwnwwnenwnwnwenwwnenwneesenwnene
nwwnenwenwewwesenwnwwswnwwsenww
wnwnwnwnwnwwnwnwswwnwenwnw
swwwwnewswnenwswseseswswnewesewne
nenwwnwnwnwnwnwneenwnwsenwnenwnwswnwnenw
neewsweeeeeeneeeeneeswneeee
wwswwwwseswswswwwswwwwnewwe
nwwswseneenesewswneswswneseswswwnesw
eneneneneneneenewnenenene
nwenwneneeeswwneeneswneneneseneeene
nenweeneenwnesewneswswenew
swwwweswnwwsweswswswwswswswwwsw
swswnwnwswswswswswswseswsweswswwswswsw
nesewswswseswseseneseneseseene
newneswwneeneeenenwswseneeenenwene
neneswseenenewneswwnenweenenenenwsene
seneneneseneswnwnenewenenenenwwswnenw
nwnwsenwnwnwnwnwsenesenwenwwnwnwswnewnwnw
seeesenesenwseeswwswnwnwseneseewenw
swswsesesenweseeseswwsesesenesenwsesesw
swswwneneswswswsweswswswswswswswswswswsw
wseseswneseseseseseseswneswesenwsesese
nwenwneeneseswswwnwnwnwnwwsewswnwne
nwnenenwwneseneenwnwnenwnwnenewne
sesenwseswenweeeeesesesesewsesesee
wnwswnenwwwenwwnwnenwwnwwsewwsww
nenenwnwnenwwnenwnenwwsenwnenwnwsenwewse
⛄"""
