#!/usr/bin/env python3

# INPUT
import copy
import sys
from functools import cache

import numpy as np
from scipy import ndimage
from scipy.ndimage import convolve


def parser(text) -> tuple:
    return text.strip().split('\n\n')


def read_input() -> str:
    with open(__file__, encoding="utf-8") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].strip()
    return data


def print_debug(pixels):
    print('===<OUTPUT>===')
    (x1, x2), (y1, y2) = ((min(d), max(d)) for d in zip(*pixels))
    for y in range(y1, y2 + 1):
        print("".join(("#" if (x, y) in pixels else ".") for x in range(x1, x2 + 1)))
    print('===</OUTPUT>===')


# MAIN
def get_3x3_code(pixels: set, pos: tuple) -> int:
    square = [(pos[0] + r, pos[1] + c) for r in (-1, 0, 1) for c in (-1, 0, 1)]
    code = ''.join('1' if pix in pixels else '0' for pix in square)
    return int(code, 2)


# original solution, but flashing was not taken into account
def part1(algo_str, image, enhance_steps=2) -> int:
    algo = {i for i, ch in enumerate(algo_str) if ch == '#'}
    output_image = {(x, y) for x, row in enumerate(image.split("\n")) for y, cell in enumerate(row) if cell == '#'}
    for _ in range(enhance_steps):
        (x1, x2), (y1, y2) = ((min(d), max(d)) for d in zip(*output_image))
        output_image = {(row, col) for row in range(x1 - 1, x2 + 2) for col in range(y1 - 1, y2 + 2)
                        if get_3x3_code(output_image, (row, col)) in algo}
    # print_debug(output_image)
    return len(output_image)


