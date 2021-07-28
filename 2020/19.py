#!/usr/bin/env python3

# HELPER FUNCTIONS
import re
from functools import lru_cache
from re import Pattern


class FrozenDict(dict):
    def __hash__(self):
        return hash(frozenset(self.keys()))


def expand_rule(ref, refs_map, rules) -> list:
    """
    rules object received 'loops' to support part 2
    """
    if ref in rules:
        return rules[ref]
    constraint = refs_map[ref]
    if '"' in constraint:
        rules[ref] = [constraint[1:-1]]
        return rules[ref]
    conditions, all_vals = constraint.split(' | '), []
    for c in conditions:
        refs, c_vals, patterns = c.split(' '), [''], []
        for r in refs:
            if r == ref:
                if 'loops' not in rules:
                    rules["loops"] = dict()
                key = "_R" + r + "_"
                rules["loops"][key] = constraint
                resolved = [key]
            else:
                resolved = expand_rule(r, refs_map, rules)
            c_vals = [start + end for start in c_vals for end in resolved]
        all_vals.extend(c_vals)
    rules[ref] = all_vals
    return all_vals


def parser(text) -> tuple:
    constraints, messages = text.split("\n\n")
    constraints = re.findall(r"(\d+): (.*)", constraints)
    messages = [l for l in messages.strip().split("\n")]
    raw_refs_map = dict()
    for r, constr in constraints:
        raw_refs_map[r] = constr
    rules = dict()
    # expand only the rule we need
    expand_rule('0', raw_refs_map, rules)

    return FrozenDict(rules), messages


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# MAIN FUNCTIONS
def part1(rules, messages) -> int:
    counter, check = 0, set(rules['0'])
    for m in messages:
        if m in check:
            counter += 1
    return counter


@lru_cache()
def re_wildcard(rule: str, ref_loops: dict) -> Pattern:
    pattern = rule
    for k in ref_loops.keys():
        pattern = pattern.replace(k, "(.+)")
    return re.compile(f"^{pattern}$")


@lru_cache()
def check_pattern(message, patterns, flat_loops, rules):
    patterns = {re_wildcard(p, flat_loops): p
                for p, spl in
                patterns.items() if message.startswith(spl[0]) and message.endswith(spl[-1])}
    m_patterns = [(p.findall(message), re.compile('_R(\d+)_').findall(patterns[p]), patterns[p]) for p in
                  patterns.keys() if p.match(message)]
    m_patterns = [list(zip(match[0] if type(match[0]) == tuple else match, rule)) for match, rule, _ in m_patterns]
    for m_p in m_patterns:
        counter = 0
        for inner_message, ref_rule in m_p:
            wildcards = FrozenDict({r: r.split("_") for r in rules[ref_rule] if '_R' in r})
            check = set(r for r in rules[ref_rule] if '_R' not in r)
            if inner_message in check:
                counter += 1
            elif check_pattern(inner_message, wildcards, flat_loops, rules):
                counter += 1
        if counter == len(m_p):
            return True
    return False


def part2(rules, messages) -> int:
    zero_rule = rules['0']
    counter, check = 0, set(r for r in zero_rule if '_R' not in r)
    flat_loops = dict()
    for k in rules["loops"].keys():
        ref_rules = rules[k.replace("_R", "").replace("_", "")]
        flat_loops[k] = [r for r in ref_rules if '_R' in r]
    flat_loops = FrozenDict(flat_loops)
    wildcards = FrozenDict({r: r.split("_") for r in zero_rule if '_R' in r})
    for m in messages:
        if m in check:
            # print(m)
            counter += 1
        elif check_pattern(m, wildcards, flat_loops, rules):
            # print(m)
            counter += 1
    return counter


# TEST
def test() -> bool:
    given = parser("""
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aba
""")
    assert given == ({'0': ["aab", "aba"], '1': ["a"], '2': ["ab", "ba"], '3': ["b"]}, ['aba'])
    given = parser("""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""")
    assert given[0] == {'4': ['a'], '5': ['b'], '2': ['aa', 'bb'], '3': ['ab', 'ba'],
                        '1': ['aaab', 'aaba', 'bbab', 'bbba', 'abaa', 'abbb', 'baaa', 'babb'],
                        '0': ['aaaabb', 'aaabab', 'abbabb', 'abbbab', 'aabaab', 'aabbbb', 'abaaab', 'ababbb']}
    # part1
    assert part1(*given) == 2
    input = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""
    assert part1(*parser(input)) == 3
    input2 = input.replace("8: 42", "8: 42 | 42 8").replace("11: 42 31", "11: 42 31 | 42 11 31")
    assert part2(*parser(input2)) == 12
    # part2
    return True


