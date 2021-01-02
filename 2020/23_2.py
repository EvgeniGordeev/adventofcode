class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def part1(s):
    cups = list([int(x) for x in s])
    for _ in range(int(1e2)):
        pick_up = cups[1:4]
        dest = cups[0] - 1 if cups[0] > 1 else 9
        while dest in pick_up:
            dest -= 1
            if dest == 0:
                dest = 9

        idx = cups.index(dest)
        if idx == 0:
            # no change
            pass
        else:
            cups = list([cups[0]] + cups[4: idx + 1] + pick_up + cups[idx + 1:])

        cups = cups[1:] + [cups[0]]

    print(cups)


def part2(s):
    N = int(1e6)
    nodes = {}
    for c in range(1, N + 1):
        nodes[c] = Node(c)

    for x, y in zip(s, s[1:]):
        x, y = map(int, [x, y])
        nodes[x].next = nodes[y]

    if len(s) == N:
        nodes[int(s[-1])].next = nodes[int(s[0])]
    else:
        nodes[int(s[-1])].next = nodes[len(s) + 1]
        for i in range(len(s) + 1, N):
            nodes[i].next = nodes[i + 1]
        nodes[N].next = nodes[int(s[0])]

    head = nodes[int(s[0])]
    for _ in range(int(1e7)):
        rem_start = head.next
        rem_end = head.next.next.next

        vals = [rem_start.val, rem_start.next.val, rem_end.val]
        goal = head.val - 1 if head.val > 1 else N
        while goal in vals:
            goal -= 1
            if goal == 0:
                goal = N

        head.next = rem_end.next
        rem_end.next = nodes[goal].next
        nodes[goal].next = rem_start

        head = head.next

    a, b = nodes[1].next.val, nodes[1].next.next.val
    print(a, b, a * b)


def main():
    part1("624397158")
    # part2(s)


main()