# IMPORTED solutions
# 2.216 s
def part1_v2(algo_string, image, enhance_steps=2):
    if algo_string[0] == ".":
        algo = [
            {i for i, p in enumerate(algo_string) if p == "#"},
        ]
    elif algo_string[-1] == ".":
        algo = [
            {i for i, p in enumerate(algo_string) if p == "."},
            {i ^ 511 for i, p in enumerate(algo_string) if p == "#"},
        ]
    else:
        print("Infinity")
        sys.exit()

    image = {(x, y) for y, line in enumerate(image.split("\n")) for x, p in enumerate(line) if p == "#"}

    for i in range(enhance_steps):
        (x1, x2), (y1, y2) = ((min(d), max(d)) for d in zip(*image))
        image = {(x, y) for x in range(x1 - 1, x2 + 2) for y in range(y1 - 1, y2 + 2) if
                 sum(1 << (8 - z) for z in range(9) if (x - 1 + z % 3, y - 1 + z // 3) in image) in algo[i % len(algo)]}

    # print_debug(image)
    return len(image)


#  7.063 s
def part1_v3(algo_str, image, enhance_steps=2):
    M = [c == '#' for c in algo_str]
    C = {(x, y): c == '#' for y, l in enumerate(image.splitlines()) for x, c in enumerate(l)}
    Z = [-1, 0, 1]
    v = lambda C, x, y, z: M[sum(C.get((x + a, y + b), z) * 2 ** (4 - 3 * b - a) for b in Z for a in Z)]

    def F(C, i, z=0):
        for _ in range(i):
            p, q = [range(a - 2, b + 2) for a, b in zip(min(C), max(C))]
            C = {(x, y): v(C, x, y, z) for x in p for y in q}
            z = M[2 ** (9 * z) - 1]
        return sum(C.values())

    return F(C, enhance_steps)


# 1.779 s
def part1_v4(algo_str, image, enhance_steps=2):
    decode = np.fromiter((True if char == '#' else False for char in algo_str), dtype=bool,
                         count=len(algo_str))

    input_array = np.array([[True if char == '#' else False for char in line]
                            for line in image.split('\n') if line.strip()]).astype(bool)

    def decode_image(subarray: np.array):
        # astype of numpy had bad performance
        return decode[int(''.join('1' if bool_ else '0' for bool_ in subarray), 2)]

    # initial pad of False value
    output = np.pad(input_array, 1, mode='constant', constant_values=False)
    for i in range(enhance_steps):
        # expand edge/nearest to account for possibility of decode[0]==True
        output = ndimage.generic_filter(np.pad(output, 1, mode='edge'), decode_image, size=(3, 3), mode='nearest')

    return np.count_nonzero(output)


# 715.0 ms
def part1_v5(algo_str, image, enhance_steps=2):
    class Board:
        def __init__(self, rules, lines):
            self.bitmap = [1 if c == '#' else 0 for c in rules]
            self.size = len(lines)
            self.ofs = 52
            self.dflt = 0
            self.board = []
            for y in range(self.ofs):
                self.board.append([0] * (self.size + self.ofs * 2))
            for y in range(len(lines)):
                self.board.append([])
                self.board[self.ofs + y].extend([0] * self.ofs)
                for x in range(len(lines[y])):
                    self.board[self.ofs + y].append(1 if lines[y][x] == '#' else 0)
                self.board[self.ofs + y].extend([0] * self.ofs)
            for y in range(self.ofs):
                self.board.append([0] * (self.size + self.ofs * 2))
            self.old = copy.deepcopy(self.board)

        def iter(self):
            ndflt = self.bitmap[0] if self.dflt == 0 else self.bitmap[-1]
            total = 0
            (self.old, self.board) = (self.board, self.old)
            self.ofs -= 1
            self.size += 2
            for x in range(self.ofs - 1, self.ofs + self.size + 2):
                self.old[self.ofs - 1][x] = self.old[self.ofs][x] = self.dflt
                self.old[self.ofs + self.size - 1][x] = self.old[self.ofs + self.size][x] = self.dflt
            for y in range(self.ofs - 1, self.ofs + self.size + 2):
                self.old[y][self.ofs - 1] = self.old[y][self.ofs] = self.dflt
                self.old[y][self.ofs + self.size - 1] = self.old[y][self.ofs + self.size] = self.dflt
            for x in range(self.ofs, self.ofs + self.size):
                pval = 0 if self.dflt == 0 else 63
                for y in range(self.ofs, self.ofs + self.size):
                    fval = (pval & 63) * 8 + self.old[y + 1][x - 1] * 4 + self.old[y + 1][x] * 2 + self.old[y + 1][
                        x + 1]
                    pval = fval
                    nbit = self.bitmap[fval]
                    total += nbit
                    self.board[y][x] = nbit
            self.dflt = ndflt
            return total

    board = Board(algo_str, image.splitlines())
    ans = 0
    for _ in range(enhance_steps):
        ans = board.iter()
    return ans


# 348.3 ms
def part1_v6(algo_str, image, enhance_steps=2):
    algo = tuple([1 if c == '#' else 0 for c in algo_str])
    img_arr = np.array([[1 if c == '#' else 0 for c in l] for l in image.splitlines()])

    # Create the vectorized + cached decode function
    @np.vectorize
    @cache
    def decode(num):
        return algo[num]

    # Here we create a convolution filter that maps bit values to each pixel
    convolution_filter = np.array([2 ** i for i in range(9)]).reshape(3, 3)

    # Padding the array to max expected size
    img_filtered = np.pad(img_arr, enhance_steps)
    # Iterating
    for _ in range(enhance_steps):
        img_filtered = decode(convolve(img_filtered, convolution_filter))
    ans = img_filtered.sum().sum()
    return ans


# 199 ms
def part1_v7(algo_str, image, enhance_steps=2):
    algorithm = np.array([1 if x == '#' else 0 for x in algo_str], dtype=np.uint8)
    img_in = np.array([[1 if x == '#' else 0 for x in row] for row in image.splitlines()], dtype=np.uint8)

    def enhance(img, num_of_steps=2, fill_value=0, pad_size=2):
        for steps in range(num_of_steps):
            img = np.pad(img, pad_size, constant_values=fill_value)
            rows, cols = img.shape

            stride_rows = rows - pad_size
            stride_cols = cols - pad_size
            stride_shape = stride_rows, stride_cols, 3, 3
            stride = np.lib.stride_tricks.as_strided(img, stride_shape, 2 * img.strides)
            stride = np.reshape(stride, (stride_rows, stride_cols, 9))

            codes = stride[:, :, 0] * 256 + np.packbits(stride[:, :, 1:]).reshape(stride_rows, stride_cols)

            img = algorithm[codes]

            fill_value = algorithm[fill_value * 511]

        return img

    return np.sum(enhance(img_in, num_of_steps=enhance_steps))


def part2(algo, image, fun) -> int:
    return fun(algo, image, 50)


# TEST
def test(fun1):
    # GIVEN
    sample_input = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
    one, two = sample_input.split('\n\n')
    one = one.replace('\n', '')
    given = parser(f"{one}\n\n{two}")
    assert fun1(*given) == 35
    # part 2
    assert part2(*given, fun1) == 3351
    return True


if __name__ == '__main__':
    fun1 = part1_v7
    assert test(fun1)
    input_ = parser(read_input())
    # ONE #1
    part_1 = fun1(*input_)
    # 4962 is too low, 5216 is too high
    print(part_1)
    assert part_1 == 4968
    # TWO #2
    part_2 = part2(*input_, fun1)
    print(part_2)
    assert part_2 == 16793

# INPUT
"""🎅
##..#.#...##.####..#..###.#.#.#.#.####.#.##.....#####.##..#..#.#.##.......##.##.#.#...#....#.####..#.##.##....###..##.#####.##....##.#.#.#.#....####...##.#......#.#..##......##..#..###.#..####.###...##.#.##.#..##.##..#.#.#..###..##.####.#.#.#..#.##...#..##...##.#####..##.##..#...#..###.#.#...#..#..##...#.#..........#...#...#.#.#.#..#.###..##....####..#######.##.#.....#.#.###...##...###...#.##.##.##..#......#.###...#.#.#.#...##.#.#.##.#..###.#...##...##.......####.##..#.#....#.#####..#..#####.#.....#....#.#.

.##.#...##..##.#..........#####..#.##..######.##..#....#..#####.#.#####.#..#...#..#####..#.......##.
.#.#.#.#####..##.#.###..#.##.##.......#.####.#............#.#....####..#.#####.##.##.#.###..#..##...
.##.#.#...##....#.#..#...........##.#.#..#####...#..##.###..##.###..........#####..##..##.#.####....
##..####.####.###.......#....#.#####.##...#....###...##...###...#...##..####....####..#####..##..###
...###.##.....#......###.#.###..#..###...#.#..#.#######.##..#..#..#..##.##..#####.#####.###...#.###.
##.###.#....##..####.#..#.###.##.#.##..#...#...###.###.#..#..#.#.###.##.#..###.#.###....###.###.....
#.#.##..#.....#.....##....######...#........#.#.#.#.######..#...##.#.######...#.##########..#.###..#
.##.#...##.#......###..####.##.#...#..##.#.####...##..####..#####..##.###.#.###...#.#.######.#.#####
..#..##..#.#.#...####..###.#..#...#..#.#.#.#.###..####.#...#......#..#..####.#...#.#.#......#...#..#
#...###..#.#.###.#.##.##.#.#.#####....#....#.....#####...#..#..#.#####..##.....#..###.#..###.#..#...
..##.#.#..##.#.#...#...#.#.#..#.#.##....#####....#.##...#..#..#.#....###...##..#.#.##.##.#.......#.#
##.##.#######.###.#..#....#..##..#.###.....#.###..#.#..#....#.#..###.##.#.....#.#.#.##.#...#..##.#..
.....#.#.#.#.####.#..####.#....##.###.###...########.#.#....#..##.#.#####...##....##....#.......#.#.
##..#...#..#.#.####..#.#..####.#####.#####.###..#.#####.#..#...##.######.###.#..#.##.#.#..#..#.####.
#.##.##.#.####...#.#.#.#..####.#.#...###...#.#....##...####.#..#####.#.####.#..#.....###.#..#...#.#.
.#..#.##...####...##.####...###..####.##........#.#.##..#..#.##...#....##.#.#..#.#.###...##.......#.
..#..#..#.###.##...###....#.#..#..##..#...###.###...#..#.....#..#.####.#.#.#.##..###...#....##.#.###
###.##....##.#.##..####.#.###...###.###.#####..##.###.....#.#####....#.##..##.#####.##..###....#....
###..#...###..#....#..#.#...#....###.#.####.##..#.#..#.###..#..#.##.#.#.......#...#....#...###..#.##
#...#.#.#...#.####.##.#.#..#...##.....#..##....#..#.##..##.####.#.#.###..##..#.#.#.###.#.#..####..##
.###..###.##..###..#..#.##..#...#.##.#.......####.#..##.#...#.##..#..........##..####..##.###..###..
###.#.#...###..#...#####.####..#..#######.#.#.###.##.###.#.####.##.#####..###.#####.#...####.##..##.
.##..##..##.#...######.###...#.##.##....##.#...##.#####.#...##..#.#...#.#..#.##.#....##.####.#.##.#.
...####..#...#...####.#.#...#...###..#.##...####.#..######.##.....##..#...#...####.###.#..##.##..#..
#.#####.##.##..#..##.#.####..##.#.#...#..####.##..###.####.##.##...#.#...#.#.#####.####.#.###..#..#.
..#.....#..##..#...#####..##.###..##.#..##..##..####.#..#.####.###...#####.#.###.....#..#.####.#.##.
#####....###..##.#.######.#.##..##.#.#####.##########.#...##...###....###.#.....#.....###.#.#.#.##.#
##.....#.###.###.#.##.########....##.##.###...#######..##..#.#.#..#.##..####..#.###.#.###.#.#......#
..##..#...#.#.#.#.###.#..#####.#.#..#......####..#.###..###...##...##.##..#..#..#.##.#..###..##.#.#.
.#.#..#..###.##.#.#...#.#...##...#.###..#.#.##.#....#..####..#.#.##.#..#...##.#.....##...####.....#.
##.#..##...#..##.####.##....##..#####.###...#..######..#....#..#######..#..#.####.#...##.##..##..#..
..##.#.###....#..#.....#..#.#.#.#........#..##.#.#.......####.##...#.#.##.######..##..#....#.#......
.....#....#.#.##...#..######.###.###.##....##.#.##.###.....#..#.#....#####.#..##.#.....#..#.##....##
##.....#.#...####...##.##.#.##.#.##......#.#########.#.##..##...###.##.#..#....#..##.####..#######..
##...#.########.###.#....#...#..##.##.###....##...#####..##.####..##..#..#####.#..######.####...#.#.
##.####..##.#####..#..###...##.......#...#.###.#.#..#..#....#.#..##.....#.#....####.###...#.#..##.#.
#.#.#.#.###..#.#####.#...##...#.###.##..#.#####.....#...#.#.#..#...##....#...####.####.##.#.....####
..###.##.#......#######..#...##..###.##....#....#.#..###...#..###.#.#...#..##...####.###.###..#.#.##
.#..#.#.##..###########.#.#..#.###.######...###.##..#.###..##.#...#.#...###.#.##.##.#..#..#..#.#...#
.#..#.#..##....#....####.#..##....#.###.####..#.##.#.#..###.#.##.#........##.#...###.#.......##.#...
...###.#.#.##.##.##.....#.#.#..#..#.##.#######...##....#.#......##....##.#.####.####.###.#....##..#.
.#.##..#.##.##.####.....##...#..###.###.###..#..##.####..##...#.###.##..##..#####.#..###....###.##.#
#.###...#####.#..#.####...##.#..#...######.....#.#....##.#.#...##....#...........##.##.##.#...######
##..#..##.....##..#.#..##.##.#..#...####.######.......###..#..##.##..##..##..###..##.##.#.#.....#...
#......###..#####..#######.#.#..#.###..##.#..##.##.##.#..###.###..##.##.....#.#..####.#.##...##..###
.##...#..###..##..#.#####.#####.###...#.........#.##.##.###.#.#.#...###.#..###.##.##.#..#..#...###.#
#.###.###.###.#.###.#.##....##..##.......#....##.###.###.#.###..#..###.#.##.##..#.#...######.####..#
..#####.###.##.#..##.##.#..#.###..#.####....#...##.#.......#.#..##.#.......##.##.#######...######.##
#.##...###..#..##.....#.#.##.#..##...##.#####..#...##...#..#.####.#.##.##.#....##.###.#.##..##..#.#.
..#.###.#.##...#..##.#..####.###..#####.##.####.#.##..####.###..##..#...#.##...#.###....####...####.
.###.....###.#....######.#####..#..#..#.#.#..#..#.###.#........##.###...#...##..#..#...#.....#.###.#
..###.##.#.#####.#..########..##..##.#..###.#.##.#....#.###........#....#...#.#...##.#.##..#..##.##.
###.#.#.#...#..##....#.##....##.#######.#.##.#.##....#....###.#.#.....#.##..###..##..#..##..#.#..##.
.#.##..#.##..##.##.##..#.###.#..##.###.#.###.##......##.#...##.##..##...##.#...##.#..#..#.##..#.##..
####..####.###..#..#####...###.#....###.#...##........#.#...#..#.#.###..####.#.#.######...#..##.#.#.
#...#..#.##..#.#.#.#.#...##.#.##..#...#.###.###.#....##.#..##.#.###..##....#.###.#.##..#..##....#...
#.###.#.##.###.#..#...####.#....#..#.#####.#...#.###.##.##.###.###..#...#.#.####..###..........##.#.
##.##.#.###.#.##.####...###.#.###..###...####..#####.###...#.##...###.##..#.####.#.##...#....##.#.##
#....#..##.##.##......##...##.##..#####...#.##.###.##...##..##..###..#..#..#...###.##.#..#..#.#...##
###.####.....#.#....####..#.##.........#....##.....#....##.#..##.##..####..###.####.#...##....##.##.
#.......###.#..####.##..#..##...#....###...##.......##.....###.######.#..#..##..#....#.###.#..##.###
#.###.##..##..##.##...#.........####..####..#..##...##.#..#..#######.###...#......#.##.####.#..##...
#.####...##.#...#.#.###...##...#....#.##.##.####.#.#....###....#...#........##.##..#.#.####..#.#.#..
.#..###.#..#.....##..#..#.###..###.#.##...#.#.....#...#....#.##.#..#.#...#..#.#..###..#.#...###.....
.####....####....#.#.....#..#.#.##........#..#.####.##.##...#.#.####.#..#.##..##..#...#.#.##...#.#.#
#####.#...####.#.####.#...#..#...#.#.##.#..#...##..#.#...##.###.##.#.###.###.#...#..#.###.##.##...#.
#.#....#.###.##..##.##..##.#...#.###....###....###..#.####.###..#.#.##...#..####....#.####...###.#..
.#...#.###.#.####..#.#####...##...#..##........#....#..#.#.##..##.##.#######.#.#.#.##.#.#.#.##..#...
#....#....#.#.##.##.##..###..###.##..#.##.....###.###......#.#....#..#.##......#.###.#..#.#.#.#..###
#####.#####.##...#.#..#..##.####.#......######..####..##.##.##.#.......#...####..#..###.#..##.#.#.#.
#.##...##..##......###...#.#.##...#.#...#..##.###.#..#.##...#.#.#.##.###.##.#####....#...#.....##..#
..##....##..#..##..##...#..#.##.####.##........###..##.##.#.#.##..#..###...#..#...##.#.##.########.#
#...#.#####.###.#....#....#######.###..#..#.#..##..#.###.#.####.##.#..###..#....###.###....###.#..##
.......###.#.#.#..#.#..###...#.##..#..#...#..#....#..#...#.#####.#...##.#.###.###.#..#.##.#..##.....
....#.##...#.##.#.###..#####..#.######.###...###..##.#.#.##.###.##.####..#..#.....#.......#.######.#
##..####......##...##.#..#..#..#..##.#.#..##..####.#.######.#...##..#..#.##.##..###..#..#.#..#..#...
.##.#..#..##.#.##..#..#.#.#...##.##...##.#.########..##..#...#####.....#.#..###.#.##.##.###..#..#.##
..##...#.#..#.#.##.###..#....#..###...#..##....##.#..######..###.#.#####..#.###.##.###..#####...####
#.#..###.##.#...#..###..#.##.##...####.####.#.....##....###..#..#...####.####.###...#..#.#.#.#.##..#
###..##...#.#..##..#...##..###.#.....#...##.###.#..###...###.####..###.#..#.#...##.....#............
.#####..##...##....######...#..###.#.#......#...######.#..#...###.#...#..####.#......##..#..#.#...#.
.#..####.#.#..###..#.#.##.####..#.#....#.####..##...#..#.#.#..###.........##.#.#####...###...#.#..#.
.#.#....#..####..##..#########.#..#.##..###..#..#...###....##.....####...#..#.##....#######.####.##.
##.#.####..#...#..#.##.#..#....##.####..####..###.#.#...#######.#.###..###.###..#.###.##...##.##..#.
.#####.....##.#....##...##...#.#..####.##..#....##.###.#####.##.#.#.#...#...#.#.#.......##..##.##.#.
.##..#.#.###.#.#.#....##.#...#....#...#...#..#######....##.#.#.#####.#.###..#..#...#......#..#.##..#
...##.....#..#.####.###...#####.#.#....##.#.#.#.#...####.####.#..##.#.##.##.###..##...##.....#...###
####.###..###.####..###.##..#.#####.#...##.#..#.#.##.####.#..####..#..##....####.#....#...#.####.#.#
##....##.#.#.##.###..#####.##..##..#..##..##..#.#..###.##.#####...#..#.##.#.####.####..#...##..#..##
#.#..###..##..#..#..####..#..#.#..#.##...###.#.#.#.#...####.#.#...####.##..#.#.#..#.##..##..##.#....
##.#.####....##..##..####.#######..##....######.##.#....#..#...#.#..#.##.#...#.#.#.#.#..###....#.#.#
.##.###..#.###..##...####.###.#.##.###.#...#..#......######.##.##.##.####.##.##....#.#......####.#.#
#..###.####.#...#.###.###.#..##.###..#.#.#####..#.##.##.#.##.##..###.####...####..#..###...#.##.####
#...............#.##.###...#..#..#.##.##.#.##.#.#...#.#....#..#.######..#..#..##....#.##..#..#..#.##
###.###...#...#..#....##.......#.#..#...##...#....#..######..#.....##.####..#....#...##...######..##
..##..#..##.#.##..###.#...............####...##..##......#...#.....#..#....#.#...#.....##..#####..##
#.....##.#.##.###......###.#.##..###....###..#...#..###.#..#..##...#..#.##...#.#...#..#.....##...#.#
..##....#..#.#.#.####..#.#.#....#.#.#.#.##.#..#.#..#..#.#.##.####......##..#...##..#.#.##..#.....#..
.#..##....###.###..##....#####.#....####....#.#.##..#...#.###.##..#.....##........###.###.####..#.#.
.###.##..#..#...#.#.#######.##.#.#.#.#.###.#.#.#.#......#####.###.#.#.#......#.#..#.#.##..#.##.#.#.#
⛄"""
