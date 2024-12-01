#!/usr/bin/env python3


def prep_input(input_lines: list[str]) -> tuple[list[int], list[int]]:
    list1: list[int] = []
    list2: list[int] = []
    for line in input_lines:
        loc1, loc2 = line.split()
        list1.append(int(loc1))
        list2.append(int(loc2))
    return list1, list2


def part1(input_lines: list[str]):
    total = 0
    list1, list2 = prep_input(input_lines)

    sorted_list1 = sorted(list1)
    sorted_list2 = sorted(list2)

    while len(sorted_list1):
        pos1 = sorted_list1.pop()
        pos2 = sorted_list2.pop()

        total += abs(pos1 - pos2)

    return total


def part2(input_lines: list[str]):
    total = 0
    list1, list2 = prep_input(input_lines)

    for pos1 in list1:
        total += pos1 * list2.count(pos1)

    return total


def main():
    with open("day01.input.txt") as fin:
        input_lines = [line for line in fin if len(line.strip()) > 0]
        print(part1(input_lines))
        print(part2(input_lines))


if __name__ == "__main__":
    main()