if __name__ == '__main__':
    assert test()

    input = read_input()
    rules, messages = parser(input)
    # # ONE #1
    part_1 = part1(rules, messages)
    print(part_1)
    assert part_1 == 226
    # # # TWO #2
    input2 = input.replace("8: 42", "8: 42 | 42 8").replace("11: 42 31", "11: 42 31 | 42 11 31")
    part_2 = part2(*parser(input2))
    print(part_2)
    # assert part_2 == 85660197232452

    # INPUT
    """🎅
108: 117 50 | 63 64
124: 50 64 | 64 64
123: 64 119 | 50 85
45: 60 64
32: 20 50 | 79 64
36: 97 64 | 70 50
97: 50 64 | 64 50
21: 50 104 | 64 83
59: 50 124 | 64 83
10: 115 64 | 34 50
118: 50 124 | 64 4
60: 12 50 | 4 64
84: 29 64 | 99 50
111: 64 27 | 50 14
18: 64 101 | 50 29
13: 64 45 | 50 1
62: 64 97 | 50 83
117: 124 64 | 70 50
98: 50 4 | 64 124
15: 64 114 | 50 12
7: 100 64 | 56 50
78: 99 50 | 52 64
82: 114 64 | 97 50
22: 6 64 | 4 50
63: 12 50 | 114 64
16: 64 52 | 50 70
76: 50 46 | 64 13
31: 64 69 | 50 67
37: 21 50 | 128 64
95: 68 64 | 16 50
12: 64 50 | 50 30
26: 50 12 | 64 83
112: 113 50 | 72 64
33: 104 64 | 52 50
25: 70 64 | 114 50
96: 51 64 | 105 50
51: 50 47 | 64 26
91: 103 50 | 9 64
65: 66 64 | 23 50
116: 64 114 | 50 97
42: 64 54 | 50 40
4: 50 64
79: 50 97 | 64 29
110: 64 116 | 50 118
0: 8 11
73: 50 12 | 64 101
70: 50 50 | 64 50
74: 61 50 | 65 64
27: 50 107 | 64 90
101: 30 30
105: 17 50 | 24 64
61: 58 64 | 102 50
17: 50 83 | 64 29
72: 30 97
88: 64 38 | 50 2
14: 50 36 | 64 2
125: 64 50 | 64 64
127: 95 64 | 28 50
83: 64 64
80: 64 107 | 50 81
106: 50 101 | 64 29
56: 88 64 | 49 50
52: 50 50 | 64 64
46: 80 50 | 120 64
94: 68 64 | 33 50
47: 50 114 | 64 6
69: 44 64 | 57 50
54: 74 64 | 3 50
89: 50 83
48: 106 64 | 59 50
87: 86 50 | 37 64
35: 64 73 | 50 55
115: 50 99 | 64 70
44: 111 50 | 109 64
75: 78 50 | 22 64
20: 64 101 | 50 6
41: 50 4 | 64 101
6: 64 50
66: 50 93 | 64 115
90: 64 101 | 50 124
23: 50 82 | 64 77
81: 50 114 | 64 101
30: 50 | 64
100: 122 50 | 75 64
86: 50 73 | 64 18
92: 64 48 | 50 71
68: 6 50 | 114 64
121: 50 70
8: 42
85: 64 112 | 50 110
38: 64 104 | 50 4
120: 84 50 | 55 64
67: 64 7 | 50 53
64: "a"
55: 50 52 | 64 125
28: 89 50 | 84 64
71: 50 39 | 64 16
109: 43 64 | 94 50
99: 50 50
43: 41 64 | 77 50
119: 64 108 | 50 35
57: 87 50 | 96 64
39: 64 97 | 50 6
104: 50 64 | 64 30
29: 50 64 | 50 50
34: 83 50 | 125 64
2: 99 64 | 124 50
11: 42 31
114: 64 64 | 30 50
93: 50 97 | 64 101
58: 50 33 | 64 121
113: 64 99 | 50 70
128: 64 4 | 50 125
40: 123 64 | 76 50
107: 50 52 | 64 83
102: 126 50 | 25 64
126: 50 125 | 64 97
19: 50 124 | 64 114
24: 114 64 | 29 50
49: 20 30
1: 64 19 | 50 15
103: 26 50 | 18 64
9: 64 117 | 50 62
50: "b"
53: 91 64 | 5 50
77: 6 64 | 99 50
5: 32 64 | 10 50
3: 64 92 | 50 127
122: 115 64 | 98 50

bbabbaaabbabbaaaabbbbbbb
bbaabaaaaabbbaaaabaaabba
baabababbbbaaaaabbabaaba
baaabbbabaabbaaababaabbaaaaabbbb
bbbbaabbbabaabbabaabaaaa
aabaaaabaababbbbababaabb
bbabbbaaabbbbabbbbabbabbbbbbbbabaabaaaabaabaabbabbabbbbbaabaaaba
baaaaaaabaabbbaaaaaababb
aaabbabaaabbabbbabaaabba
abbbbbabbababaabbaaabbbaababbbbaababbabb
bababbaabbbbbbaababaaabaaabababbabababba
babbaabbbabaabbbbbaaabba
abbbbbabbbbaababbababaaa
aaabaaababbaaabbbbbabbaaaabbbbba
bbaabaaaabbbaaaabbabbbab
baabaabababbaaababbababa
abbbbbabababaaabbbbbbbba
aababbbababbababaaababababbbbbbabaaabaaa
bbbbabaabbabaabbbbabbbaa
aabaabbbbbbababbbabbbaba
abbababaabbbaabbbabaaaababbbaabababbaaaaababbaabbbaabbabbbabaaabbaabaabbbbaaabaa
baababaaabababaabaaabbabbbaaaabbabbabaab
bbbaaaaabaababaaaaabbaaabbbababbaaabaaba
bbababbabbbbbbabbbbabbbbbaabbbabaabbbbababbabaab
abbbbbabbbabaabbbabbaabaaababaab
bbbbabbbbaababaaaaabbbbabbabbbbbbabbbbaaabaabbabaabbabbb
abbaabbabaaabaaaaabbbbaaaaabbbbb
aabaababababbbabbbabbbaabaaaabaaaaabbbbbaabbbabbaaabbbab
abaabaaabababbaababbabab
aabaaaabbbaababbbbabaaab
bbbababbabbbbabaaaabababbbabbbabbbbaaaabaaabbbbbaabababbbbababbbbbabaabb
aabbaababaabaaaaabbbbbabbbaaabaaaabaabab
baabbaaaaaaabbabbbababab
abbbabaabaabbbabbabaaaabaabaaaababaabbbb
aabbbabaaabababaabbababb
abababbbabaaabbaaaaaaababbabaabbbabbaaaabbbbbaab
abbabbaabbbaabbbabbaabaa
baabababbaabbaaabaaababb
aababaabbbabbababbaabababaaaabbabaabbaab
bbaaaabbbbbbababaabbbaaaabaabaaabbbbbbba
abbaabbbbaababaaaabaabaa
aaaaaabbabbaabbbbaabbabb
bababababababaabaaabbaabbababaababaabaabababbaba
ababbbbabbbbabaaabbbbbba
babaaabaaabbababbabbbbaa
bbabbbbabbbbbbabaaababbbaaabbabbbabbabbababbabbbbaabbbaabbababaa
bbaabaaaaabbbabaabbabbba
babababababbaabaaabbbbbb
baabbbabaabaabbabaabbbbb
babbbbababbaaabbbaaabbaabababbaabababaabbbbbaaabaaaaaaaa
aabbbabbababbbbaaaaaabaa
bbbababbababbbbabbaaabba
aabbabbaababaabbbbaababa
abbabaaabbbaaaaabbbababaaabbababbabbbaab
babaaaaaaababababbbabbbbbbbbbbaa
abaaababbabbbbbabaabaabb
babbbabbabbbbbabababbbbaaababbab
aaabbbbabababaabababbbbaabababab
baaabaabbabaaaabbababbaabbbabbbaabbbabbb
babaaabbabbabbabbabbbaba
bbaabbbababbbbabaaaabaaaaabbabababaabaab
abaaabaaabaabababbaaaabbbabbabab
bbbaaaababbabbabaaaaabab
bbbbababbaaabbaaabaabbbb
abbbbabbbaaaaababbbbbbba
bababbabaababbbbbababaaa
bbababbabbbbabbbbbababaabbbbbbbbabbbbabbbbaababa
baaaaababaabababaabaaabb
baabaababaaabbaaabababab
baaaaaaabbbababbbbbaabbbaababaaa
ababaaabbabaabbbabababba
baaabbbaabbabaaabbaaaaabaaaabbabbabbbbbbbbbaabaa
bbbababbabbbaaabaababaab
aaaaaabbaabbbaaabaaaaabb
babaaabbbbabbaaabbabbaab
aaabbaabbbababaaabaabaababababab
aaabaabbbabbaaaaababaaabababaabb
bbaaaabbbaaabbbaaababaaa
bbabbbbabbbaababbabbabba
baabababaaababaababaaaaaaababbab
baabbaaaaaabaaabbbbbaaaa
babbaaababaabaaaaaaabbbb
babaaaaaaaaabbabaabbababaabbabbaababaaabbbaabbaaaaabbbbb
abababaabbabaabbbaabbaaabbaaaaaa
bbbbbbaaaaabbabbbabbaaaabaabbbaababbbbbbbaabbbbaabbbababaabbaaababaababbabbbbaaaaabaaaaaaabaabab
bbababaabbbbaabbbbaabbbbbbbbbbbabbbaabbabbbbbabbabaaabaaaaabaaaa
abbbaabbbbbaabbbbabaabaabababbbbabaabbab
babaababaaababaabbaabbbbaaabaaabaaababbbabbbaaaabbabbbbbbbaababaabaabbbbbbbbbaaaaaababaa
babaabaababaabaabbaabbbb
bbbbbaaabbababaaabaabbaaaaaaabbbabbabaabbaaaabba
babbbbbbaaabbbabbbbabaaa
abaabaaababbbbabaababbab
bbaaabaabaaaaaaaaaabbbabaabbbbbb
aaabbbabaaaaaabbaabbaabbbaabaabaaabbababaaabaaababbbabab
aaabbaabaabbabaabbbbabbabaaabaabbaabbabb
babababaabaabaaababbaaba
babbbbbbabababaabaabbaba
baabbbabbbaaaaabababbaabaabbbbaaababaabaabbaabaaaaaabbaabbaaabba
abbbabaaabbbaabbbbaaabba
baabbbabaabbbbaaaabbbbbb
bababbabaaaabaaaaabbbbaaababaaaaaaababbaaaabbbbbabaabbab
abbaabbbbbabbbbbaabbbaab
ababbbabababbbaaaabbbabbbbaabaabbbbaaabbbaababbaaaaabbbbbaabbabb
aaababaaabbaabbbabbbbaaa
bbbababbbabbbaaaaabbbbaabaaabbaabbabababaaaaabaa
babaabaaabbaabbbbbbbabaaabbaaabbbaababbaabbbbbbbbaabaaaa
bababaabaabaaaabbaaaabba
baabbbbabaabababbaaabbabbbaabbbaabbbbabaababaaaaababbabaaabaabaaaaaababb
aabbbabbbbabbaaaaaaaabba
bbbaaabbaabbababbaabaaaa
abbbbbababbaabbbbaaabaaabbbbbabbbaaababaaabbaaababaabaaabbbabbaabbbbbbababaababb
babbbbbbababbbaabbabbbab
abbaabbaaababbbabbaababa
aaabbbabbabaabaaabbaabbbabbaabbbaaaaaaaa
abbbbabbbbbbabababbaabab
bbbbababaaabababbbbbbbba
bbbabaabababbbabbaaaabbbbababbabbabababa
aababababbbababbbbaabaaaababbababbbbaaaaabbbbabaabaababbabbbaaabbabbaaaabbbbababbabaabab
aabbaaabababbbaaabbaabaabababaaaaaaabababbabaaab
bbaaaaabbabbbbbabbabbbab
babbaababbbbabbbbbabaaab
aabababaaabbababbbbbaaba
babbaaaabbbaabbbbbbbabaaabbbbbba
bbaabaabbbabbbbaabaaababbaabababaabaaaaa
abaaababbababbaaabbbbbbb
bbaaaabbabbabaaaababbabb
aaabababaababababaaabbbb
ababbaaaabbbaabbbaabababbaaabbababbabbbabbaaabbb
aababbbaabababbabbabbbabbbaabababbbaababbabaabbabaababaa
baaabbbababbbabbbbaabaababbbbabbbabababbaabbbbba
aabababbaababbbbabbbaaaababbbbabbbbaaabbbabbbabaabaababb
baaabbabababbaaabaaaabab
aababbbaaabaabbaababbabb
aaabbaaaaababbbbbaabbbbbbaaaabaa
bbbbbaaababaabaaabbaabbbbbabbbabaaaaabab
aababbbbaabaabbabbabbaab
bbbaaaabaaaabaababbbbbbb
abbabaaaaaaabaaababaaabaaaababbbabaaabbb
abbbaaabbabababaabbbbbaa
baababaaaaababababababaabaaabbbaabaabaaa
bbbbbbbbababbbbabbabbaab
ababbaabaabaabbbabbbbbbb
babaaababaabbaaaabbabbaaababbababbabbbaaababbbabbbabbbabbabbbabb
babaabbabbbaaababbaaaaaa
bababbbaabababaabababaabaaaaaabbbbbababa
bbbbaabbababaababaaaaaab
ababbabbbabbbbaabaabbbbb
aabababbabababbaababaabbbbbaabaaabbbbbababbbbbabbbbbabbbbababbabbaababaa
ababbbababbabbaabaaaaabb
babaabbbbabbabbbaaabbaabbaabbbababbbabba
abbbaaabbaababaabbabaaba
bbbabaabbabaabbbaabaabab
ababbaaaaabaaaabbbaaabab
baababababbabbaabbababab
abbbbbabbbbbaabbaaaaaaab
baaaabbbaababaaaaabaaabbababbababaaaaabbbaaaabaa
bbbaaabbabbbaaaababaaaaa
bbbbaabbbbabbaaabbaaaaba
aaaabbabaaabbabbaaaabbba
abaabaaabbbaaaababbaaabaabbbaaabbbababaaaabbaabbabbabaababbabbbb
aaabaabbbbaabaababbbaaababbbaaba
baaabbbbbabbababbabaabab
babbbabbabbabaaaaaaaaabbbbaaaaaa
ababbaaaabaababaaaabbbbb
bbbaaabbbaabaababaaabbaabbbbbbaaabbbbbaa
ababaaaabbbbbbbbabaabbaa
bababaababbbabaaaabbabaa
babbabaababbaaabbabbbbaababaababbbbaaaaaaaabaabaaaaaababbbabbbbaaaabbbaa
baaabaaaabbbabbabaababbb
babaaaaabababababaabbaabbaabbbbabbabbabbbbaaaabababbabbbaabbbaaa
baabaababbaabbbaaababbab
aabaabababaabbbabbbabaaaabaaabaababbabbbaaabbbbbbaabbbaabaaabbbbaababbbbaabbaabb
aabbbabbbbaabaaabbbbbabb
aaabbaabaabbabbabaaaabba
baaabbbaaaabbaaababbabba
abaabbbababbbbababbaaaaa
bbaaabaaabbbbababbbaababbbbbbaaaabbaababaaabbbbb
ababaaaabbbbbaabbababaabbbabbaaabbbbaaba
aabbabaaaabbbabbbaabbbbaababaababbbabbbbabaaabaabbaaaabbaabaaaaa
bbbabbababbaaabbbaabbaaabaabbbaaaabbbbaabbababaaaabababb
babaaababbbbbaaaaabaaabb
abbbabbabbbbaabbbbabbbaa
bbbbabbbababbaabbbabaaaa
abbbaabbbbbbbaaaabbababa
bababaabbbbbbbbbaaaaabbb
babaaaababaabababbaabbaa
abbbaabbabaababaabaaabaaabbbabaabbaababa
bababbababbabbaabbaaaaaa
babbaaaababbaaabbbabaaaa
bbbbbaaaaabbababaaaaabaa
abaababaabaaabaaabaababb
baabbbbababbaabbbbbbbaba
bbabbbbbbbaaaaabbbaaaaabbaabbbaabbbbaaabaaaabbaa
aaabbbaaaaaaabbbaaabaabbaaaaaaaabbbaaabbbbbbbaba
aabbbababbababbaaaaaabbb
bbaabaaaabbaaabbabbabbababaaabbabbaaabba
babbaabbabbbbabbbabbbaaabbbaabbbbabbbaababaabbabbabbbbaa
bbbaabbbaababababaaaaaab
bbaaabaababaaabbaabbabbb
aaabaabbbbabbbbbababaabb
babaabbbbbbaababaabbbabbabbbabaabbabbaaababbabba
babbbbbabaaabbbaaaaaabab
aaabbbbabbababaaababbbbb
abbbaaaabaaaaababbabbaba
baabaaabbbbabbbbaabbbbaababaaabbabaaabba
ababaababaababaaaaabbbaa
baaabbabaaabbaabbbbbabaaaaaabbaaaaaabaaabaabaabaabaaabbaaabbababaaabbababbaaaaba
baabaabaaaaaaabbabbabaaabbabaabbbbabbbbabbabbaabbbabbbabbaabaabb
aabbbaaabbbabbbbbbbbbbba
aaabaabbaababbbabbabaaaa
aaabbabbabbbbbbaaabbbbbbabbbbaaa
aabbbbaaaabababaaababbbaaaabaaaa
bbaabaabbbbbbabababaababbbbbabaabbbbabaaabbabaab
aaabaabbaabbabbabaaaaaab
baaaaabaababbbabbbbaaaaa
ababbaabaaabaabbabaaaaba
baabaabaabababaababaaabbbbabbabb
baabbbabbbababbaaababaaa
aabaaaabaabaaaabbabababb
babbaababaabaaabaaaabbba
abbaabbbaabbbaaabaaababa
aabbbabbaababbbbbbaababbbbbbbbaaabaaaabb
babbabbaababababbaaaabbbbaaaaaabbaaabbbbababbbabaabababa
baabaaabbababbabbbaababa
babbbabbbbabbbbbabbababa
aabbababbbbbbbbbabbaabab
bbbbbaabaabbabbaabaaaabb
babbbbbbbabaaaabaabbbabbbabaabbbbbababaabbbbaabbabaaabbb
bbabbbbaaaababbabaaaaaab
abaaaabababaabbaababaabb
aaabbbabababbaaaaabaabbaababbbaabaaabbab
aaaabbabbababbbabaabbaab
bbaaaaabbbaabaababbabbba
baaabaaabaabbbbaaabaaabb
aababbbbbbbababbbaaabbbbbbaaabba
aaaabaaabbbbbbbaabaabbab
aabaabbabbbaabbbaabbabbababaabbababbaaabaabaabaaabaaabba
baababaabababababbbbbaba
bbaabaaabaaabbababbababa
abbbaaaaaaababaabaaabbaabaaabbaaaabbaaba
abbabbabbbbaaabaabaababb
babbabbbaabbbaaaaaaababb
bbbabababbaabaabaaabaaaa
bbbabaaabaababbabbaaabbaabaabbaa
baaaaababbbbbaabbbabbabb
baabababbaaabbbabababbaaababbabbabbbbbbb
abbbaabbabaaaaaaabaaaaaaaaabbbbababbaaaaababbababaabbbbbbabbbaababbbbaaa
aaabbabbbaaaaaaabababaababaaaaab
babaaaaaaabbbababbbbabbbabbaabbbaaabbaaaaaaaaaab
aabbbabbbababbaabbbababaabbaabbabaaaaabb
babbaaabbaabbbaabaabbabb
abbaabbaaabababbababbaba
abbbbbabbbbbbbbbbaabbabb
bbbaabbbbabaabaababaababbabbbabaaabaaabb
baabbbbabbbbbbbbbbbbaabbababbabb
aaabbbbaabbabbaaaaaababa
aabaabbabbbaaabababbbbbaaaaaaababaabbaba
abbabbabbaabbbabaaaabbaabaabbabbababbbbbbbaaaaaaaaaababbbbbaaabaaabaaaaabaaaabaa
aaababaaaabbababbaabbbaabaababaaaabaaabaaaaabbaa
baabaaabaaaaaaaaaabaaabbbbbbaaab
abaaabaaaaaaaabbbbaaaaba
babbaaabbbaaabaababbbaba
babbbbbabbaabaababbababbbabbabbabbbbbaba
aaaaaabbbaaaaaaaabaaaabaabbaabbaabbabbbbbbababbbaaaabbbb
bbbaababababbaabbbbabaaa
aaaaabbabbaaaaabaaabbaabbbabbabaababaabbababbaaababbabaabbbaaabbabbbbabb
babaabaaaabbbaaaaabbaaab
bbbbabbbbaaabbbabbbaababaaabbaabbabbbaba
aabaabaaabaaaabbabbabababaaabbabbbaaaabbbbbbaaaaababbaabaaabaabaabbababb
ababbaaaababbaabbaaaabbabababaababbaaabb
abababababbbabbbaabbbaababbabaab
babbbbabbbbababbbbbbbbabbbababbb
aababbbbabaaaabaaabaabab
bbbaaababababbababaababb
bbbabbbbbabbbabbaabaabab
baaababbaaabbbaaabbbabaaabaabaaaaaaabaaaabaababa
bbbbbbbbbbabbbbbbbbbbbabaaabbbaaabbbbaab
babbabbbbbbbabbbbbaaabba
babaaababbbbabaaaaabaaabaababababbabaaab
abaababaababbaaabbabbbbbabbabbab
bbbabbbbaabaaaabbbabaabbaaababbaaababbbbabaaaabbbbbabbbabaaaabab
babbbbbbaaabaabbbbbabbbbbabaabaaabaaabaabaaababa
abbabbababbbbababbabaaab
ababbaaaabaaabaabbaababb
aabaaaabababaaaabbbbaabbabbbaaaaabbaaaab
babaaaaaabbbaaaabababaababbbabbababaabaababbbbaaaabaabab
abaaaaaababbaabaabbaaaaababbaabbbabbbbbbbaaaabbbabaabbabbbabababaaababba
aabbbabababbaabbababbabb
aaabbaaaabaabbbaababaabb
bbaabbbabbbbababaaabbbabbbbbabbabaaaaaabaabbbbaaaaabbaabbaaaaaaa
babaaaabaaabbabbaaabbaba
aabbbbaabbbabbaabbbbbbba
bbaaaaaaabaabbaaaabaaaba
abbbaaabbabbbbbbbbbbabaababaaabbbbaabaaaabbbbbbaabaabbaaabbbababbbbabbba
abbaabbbaabbabababaaaabaabbababbabbbabbb
abbaaabbbbaabaaabbbbabbbbabbbbbbbaababbb
bbabbbbaabbbaaaabbbaababbbababbababbabba
abaaabaaabaabaaabbabbbaa
aaabbbabbbbbababaaabaaba
aabaabbabbbaaaabbabbabba
abbaaabbbbaabaabbababaaa
aabbabababbaaaaaaaaaabbbabababaabbbaaabbbbbaaaaa
aaaabbabbaababaabaaabaab
bababbaaaaabbaaaabbabbbb
abbaabbbabaaababbbbaababbabbaaaaabbbaaababbaaabaabbbbbba
aabbbabaaaabaaabbaaaabaa
bababbaabababbaabaabbaba
bbaabbbbbbbbaaaaabaabbbb
bbbbbbabbabbbbbaabbbbaaa
bababbbabaaabaaabbbabaab
baaaabaaaabbbbabbabbabbaaaaabbaa
bbbbbbabbaabbbabaabbbaab
baabaabaabbbaabbaababbab
aaabbaaabbbbababaabbababbabaabbaabaabbbabbbabaab
baaaaaababbbbbbabbabababbbaaabbbaabaaaababbbabbbaababaabbbaaaaabbaabbbbbabbababb
abbbabbabbaaabaabaaabaab
abaabbbabababbabababaabaabbabbabaabbaaaabbbbaaaa
bbabbabbbbbbaaabaabaababababaabbabababba
abaabbabbababaaabbabbababbabaaaababaaaaaaaaaabaabbbbaabbbbbbabaaaaaababbbbabaabaaababbba
bbaabbaabbbbbbabbabaaaabababaabbabbabbabbabaaabb
abbbaabbbbbaabbaabbbabab
bbbbbaabaaaabaabbaaababbabaaaabbabababbb
aabbbbbabaabaababaaabbaaaabaabbaabababbbaaabbbbb
aaaabaaabbbabababaaabbaaaabbabababbaababaababbaaabaaabba
bbbbabaaababbaaabbabaabbbabbaaaaaaaaaaab
babbaaaababbbbbabbbabababaabaabb
baabababbbbbabbbabbabbba
babaabaaaaabbaaaaaaaaaaa
bbbaaaabbabbaabbbabbbaba
abbaaabababbbaaabbaababb
aaababaabbabaabbbababaaa
baaabbaaababbabbbabaaaaaabaabbbbaaabaabaababbbbbbbaaaabbaabbbaabababbabbababbaaa
bbaabaabbbbababaaabbaabbaaabababbbbabaaaaaaaaaabbaaaaabbababbbbb
aaababbaabababaabbbaaabbbbabbaab
aabbbabaabbbabaabaabaaaa
ababbaaababbaababbabbaba
babbabaabbaaabbbabbbaaaaaabaabababaabaaaabaaabbbabbaabbbbabbabbbabbbaaab
ababbaaaababbaaabbbbaaba
bababbaabaabaaababbaabab
babaabbaaabaabbaabbbbabbaababbbabaaaabaaaababaab
babbbaaaabbbbbabaabaaaabbbabaaaa
abaabaaabababbabbbabaaab
babaabbabbbbabaaabaaaabaabbabbabaaaabbab
aaabaabbaabbbababbabbbbbaaabaaaa
ababaababbbaabababbaaaaabababbbbaabbaaba
aabbbabbabbabaaaabaabbab
bbabbaaabababbaabbababbb
baabbababbababbaaaaabbbbaabbbabaabaabbbbbabaabaabbbbbaaa
aababbbabaaaaaabbaaabaab
bbbbabbbaaaabaaaababaaaabbaaaaaaababbabb
baababbbaabaababbbababbbbbbaababbbbbaaabaaabbababbabaaaaababaaabaaaaabbabbbababb
baababaabbbabbbbbaaaabab
abbaaababbbaaabbbabababb
bbaaaaabbabbaabbababbabb
aabaabbaababaabaaaabbaba
bbbaababaaabbbbaabbaabbbbaaabababbbbbaba
bbaabbbabbaabaabaaaaabaa
aabaaaabbaaabbababaabbbabbbaaabbaabaaabaaaaabbba
babbaaabbaaabbaabbabbabb
bbbaababaaabbbabbabaabab
aaababaabbaaabaaaabaabbaabaabbab
aaababbaabaabaabbaaaaabbbbabbaaaaaaabbababbbaaaabaabbaabaabbaabbbbbabbab
aaaaaaaaabbaabaababbbbbababaababbabbaabbababbbabaaaaaabaabbbabab
baaaaabbabaaaabbaaababbabaabbaababbbbbabaaababbbbbbbbaaaabaaabababbababbabbabaababababab
abaaaaabbaabababbabaaaababbbaaaabbaaaaaa
ababaaaabbbbbaaaababaababaabbabbbbaaabab
bbaaaabbaabbbabbabbaabab
baabaabaababaabaaaabaaba
baabbbabbbaabbaabbababaabbbaaabbbaaaabaabaabbbbbaabbabaaabbababbbbbbbaabbabbaaabababaabb
aaaabaaaabbaaababbabbaba
aabababbaaabbbababaababb
ababaaabababbbabbbabbbab
abbbabbaaaababaabaaabbaaababbbbaaabbabbaaaaaabaabaaabbbbbbaaabbaaaaaabba
baaaabbbbaabbababbabbbabbabaaaba
baabaabaaaaabbabaabaabbbbaaaabbaabaaabbb
abbaabbbababbaaababaaababbbaaababaaaaaabbbababab
aabbbbaaaaaabaababbaaaababaaabbbaabbbaaaabbbbbababbbaabaaaaabbabaaaaaaaa
baaaaaaabababaabababbaba
bababbbaaabbababbbaaaaba
aaababbaaabbabbaababbbbb
aabababbabbbbabaabbabaaaabaabbbabbababbabababbabaaaaabba
abbababbbaabaabbbaabbaaaabaaabbaababbbbbbbbbbabbaababbaabaabaababbbabbabaabbabbbbbaaaabbbbbababb
aabbabbaabaababaaaaaabba
aabbababaaababbaabaabbab
abbbbbaababbaababbababaabbaaaaaabaaabababaaaabbbbbaaabbb
aaaaabbabaababbaaabaabaa
babbbaaabaabbbbababaabbaabaaaaabbbabbbaaabbbabbbbabbbbaa
aaaabaabbabaaaababababba
abbbabbbaaaaabbbbbaabbaa
bbbaaaabbbaabbbababaaabbbbababaabbaaaaaa
aaaabaabbbbaaaabbbbabbab
aababbbbbaabababbbaaabba
baabbbbababbbabbaabbabbabbbababbaaaaabab
bbabbbbabaabbaaabaabbbbb
ababbaabbbababbabbababab
aaabababbbbababbabaaababbbabaaba
aaabababbaaabbbabbabbabb
bbbbbbabaabaaaabbbaaabab
abbabbaabbbabbaaabbaabbbaabaababaababbab
abbaabbababbaaaaabbaabbaaabaabbaaabbaaba
ababbbabbaababbbbabbbbaaaabbaaabaaaaaaab
baabbbbaaaababbbaabbbbbaaabaaaaa
bbbababababbaabaaaaaabaa
baabababbbbaabbababbbbbaaaababbaabaabbbaaabbabaabbaabbbb
aabbbaaabbbbbaabaaabbaba
babbbabbaabbaabbbaabbaab
bbbabaabbbbaabbaaaabbabbaaabababbbabbaaaabbbaabbbaaabaaababababb
bbbaaaabbbabbbbabbbabbba
aabbbabababaaaaabbbabbaaaabaaaba
bababbaababababaabaaaabb
bbbaaabbbbbaabbabbbbbbaabbaabbbb
abbbaabbbababaabbbaaaaba
abababaabaaabbbabaaabbabbabaaaabbbaaabab
bbbabbbbbbbaaaaabbbbababbbabaaabababbbbb
abaaaaaaababbaababbaaabaabbaaaab
bababaababbbabbabbabaaba
babbaababababaabbbbbbbbbabbababbbababbbb
bbbaaabbbbababaababbbaba
aaabbbbaabbbababbababaaaaaabbbbaababbbbbabaaababbbabbbaaaaaaaabaaaaaabaa
bbaabbbabbbbbbaaaaaaaaab
baaabbbabbbaaaaaaabbaaaa
aaaabaaaaabaabbaabbabbbb
abbbbabbbaababaaabababbbbaaabaabaaaaabaabbbbabbaabbabbbb
aaaabaabbbababbababbaabbbbabaabbbbbbaaab
bbbbbaaabbbaababbbbababbbbabaabbaabbbbba
aaabbbbababbbabbbbbaababbbbbbbbbbbabaabbaaaaabaa
aabbbabaababaaabbabbbaba
bbbaababbbbbbbbbabaabbaa
ababaaababbbbbabaaaaabab
bbbababbbababbbaabbababa
bababbbaabbbabbababbabaa
bbbababaabaaaabaaaaabbbb
ababaaabbbbaaaabbbabaaba
aaababaabbbaaabbbbbaaaababbabbbb
babbbbabbababbaaababaaaaabaababbabbbabbb
bababbabbabbabbbaabbababbaabbaaaaabbbaabaabbaabbbbaaabbaabbabbbabbbbbaab
babbaababaaabbaaababaaaabbbaabaa
bbabbbbabaabababbaaabaab
abbbaaabaaababbaabaabbab
bbbababbbbbabbbbbbabbabb
bbbbbaababaaaabaababaabb
abbabaaaabbbaaaababbbbab
ababbbabaaabbbabaabbbbaaaaabbbbbaabaaaba
bbaaabaaaaababaaabaabbbb
abaaabaababaaabbbaaabbaabbbbabaabbabbaab
bbbbbababbabaababaababbbaabbaabaaabaaaaaaabbbbba
aabbbabbabbaaababbababaabbbabababaaaaaaaaabaabaabaababba
abaaaababbbbbbababaabbbabbbaaaaaababbabb
babbbbbaaaaabbabbaaaaabb
aaabaababbaabbaaabbbbbabbbbababbaabbbbbababbbaab
abbabaaabbbabbaababbaabbaabbbbba
babaaabaabbbabbaaaaabbaa
baabbbbabaaaaababbbaabbbaaaabbbb
aabbaabbbbbaaaabbbbabbaaabbabbababbbbaababaababb
abaaaabbbbaaababbbbbbabb
abaaaabaababbbabaabaaabb
abaababbaabaababbaaabbbb
bbabbabbabababbaaaabbabaabababab
aaaaaabbbabaaaabbbbbbbaabaaaaabbaababbabbabbbababaaaabba
bbababbabaaababbababbbbbbabbabab
bbabbaaababbbbaababbaaab
baaaaaaaaabababbaabaabaa
abbaaabbabbbaaaababaaabaababaabaababaabb
abaaaaabaaababbaaaabaaab
abaaaaaabbaabaaaaaabbaabababbbaaabbbabbbbaabbaab
abbaaabbbbaabbaaaabbbaaabaabaaaa
aabaaaabbbbaaaabaaababbb
abbaabaabbbbababbabbaaababaaabbaaabaaaabbabababababababb
⛄"""
