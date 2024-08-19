#!/usr/bin/python
from collections import namedtuple

seeds = [79, 14, 55, 13]
maps = [[(50, 98, 2), (52, 50, 48), ], [(0, 15, 37), (37, 52, 2), (39, 0, 15), ], [(49, 53, 8), (0, 11, 42), (42, 0, 7), (57, 7, 4), ], [(88, 18, 7), (18, 25, 70), ], [(45, 77, 23), (81, 45, 19), (68, 64, 13), ], [(0, 69, 1), (1, 0, 69), ], [(60, 56, 37), (56, 93, 4), ]]

testdata = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
    """.strip()

Map = namedtuple('Map', 'name ranges')


def parser(text) -> tuple:
    lines = [line for line in text.split('\n\n')]
    seeds = [int(s) for s in lines[0].partition('seeds: ')[-1].split(' ')]
    maps = [Map(p[0], [tuple(int(i) for i in r.split(' ')) for r in p[-1].strip().split('\n')]) for m in lines[1:] if (p := m.partition('map:'))]
    return seeds, maps


given = parser(testdata)

seeds, maps = given


# part 1
def domap(m, v):
    for dst, src, n in m:
        if src <= v < src + n:
            return v - src + dst
    return v


s = list(seeds)
for m in maps:
    s = [domap(m.ranges, i) for i in s]
print('part 1')
print(min(s))


def maprange(m, a, b):
    for dst, src, n in m:
        if src < b and a < src + n:
            ra = max(src, a)
            rb = min(src + n, b)
            yield (ra - src + dst, rb - src + dst)
            if a < src:
                yield from maprange(m, a, src)
            if b > src + n:
                yield from maprange(m, src + n, b)
            return
    yield (a, b)
    return


def flatten(r):
    new = []
    r.sort()
    for a, b in r:
        if new and a <= new[-1][1]:
            new[-1][1] = max(new[-1][1], b)
        else:
            new.append([a, b])
    return new


def mapranges(m, s):
    new = []
    for begin, end in s:
        new.extend(maprange(m, begin, end))
    # return flatten(new)
    return new


s = sorted([(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)])
print(f"Before mapping")
print(s)

for m in maps:
    print(f"Mapping {m.name}")
    s = mapranges(m.ranges, s)
    print(s)
print('part 2')
print(min(s)[0])
