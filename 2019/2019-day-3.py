def input(location):
    with open(location) as f:
        wire_1 = [n for n in f.readline().split(',')]
        wire_2 = [n for n in f.readline().split(',')]
        return wire_1, wire_2


def calc_manhattan(point: list, original_point=None):
    if original_point is None:
        original_point = [0, 0]
    return int(abs(point[0] - original_point[0]) + abs(point[1] - original_point[1]))


def convert_points(directions: list):
    points = []
    point = [0, 0]
    points.append(point)
    for instruction in directions:
        point = point.copy()
        arrow = instruction[0]
        step = int(instruction[1:])
        if arrow == 'R':
            point[0] = point[0] + step
        elif arrow == 'L':
            point[0] = point[0] - step
        elif arrow == 'U':
            point[1] = point[1] + step
        elif arrow == 'D':
            point[1] = point[1] - step
        else:
            raise ValueError(f"invalid direction - {arrow}")
        points.append(point)
    return points


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


# Return true if line segments AB and CD intersect
def intersect(segment1, segment2):
    (A, B) = tuple(segment1)
    (C, D) = tuple(segment2)
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def find_intersection(line1, line2):
    (x1, y1, x2, y2) = tuple(line1[0] + line1[1])
    (x3, y3, x4, y4) = tuple(line2[0] + line2[1])
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    return [int(px), int(py)]


# def calc_steps_till_intersection(wire: list, index: int, int_point: list):
#     counter = 0
#     steps = 0
#     while counter <= index:
#         if counter == index:
#             steps += calc_manhattan(int_point, wire[counter])
#         else:
#             steps += calc_manhattan(wire[counter + 1], wire[counter])
#         counter += 1
#     return steps


def cross_wires(directions1, directions2):
    wire1 = convert_points(directions1)
    wire2 = convert_points(directions2)

    intersections = []
    steps = []
    i = 0
    step1 = 0
    while i + 1 < len(wire1):
        segment1 = (wire1[i], wire1[i + 1])
        j = 0  # reset counter
        step2 = 0
        while j + 1 < len(wire2):
            segment2 = (wire2[j], wire2[j + 1])

            if intersect(segment1, segment2):
                int_point = find_intersection(segment1, segment2)
                intersections.append(int_point)
                int_point_steps1 = step1 + calc_manhattan(segment1[0], int_point)
                int_point_steps2 = step2 + calc_manhattan(segment2[0], int_point)
                steps.append((int_point_steps1, int_point_steps2))

            step2 += calc_manhattan(segment2[0], segment2[1])
            j += 1

        step1 += calc_manhattan(segment1[0], segment1[1])
        i += 1
    return intersections, steps


def closest_manhattan(directions1: list, directions2: list):
    intersections = cross_wires(directions1, directions2)[0]
    intersections = sorted(intersections, key=lambda p: calc_manhattan(p))
    return calc_manhattan(intersections[0])


def fewest_steps(directions1: list, directions2: list):
    result = cross_wires(directions1, directions2)
    steps = result[1]
    steps = sorted(steps, key=lambda s: s[0] + s[1])
    return sum(steps[0])


def test_closest():
    assert closest_manhattan(*input('input/2019-day-3-test1.txt')) == 6
    assert closest_manhattan(*input('input/2019-day-3-test2.txt')) == 159
    assert closest_manhattan(*input('input/2019-day-3-test3.txt')) == 135


def test_fewest():
    assert fewest_steps(*input('input/2019-day-3-test1.txt')) == 30
    assert fewest_steps(*input('input/2019-day-3-test2.txt')) == 610
    assert fewest_steps(*input('input/2019-day-3-test3.txt')) == 410


if __name__ == "__main__":
    test_closest()
    print(f"https://adventofcode.com/2019/day/3, answer is {closest_manhattan(*input('input/2019-day-3.txt'))}")
    test_fewest()
    # 163524 is too low
    print(f"https://adventofcode.com/2019/day/3#part2, answer is {fewest_steps(*input('input/2019-day-3.txt'))}")
    exit(0)
