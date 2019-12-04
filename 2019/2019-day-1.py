import math


def calc_fuel(mass: int):
    return math.floor(mass / 3) - 2


def calc_fuel_for_fuel(fuel_mass: int):
    result = 0
    fuel_for_fuel = fuel_mass
    while (fuel_for_fuel := calc_fuel(fuel_for_fuel)) > -1:
        result += fuel_for_fuel
    return result


def rocket_equation():
    modules_fuel = 0
    all_fuel = 0
    with open('input/2019-day-1.txt') as f:
        for line in f:
            mass = int(line)
            fuel = calc_fuel(mass)
            fuel_for_fuel = calc_fuel_for_fuel(fuel)
            modules_fuel += fuel
            all_fuel += fuel + fuel_for_fuel
    print(f"https://adventofcode.com/2019/day/1, answer is {modules_fuel}")
    # 4853283 is the wrong answer
    print(f"https://adventofcode.com/2019/day/1#part2, answer is {all_fuel}")


if __name__ == "__main__":
    rocket_equation()
    # print(calc_fuel_for_fuel(654))
    exit(0)
