#!/usr/bin/env python3
import os


def input(location='input/2019-day-5.txt'):
    cwd = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cwd, location)) as f:
        line = f.readline()
        input = [int(n) for n in line.split(',')]
        return input


def param_mode(opcode):
    """
    if not in [1, 2, 3, 4, 99] interpret param modes as follows:

    ABCDE
     1002

    DE - two-digit opcode,      02 == opcode 2
     C - mode of 1st parameter,  0 == position mode
     B - mode of 2nd parameter,  1 == immediate mode
     A - mode of 3rd parameter,  0 == position mode,
                                      omitted due to being a leading zero
    """
    if opcode in [1, 2, 3, 4, 99]:
        return opcode, [0, 0, 0]
    param_str = f"{opcode:05d}"
    params = [int(c) for c in param_str]
    _opcode = params[3] + params[4]
    return _opcode, params[:3][::-1]  # reverse modes (CBA -> ABC) with slicing technique


def get_index(int_codes: list, index: int, mode: int):
    if mode == 0:  # positional
        return int_codes[index]
    elif mode == 1:  # immediate
        return index
    else:
        raise ValueError


def intcode(int_codes, input=1):
    index = 0
    output = []
    while index < len(int_codes):
        code_with_params = param_mode(int_codes[index])
        opcode = code_with_params[0]
        param_modes = code_with_params[1]
        if opcode in [1, 2]:
            a_index = get_index(int_codes, index + 1, param_modes[0])
            b_index = get_index(int_codes, index + 2, param_modes[1])
            val_index = get_index(int_codes, index + 3, param_modes[2])

            a = int_codes[a_index]
            b = int_codes[b_index]

            if opcode == 1:
                new_val = a + b  # add
            elif opcode == 2:
                new_val = a * b  # multiply
            else:
                raise ValueError

            int_codes[val_index] = new_val  # store value
            index += 4
        elif opcode in [3, 4]:
            new_index = int_codes[index + 1]
            if opcode == 3:
                int_codes[new_index] = input  # store value
            elif opcode == 4:
                _out = int_codes[new_index]
                output.append(_out)
                print(f"Output is {_out}")
            else:
                raise ValueError
            index += 2
        elif opcode == 99:  # halt
            break
        else:
            raise ValueError(f"opcode={opcode}")
    return int_codes, output


def asteroids(int_codes: list):
    return intcode(int_codes)


def test_asteroids():
    result1 = intcode([1002, 4, 3, 4, 33])
    assert result1[0] == [1002, 4, 3, 4, 99]
    assert result1[1] == []
    result2 = intcode([3, 0, 4, 0, 99])
    assert result2[0] == [1, 0, 4, 0, 99]
    assert result2[1] == [1]


if __name__ == "__main__":
    test_asteroids()
    part1 = asteroids(input())
    output1 = part1[1]
    print(f"https://adventofcode.com/2019/day/5, answer is {output1[-1]}")
    # (noun, verb) = determine_pair_of_inputs()
    # print(f"https://adventofcode.com/2019/day/5#part2, answer is {100 * noun + verb}")
    exit(0)
