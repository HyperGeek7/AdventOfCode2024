#!/usr/bin/env python3

from math import ceil, floor
import re
from typing import NamedTuple, Optional


class LineDefinition(NamedTuple):
    # ax + by + c = 0
    a: int
    b: int
    c: int


def intersection(
    line1: LineDefinition, line2: LineDefinition
) -> Optional[tuple[int, int]]:
    # My math is *extremely* rusty, but
    # https://www.cuemath.com/geometry/intersection-of-two-lines/
    # assures me that this is how you get the intersection of
    # two lines.

    x = ((line1.b * line2.c) - (line2.b * line1.c)) / (
        (line1.a * line2.b) - (line2.a * line1.b)
    )
    y = ((line1.c * line2.a) - (line2.c * line1.a)) / (
        (line1.a * line2.b) - (line2.a * line1.b)
    )

    if floor(x) == ceil(x) and floor(y) == ceil(y):
        return int(x), int(y)

    return None


def part1(input_pairs: list[tuple[LineDefinition, LineDefinition]]) -> int:
    # This is actually parts 1 and 2.
    # The change to part 2 is handled during input parsing,
    # with the heavy lifting here being indentical.
    result = 0

    for input_pair in input_pairs:
        intersection_point = intersection(*input_pair)

        if intersection_point is not None:
            this_score = (intersection_point[0] * 3) + intersection_point[1]
            result += this_score

    return result


def parse_input(
    input_lines: list[str], part2: bool
) -> list[tuple[LineDefinition, LineDefinition]]:
    result = []

    while len(input_lines):
        this_line = input_lines.pop(0)
        match = re.match(r"Button A: X\+([0-9]+), Y\+([0-9]+)", this_line)
        if match is None:
            raise Exception("Input was malformed: " + this_line)

        a1 = int(match.group(1))
        a2 = int(match.group(2))

        this_line = input_lines.pop(0)
        match = re.match(r"Button B: X\+([0-9]+), Y\+([0-9]+)", this_line)
        if match is None:
            raise Exception("Input was malformed: " + this_line)

        b1 = int(match.group(1))
        b2 = int(match.group(2))

        this_line = input_lines.pop(0)
        match = re.match(r"Prize: X=([0-9]+), Y=([0-9]+)", this_line)
        if match is None:
            raise Exception("Input was malformed: " + this_line)

        if part2:
            c1 = int(match.group(1)) + 10000000000000
            c2 = int(match.group(2)) + 10000000000000
        else:
            c1 = int(match.group(1))
            c2 = int(match.group(2))

        result.append((LineDefinition(a1, b1, -c1), LineDefinition(a2, b2, -c2)))

    return result


def main():
    with open("day13.input.txt") as fin:
        input_lines = [
            line.strip() for line in fin.readlines() if len(line.strip()) > 0
        ]
        input_set = parse_input(input_lines.copy(), False)
        print(part1(input_set))
        input_set = parse_input(input_lines.copy(), True)
        print(part1(input_set))


if __name__ == "__main__":
    main()
