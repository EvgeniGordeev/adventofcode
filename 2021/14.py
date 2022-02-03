#!/usr/bin/env python3

# INPUT
import re
from collections import Counter
from functools import cache


def parser(text) -> tuple:
    template, rules = text.strip().split('\n\n')
    return template, {k: v for k, v in sorted(re.findall(r'(.*) -> (.*)', rules))}


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN
# brute-force
def run_bf(template: str, rules: dict) -> str:
    res = []
    for i in range(1, len(template)):
        window = template[i - 1:i + 1]
        res.append(template[i - 1])
        res.append(rules[window])
    res.append(template[-1])

    return ''.join(res)


class FrozenDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


@cache
def run(template: str, rules: FrozenDict, step: int, root=True) -> FrozenDict:
    if step == 0:
        return FrozenDict(Counter(template[:-1]))
    res = Counter()
    for i in range(1, len(template)):
        window = template[i - 1:i + 1]
        insert = rules[window]
        new_inner = template[i - 1] + insert + template[i]
        inner_res = run(new_inner, rules, step - 1, False)
        res += Counter(inner_res)
    if root:
        res += Counter(template[-1])
    return FrozenDict(res)


def part1(template: str, rules: dict, steps=10) -> int:
    return part2(template, rules, steps)


def part2(template: str, rules: dict, steps=40) -> int:
    counter = run(template, FrozenDict(rules), steps)
    char_count = counter.values()
    return max(char_count) - min(char_count)


# TEST
def test():
    # GIVEN
    sample_input = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
    given = parser(sample_input)
    assert run_bf('NNCB', given[1]) == 'NCNBCHB'
    assert run_bf('NCNBCHB', given[1]) == 'NBCCNBBBCBHCB'
    assert run_bf('NBCCNBBBCBHCB', given[1]) == 'NBBBCNCCNBBNBNBBCHBHHBCHB'
    assert run_bf('NBBBCNCCNBBNBNBBCHBHHBCHB', given[1]) == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    assert part1(*given) == 1588
    # part 2
    assert run_bf(run_bf('NN', given[1]), given[1]) == 'NBCCN'
    rules_t = FrozenDict(given[1])
    assert run('NN', rules_t, 2) == Counter('NBCCN')
    assert run('NNCB', rules_t, 4) == Counter('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')
    assert part2(*given) == 2188189693529
    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    part_1 = part1(*input_)
    print(part_1)
    assert part_1 == 3048
    # TWO #2
    part_2 = part2(*input_)
    print(part_2)
    assert part_2 == 3_288_891_573_057

# INPUT
"""🎅
PKHOVVOSCNVHHCVVCBOH

NO -> B
PV -> P
OC -> K
SC -> K
FK -> P
PO -> P
FC -> V
KN -> V
CN -> O
CB -> K
NF -> K
CO -> F
SK -> F
VO -> B
SF -> F
PB -> F
FF -> C
HC -> P
PF -> B
OP -> B
OO -> V
OK -> N
KB -> H
PN -> V
PP -> N
FV -> S
BO -> O
HN -> C
FP -> F
BP -> B
HB -> N
VC -> F
PC -> V
FO -> O
OH -> S
FH -> B
HK -> B
BC -> F
ON -> K
FN -> N
NN -> O
PH -> P
KS -> H
HV -> F
BK -> O
NP -> S
CC -> H
KV -> V
NB -> C
NS -> S
KO -> V
NK -> H
HO -> C
KC -> P
VH -> C
VK -> O
CP -> K
BS -> N
BB -> F
VV -> K
SH -> O
SO -> N
VF -> K
NV -> K
SV -> O
NH -> C
VS -> N
OF -> N
SP -> C
HP -> O
NC -> V
KP -> B
KH -> O
SN -> S
CS -> N
FB -> P
OB -> H
VP -> B
CH -> O
BF -> B
PK -> S
CF -> V
CV -> S
VB -> P
CK -> H
PS -> N
SS -> C
OS -> P
OV -> F
VN -> V
BV -> V
HF -> B
FS -> O
BN -> K
SB -> N
HH -> S
BH -> S
KK -> H
HS -> K
KF -> V
⛄"""
