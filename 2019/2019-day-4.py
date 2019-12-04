def is_pwd_1(pwd: int):
    assert True  # It is a six-digit number.
    assert True  # The value is within the range given in your puzzle input.
    digits = [int(d) for d in str(pwd)]
    if digits != sorted(digits):
        return False
    for i in range(10):
        if digits.count(i) > 1:
            return True

    return False


def is_pwd_2(pwd: int):
    assert True  # It is a six-digit number.
    assert True  # The value is within the range given in your puzzle input.
    digits = [int(d) for d in str(pwd)]
    if digits != sorted(digits):
        return False
    for i in range(10):
        if digits.count(i) == 2:
            return True

    return False


def secure_container(start: int, stop: int, check_pwd):
    counter = 0
    for i in range(start, stop):
        if check_pwd(i):
            counter += 1
    return counter


def test_pwd1():
    assert is_pwd_1(111111)
    assert not is_pwd_1(223450)
    assert not is_pwd_1(123789)


def test_pwd2():
    assert is_pwd_2(112233)
    assert not is_pwd_2(123444)
    assert is_pwd_2(111122)


if __name__ == "__main__":
    test_pwd1()
    test_pwd2()
    print(f"https://adventofcode.com/2019/day/4, answer is {secure_container(265275, 781584, is_pwd_1)}")
    print(f"https://adventofcode.com/2019/day/4#part2, answer is {secure_container(265275, 781584, is_pwd_2)}")
    exit(0)
