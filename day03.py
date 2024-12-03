#!/usr/bin/env python3

import re


def part1(input_lines: list[str]) -> int:
    total = 0
    for line in input_lines:
        for match in re.finditer(r"mul\(([0-9]+),([0-9]+)\)", line):
            total += int(match.group(1)) * int(match.group(2))

    return total


def part2(input_lines: list[str]) -> int:
    total = 0
    mul_enabled = True
    for line in input_lines:
        for match in re.finditer(r"do\(\)|don't\(\)|mul\(([0-9]+),([0-9]+)\)", line):
            print(match.group(0))
            if match.group(0) == "do()":
                mul_enabled = True
            elif match.group(0) == "don't()":
                mul_enabled = False
            elif mul_enabled:
                total += int(match.group(1)) * int(match.group(2))

    return total


def main():
    with open("day03.input.txt") as fin:
        input_lines = [line for line in fin if len(line.strip()) > 0]
        print(part1(input_lines))
        print(part2(input_lines))


if __name__ == "__main__":
    main()
