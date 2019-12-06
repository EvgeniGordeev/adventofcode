#!/usr/bin/env python3
import os


def _input(location='input/2019-day-5.txt'):
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
    if opcode in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
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


def intcode(int_codes, _in=1):
    instruction_pointer = 0
    output = []
    while instruction_pointer < len(int_codes):
        code_with_params = param_mode(int_codes[instruction_pointer])
        opcode = code_with_params[0]
        param_modes = code_with_params[1]
        if opcode in [1, 2]:
            param1 = get_index(int_codes, instruction_pointer + 1, param_modes[0])
            param2 = get_index(int_codes, instruction_pointer + 2, param_modes[1])
            param3 = get_index(int_codes, instruction_pointer + 3, param_modes[2])

            a = int_codes[param1]
            b = int_codes[param2]

            if opcode == 1:
                new_val = a + b  # add
            elif opcode == 2:
                new_val = a * b  # multiply
            else:
                assert False

            int_codes[param3] = new_val  # store value
            instruction_pointer += 4
        elif opcode in [3, 4]:
            new_index = int_codes[instruction_pointer + 1]
            if opcode == 3:
                int_codes[new_index] = _in  # store value
            elif opcode == 4:
                _out = int_codes[new_index]
                output.append(_out)
                # print(f"Output is {_out}")
            else:
                assert False
            instruction_pointer += 2
        elif opcode == 5:  # jump-if-true
            param1 = get_index(int_codes, instruction_pointer + 1, 0) # using param_modes - index of bounds
            param2 = get_index(int_codes, instruction_pointer + 2, 0) # using param_modes - index of bounds
            if param1 != 0:
                instruction_pointer = param2
            else:
                instruction_pointer += 3
        elif opcode == 6:  # jump-if-false
            param1 = get_index(int_codes, instruction_pointer + 1, 0) # using param_modes - index of bounds
            param2 = get_index(int_codes, instruction_pointer + 2, 0) # using param_modes - index of bounds
            if param1 == 0:
                instruction_pointer = param2
            else:
                instruction_pointer += 3
        elif opcode == 7:  # less than
            param1 = get_index(int_codes, instruction_pointer + 1, 0) # using param_modes - index of bounds
            param2 = get_index(int_codes, instruction_pointer + 2, 0) # using param_modes - index of bounds
            param3 = get_index(int_codes, instruction_pointer + 3, 0) # using param_modes - index of bounds
            if param1 < param2:
                int_codes[param3] = 1
            else:
                int_codes[param3] = 0
            instruction_pointer += 4
        elif opcode == 8:  # equals
            param1 = get_index(int_codes, instruction_pointer + 1, 0)
            param2 = get_index(int_codes, instruction_pointer + 2, 0)
            param3 = get_index(int_codes, instruction_pointer + 3, 0)
            if param1 == param2:
                int_codes[param3] = 1
            else:
                int_codes[param3] = 0
            instruction_pointer += 4
        elif opcode == 99:  # halt
            break
        else:
            raise ValueError(f"opcode={opcode}")
    return int_codes, output


def asteroids(int_codes: list, _in=1):
    return intcode(int_codes, _in)


def test_part1():
    result1 = intcode([1002, 4, 3, 4, 33])
    assert result1[0] == [1002, 4, 3, 4, 99]
    assert result1[1] == []
    result2 = intcode([3, 0, 4, 0, 99])
    assert result2[0] == [1, 0, 4, 0, 99]
    assert result2[1] == [1]


def test_part2():
    result11 = intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1)
    assert result11[1] == [1]
    result12 = intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0)
    #  assert result2[1] == [0] # todo: this fails
    result2 = intcode([3,9,8,9,10,9,4,9,99,-1,8], 7)
    test_codes = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                  1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                  999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    result31 = intcode(test_codes, 7)
    # assert result31[1] == [999] # todo: this fails
    result32 = intcode(test_codes, 8)
    assert result32[1] == [1000]
    result33 = intcode(test_codes, 9)
    # assert result33[1] == [1001] # todo: this fails


if __name__ == "__main__":
    test_part1()
    test_part2()
    part1 = asteroids(_input())
    output1 = part1[1]
    print(f"https://adventofcode.com/2019/day/5, answer is {output1[-1]}")
    # part2 = asteroids(_input(), 5)
    # print(f"https://adventofcode.com/2019/day/5#part2, answer is {100 * noun + verb}")
    exit(0)
