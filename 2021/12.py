#!/usr/bin/env python3

# INPUT
import string


def parser(text) -> tuple:
    return text.strip().splitlines()


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


# MAIN
class Node:
    def __init__(self, val, children: set = None):
        self.val = val
        if not children:
            self.children = set()

    def __hash__(self):
        return hash(self.val)

    def __repr__(self):
        return self.val


def to_tree(lines):
    map = {}
    for link in lines:
        n1, n2 = link.split('-')
        if n1 not in map:
            map[n1] = Node(n1)
        if n2 not in map:
            map[n2] = Node(n2)
        # fix path according to start and end logic
        if n2 == 'start' or n1 == 'end':
            n1, n2 = n2, n1
        map[n1].children.add(map[n2])
        if n1 != 'start' and n2 != 'end':
            map[n2].children.add(map[n1])
    return map


def part1(lines) -> int:
    def dfs(root: Node, path: str, paths: set):
        leaf = root.val
        if leaf == 'end':
            path += 'end'
            paths.add(path)
            return
        # small cave already visited
        if leaf[0] in string.ascii_lowercase and leaf in path:
            return
        path += leaf + ','
        for child in root.children:
            dfs(child, path, paths)

    map = to_tree(lines)
    paths = set()
    dfs(map['start'], '', paths)
    return len(paths)


def part2(lines) -> int:
    def dfs(root: Node, path: str, paths: set, allow_double_visit=True):
        leaf = root.val
        if leaf == 'end':
            paths.add(path)
            return
        # single small caves allow 2 visits, other small ones 1 visit
        if leaf[0] in string.ascii_lowercase and leaf in path:
            if allow_double_visit:
                allow_double_visit = False
            else:
                return
        path += leaf
        for child in root.children:
            dfs(child, path, paths, allow_double_visit)

    map = to_tree(lines)
    paths = set()
    dfs(map['start'], '', paths)
    return len(paths)


# TEST
def test():
    # GIVEN
    sample_input = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
    given = parser(sample_input)
    assert part1(given) == 10
    sample_input2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""
    given2 = parser(sample_input2)
    assert part1(given2) == 19
    given3 = parser("""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
    """)
    assert part1(given3) == 226
    # part 2
    assert part2(given) == 36
    assert part2(given2) == 103
    assert part2(given3) == 3509
    return True


if __name__ == '__main__':
    assert test()
    input_ = parser(read_input())
    # ONE #1
    part_1 = part1(input_)
    print(part_1)
    assert part_1 == 5157
    # TWO #2
    part_2 = part2(input_)
    print(part_2)
    assert part_2 == 144309

# INPUT
"""🎅
TR-start
xx-JT
xx-TR
hc-dd
ab-JT
hc-end
dd-JT
ab-dd
TR-ab
vh-xx
hc-JT
TR-vh
xx-start
hc-ME
vh-dd
JT-bm
end-ab
dd-xx
end-TR
hc-TR
start-vh
⛄"""
