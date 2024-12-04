#!/usr/bin/env python3

from collections import Counter


def generate_skew_line(input_lines: list[str], i: int, j: int) -> str:
    skew_line = ""
    while True:
        try:
            skew_line += input_lines[i][j]
            i += 1
            j += 1
        except IndexError:
            break

    return skew_line


def part1(input_lines: list[str]) -> int:
    if len(input_lines) == 0:
        raise Exception("Listen here, you.")

    total = 0
    for line in input_lines:
        # Easy search first: XMAS written out horizontally
        total += line.count("XMAS")
        # Only marginally less easy: SAMX written out horizontally
        total += line.count("SAMX")

    # Vertical is not difficult: rotate the input 90 degrees,
    # then do the thing again.
    rotated_input_lines: list[str] = []
    for i in range(len(input_lines[0])):
        rotated_input_lines.append("".join(line[i] for line in input_lines))

    for line in rotated_input_lines:
        # Easy search first: XMAS written out horizontally
        total += line.count("XMAS")
        # Only marginally less easy: SAMX written out horizontally
        total += line.count("SAMX")

    # Diagonals are trickier, but the same principle applies:
    # "skew" the input, then do the thing.
    skewed_lines: list[str] = []
    for i in range(len(input_lines)):
        skewed_lines.append(generate_skew_line(input_lines, i, 0))
    # We already did 0,0, so start j at 1
    for j in range(1, len(input_lines[0])):
        skewed_lines.append(generate_skew_line(input_lines, 0, j))

    for line in skewed_lines:
        total += line.count("XMAS")
        total += line.count("SAMX")

    # Do the same, but with the lines in reverse order to get the
    # other diagonal.
    skewed_lines = []
    reversed_input_lines = [line for line in reversed(input_lines)]
    for i in range(len(input_lines)):
        skewed_lines.append(generate_skew_line(reversed_input_lines, i, 0))
    for j in range(1, len(input_lines[0])):
        skewed_lines.append(generate_skew_line(reversed_input_lines, 0, j))

    for line in skewed_lines:
        total += line.count("XMAS")
        total += line.count("SAMX")

    return total


def part2(input_lines: list[str]) -> int:
    total = 0
    for i, line in enumerate(input_lines):
        if i == 0 or i == len(input_lines) - 1:
            continue
        last_index = 0
        while True:
            j = line.find("A", last_index + 1)
            if j == -1:
                break

            try:
                corner_chars = [
                    input_lines[i - 1][j - 1],  # NW
                    input_lines[i - 1][j + 1],  # NE
                    input_lines[i + 1][j - 1],  # SW
                    input_lines[i + 1][j + 1],  # SE
                ]
                if corner_chars[0] != corner_chars[3]:
                    count = Counter(corner_chars)
                    if count["M"] == 2 and count["S"] == 2:
                        total += 1
            except IndexError:
                pass

            last_index = j

    return total


def main():
    with open("day04.input.txt") as fin:
        input_lines = [line for line in fin if len(line.strip()) > 0]
        print(part1(input_lines))
        print(part2(input_lines))


if __name__ == "__main__":
    main()
