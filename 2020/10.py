#!/usr/bin/env python3


# HELPER FUNCTIONS
def parser(text) -> list:
    return [int(l) for l in text.strip().split("\n")]


def read_data() -> list:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return parser(data)


# MAIN FUNCTIONS
def find_differences(nums: list) -> dict:
    jolt, _nums, diffs = 0, sorted(nums), {1: 0, 2: 0, 3: 0}
    for adapter in sorted(_nums):
        diff = adapter - jolt
        if 0 < diff < 4:
            jolt = adapter
            diffs[diff] += 1
        else:
            break

    # Finally, your device's built-in adapter is always 3 higher than the highest adapter
    diffs[3] += 1
    diffs['adapter'] = jolt + 3
    return diffs


def find_joltage(diffs: dict) -> int:
    return diffs[1] * diffs[3]


# PART 2
# approach 1 - produce arrangements and count the length
# too much space and time
def produce_sequence(arrangements, start: int, opts: list):
    """
    NB: doesn't work for big input.
    Actually producing sequences, generating sequences for input takes too much time
    """
    new_sequences = []
    for l in arrangements:
        if start < l[-1]:
            continue

        l.append(opts[0])
        i, n = 1, len(opts)
        while i < n:
            new_seq = l[0:-1]
            new_seq.append(opts[i])
            new_sequences.append(new_seq)
            i += 1
    arrangements += new_sequences


def find_arrangements1(nums: list) -> int:
    adapter_map = to_adapter_map(nums)

    arrangements = [[0]]
    for k, v in adapter_map.items():
        produce_sequence(arrangements, k, v)

    return len(arrangements)


# approach 2 - keep track of leaves and the count the length of leaves
def count_sequences_by_keeping_track_of_leaves(leaves, start: int, opts: list):
    """
    keep track of leaves in sequence tree
    """
    i, n = 0, len(leaves)
    while i < n:
        if start == leaves[i]:
            leaves[i:i + 1] = opts
            i += len(opts)
            n += len(opts) - 1
        else:
            i += 1


def find_arrangements2(nums: list) -> int:
    adapter_map = to_adapter_map(nums)

    leaves = [0]
    for k, v in adapter_map.items():
        count_sequences_by_keeping_track_of_leaves(leaves, k, v)

    return len(leaves)


def to_adapter_map(nums):
    jolt, i, n, _nums = 0, 0, len(nums), sorted(nums)
    optional = set()
    adapter_map = {}
    while i < n:
        adapter = _nums[i]
        if 0 < adapter - jolt < 4:
            if jolt in adapter_map:
                adapter_map[jolt].append(adapter)
            else:
                adapter_map[jolt] = [adapter]
            j = i + 1
            while j < n and 0 < _nums[j] - jolt < 4:
                optional.add(_nums[j - 1])
                adapter_map[jolt].append(_nums[j])
                j += 1
            jolt = adapter
        else:
            break
        i += 1
    return adapter_map


# approach 3 - FINAL one
def count_sequences(leaves: dict, start: int, opts: list):
    """
    keep track of leaves in sequence tree
    """
    if start in leaves:
        curr = leaves[start]
        del leaves[start]
        for o in opts:
            leaves[o] = leaves.get(o, 0) + curr


def find_arrangements(nums: list) -> int:
    adapter_map = to_adapter_map(nums)

    leaves = {0: 1}
    for k, v in adapter_map.items():
        count_sequences(leaves, k, v)

    # all sequences must end with the same node
    assert len(leaves.keys()) == 1

    return leaves.popitem()[1]


# borrowed from https://github.com/sophiebits/adventofcode/blob/main/2020/day10.py#L41
def countways2(nums):
    top = max(nums) + 3
    nums = set(nums)
    nums.add(top)
    a, b, c = 0, 0, 1
    for i in range(1, top + 1):
        if i in nums:
            a, b, c = b, c, a + b + c
        else:
            a, b, c = b, c, 0
    return c


# TEST
def test():
    # GIVEN
    given = """
16
10
15
5
1
11
7
19
6
12
4
    """
    given2 = """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
    """
    assert {1: 7, 2: 0, 3: 5, 'adapter': 22} == find_differences(parser(given))
    assert {1: 22, 2: 0, 3: 10, 'adapter': 52} == find_differences(parser(given2))
    assert 8 == find_arrangements(parser(given))
    assert 19208 == find_arrangements(parser(given2))
    # assert 19208 == find_arrangements1(parser(given2))
    # assert 19208 == find_arrangements2(parser(given2))


if __name__ == '__main__':
    test()
    lines = read_data()
    # ONE
    part_1 = find_joltage(find_differences(lines))
    print(part_1)
    assert part_1 == 2475
    # # TWO
    part_2 = find_arrangements(lines)
    print(part_2)
    # # assert part_2 == 3585

# INPUT
"""🎅
48
171
156
51
26
6
80
62
65
82
130
97
49
31
142
83
75
20
154
119
56
114
92
33
140
74
118
1
96
44
128
134
121
64
158
27
17
101
59
12
89
88
145
167
11
3
39
43
105
16
170
63
111
2
108
21
146
77
45
52
32
127
147
76
58
37
86
129
57
133
120
163
138
161
139
71
9
141
168
164
124
157
95
25
38
69
87
155
135
15
102
70
34
42
24
50
68
169
10
55
117
30
81
151
100
162
148
⛄"""
