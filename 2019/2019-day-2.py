def input():
    with open('2019-day-2.txt') as f:
        line = f.readline()
        input = [int(n) for n in line.split(',')]
        return input


def intcode(int_codes):
    index = 0
    while index + 4 < len(int_codes) and (opcode := int_codes[index]) != 99:
        if opcode in [1, 2]:
            a_index = int_codes[index + 1]
            b_index = int_codes[index + 2]
            val_index = int_codes[index + 3]

            a = int_codes[a_index]
            b = int_codes[b_index]

            if opcode == 1:
                new_val = a + b  # add
            else:
                new_val = a * b  # multiply

            int_codes[val_index] = new_val  # store value
        elif opcode == 99:  # halt
            assert False, "Must've been never called"
            break  # assert will fail first, but leave it here in case I decide to unwalrus the solution
        else:
            raise ValueError(f"opcode={opcode}")
        index += 4
    return int_codes


def program_alarm(int_codes: list, noun=12, verb=2):
    int_codes[1] = noun
    int_codes[2] = verb
    return intcode(int_codes)


def test():
    assert intcode([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert intcode([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert intcode([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def determine_pair_of_inputs():
    expected = 19690720
    for noun in range(0, 100):
        for verb in range(0, 100):
            attempt = program_alarm(input(), noun, verb)
            if attempt[0] == expected:
                return (noun, verb)


if __name__ == "__main__":
    test()
    part_1 = program_alarm(input())
    print(f"https://adventofcode.com/2019/day/2, answer is {part_1[0]}")
    (noun, verb) = determine_pair_of_inputs()
    print(f"https://adventofcode.com/2019/day/2#part2, answer is {100 * noun + verb}")
    exit(0)
