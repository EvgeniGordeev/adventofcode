#!/usr/bin/env python3
from collections import namedtuple


# HELPER FUNCTIONS
def parser(text) -> list:
    return [int(s) for s in text.strip()]


def read_input() -> str:
    with open(__file__, "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return data


# SANDBOX
Move = namedtuple("Move", "in_cups move current pick_up dest cups")


def _log(move: Move):
    message = """
-- move %s --
cups: %s 
pick up: %s
destination: %s
""" % (
        move.move + 1, " ".join([f"({c})" if c == move.current else str(c) for c in move.in_cups]), ", ".join([str(c) for c in move.pick_up]),
        move.dest)
    print(message)
    return message


def run_move_bruteforce(move: int, cups: list) -> Move:
    size = len(cups)
    move_index = move % size
    # actual move
    current = cups[move % len(cups)]
    start_pick_up, end_pick_up = (move_index + 1) % size, (move_index + 4) % size
    pick_up = cups[start_pick_up:end_pick_up if end_pick_up > start_pick_up else size] + cups[0:0 if end_pick_up > start_pick_up else end_pick_up]
    new_cups = [c for c in cups if c not in pick_up]
    dest = current - 1
    while dest in pick_up:
        dest = dest - 1
    if dest not in new_cups:
        dest = max(new_cups)

    dest_ind = new_cups.index(dest)
    new_cups[dest_ind + 1:dest_ind + 1] = pick_up

    curr_index = new_cups.index(current)
    if curr_index != move_index:
        # we need to maintain clockwise insertion, i.e. index of current cup must not change
        new_cups = new_cups[curr_index - move_index:size] + new_cups[0:curr_index - move_index]
    # logging info
    move_details = Move(cups, move, current, pick_up, dest, new_cups)
    # _log(move_details)
    return move_details


def _collect_part1(cups: list) -> int:
    index_of_one, size = cups.index(1), len(cups)
    index_of_one = index_of_one + 1 if index_of_one + 1 < size else 0
    result = cups[index_of_one:len(cups)] + cups[0:index_of_one]
    return int("".join(str(n) for n in result[0:-1]))


def part1_sandbox(cups: list, rounds: int = 100) -> int:
    for i in range(rounds):
        # start = cups.copy()
        cups = run_move_bruteforce(i, cups).cups
        # print(f"{i}:{start}->{cups}={_collect_part1(cups)}")
    return _collect_part1(cups)


# MAIN FUNCTIONS
class Node(object):
    __slots__ = ('val', 'next')

    def __init__(self, val):
        self.val = val
        self.next = None

    def __repr__(self):
        return f"Node({self.val})"


def _log_node_list(node: Node, forward=9):
    return [val for _ in range(forward) if (_, val := node.val, node := node.next) != (None, None, None)]


def to_linked_dict(cups: list, limit: int) -> dict:
    nodes, last = {}, None
    for c in range(limit, max(cups), -1):
        current = Node(c)
        current.next = last
        nodes[c] = current
        last = current

    for c in reversed(cups):
        current = Node(c)
        current.next = last
        nodes[c] = current
        last = current
    head, tail = cups[0], limit if limit > len(cups) else cups[-1]
    # close the circle - last points to first
    nodes[tail].next = nodes[head]
    return nodes


def part1(cups: list, rounds: int = 100) -> int:
    nodes = to_linked_dict(cups, 9)
    head = nodes[cups[0]]
    # print(f"{0}:{_log_node_list(head)}")
    for _ in range(rounds):
        head = run_move(head, nodes)
        # print(f"{_ + 1}:{_log_node_list(head)}")
    node_list = _log_node_list(nodes[1])
    return int("".join(str(n) for n in node_list[1:]))


def part2(cups: list, limit: int = int(1e6), rounds: int = int(1e7)) -> int:
    nodes = to_linked_dict(cups, limit)
    head = nodes[cups[0]]
    # print(f"{0}:{_log_node_list(head)}")
    for stepno in range(rounds):
        head = run_move(head, nodes)
        if stepno % 500000 == 0:
            # print(stepno)
            pass
        # print(f"{_ + 1}:{_log_node_list(head)}")

    a, b = nodes[1].next.val, nodes[1].next.next.val
    return a * b


def run_move(head, nodes):
    size = len(nodes)

    pickup_start = head.next
    pickup_end = head.next.next.next
    pick_up_vals = {pickup_start.val, pickup_start.next.val, pickup_end.val}

    dest = head.val - 1 if head.val > 1 else size
    while dest in pick_up_vals:
        dest -= 1
        if dest < 1:
            dest = size

    dest_node = nodes[dest]

    head.next = pickup_end.next
    pickup_end.next = dest_node.next
    dest_node.next = pickup_start
    head = head.next

    # a = head.next
    # b = a.next
    # c = b.next
    #
    # look = head.val
    # while True:
    #     look -= 1
    #     if look == 0:
    #         look = size
    #     if look not in (a.val, b.val, c.val):
    #         break
    #
    # after = nodes[look]
    # head.next, head, after.next, c.next = c.next, c.next, a, after.next

    return head


# TEST
def test() -> bool:
    given = parser("""
389125467
""")
    assert given == [3, 8, 9, 1, 2, 5, 4, 6, 7]
    # move = run_move_bruteforce(0, given)
    # assert move == Move(in_cups=[3, 8, 9, 1, 2, 5, 4, 6, 7], move=0, current=3, pick_up=[8, 9, 1], dest=2, cups=[3, 2, 8, 9, 1, 5, 4, 6, 7])
    # move = run_move_bruteforce(1, move.cups)
    # assert move == Move(in_cups=[3, 2, 8, 9, 1, 5, 4, 6, 7], move=1, current=2, pick_up=[8, 9, 1], dest=7, cups=[3, 2, 5, 4, 6, 7, 8, 9, 1])
    # move = run_move_bruteforce(2, move.cups)
    # assert move == Move(in_cups=[3, 2, 5, 4, 6, 7, 8, 9, 1], move=2, current=5, pick_up=[4, 6, 7], dest=3, cups=[7, 2, 5, 8, 9, 1, 3, 4, 6])
    # move = run_move_bruteforce(3, move.cups)
    # assert move == Move(in_cups=[7, 2, 5, 8, 9, 1, 3, 4, 6], move=3, current=8, pick_up=[9, 1, 3], dest=7, cups=[3, 2, 5, 8, 4, 6, 7, 9, 1])
    # move = run_move_bruteforce(4, move.cups)
    # assert move == Move(in_cups=[3, 2, 5, 8, 4, 6, 7, 9, 1], move=4, current=4, pick_up=[6, 7, 9], dest=3, cups=[9, 2, 5, 8, 4, 1, 3, 6, 7])
    # move = run_move_bruteforce(5, move.cups)
    # assert move == Move(in_cups=[9, 2, 5, 8, 4, 1, 3, 6, 7], move=5, current=1, pick_up=[3, 6, 7], dest=9, cups=[7, 2, 5, 8, 4, 1, 9, 3, 6])
    # move = run_move_bruteforce(6, move.cups)
    # assert move == Move(in_cups=[7, 2, 5, 8, 4, 1, 9, 3, 6], move=6, current=9, pick_up=[3, 6, 7], dest=8, cups=[8, 3, 6, 7, 4, 1, 9, 2, 5])
    # move = run_move_bruteforce(7, move.cups)
    # assert move == Move(in_cups=[8, 3, 6, 7, 4, 1, 9, 2, 5], move=7, current=2, pick_up=[5, 8, 3], dest=1, cups=[7, 4, 1, 5, 8, 3, 9, 2, 6])
    # move = run_move_bruteforce(8, move.cups)
    # assert move == Move(in_cups=[7, 4, 1, 5, 8, 3, 9, 2, 6], move=8, current=6, pick_up=[7, 4, 1], dest=5, cups=[5, 7, 4, 1, 8, 3, 9, 2, 6])
    # move = run_move_bruteforce(9, move.cups)
    # assert move == Move(in_cups=[5, 7, 4, 1, 8, 3, 9, 2, 6], move=9, current=5, pick_up=[7, 4, 1], dest=3, cups=[5, 8, 3, 7, 4, 1, 9, 2, 6])
    # assert _collect_part1(move.cups) == 92658374
    assert part1(parser("389125467"), 10) == 92658374
    assert part1(parser("389125467"), 30) == 35298467
    assert part1(parser("389125467"), 100) == 67384529
    # part 2
    assert part2(parser("389125467"), 9, 10) == 18
    assert part2(parser("389125467")) == 149245887792
    return True


if __name__ == '__main__':
    # assert test()

    input = parser(read_input())
    # ONE #1
    part_1 = part1(input)
    print(part_1)
    assert part_1 == 74698532
    # TWO #2
    part_2 = part2(input)
    print(part_2)
    assert part_2 == 286194102744

# INPUT
"""🎅
624397158
⛄"""
