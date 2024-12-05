#!/usr/bin/env python3

from collections import defaultdict
from functools import cmp_to_key


def parse_input(
    input_lines: list[str],
) -> tuple[defaultdict[int, list[int]], list[list[int]]]:
    rules: defaultdict[int, list[int]] = defaultdict(lambda: list())
    pages: list[list[int]] = []

    while len(input_lines):
        this_line = input_lines.pop(0)
        if "|" not in this_line:
            break

        this_rule = this_line.split("|")
        rules[int(this_rule[0])].append(int(this_rule[1]))

    while len(input_lines):
        this_line = input_lines.pop(0)
        if "," not in this_line:
            break

        pages.append([int(page) for page in this_line.split(",")])

    return rules, pages


def page_set_valid(rules: defaultdict[int, list[int]], page_set: list[int]) -> bool:
    for page in page_set:
        if page not in rules:
            continue
        page_pos = page_set.index(page)

        for rule in rules[page]:
            try:
                rule_pos = page_set.index(rule)
                if rule_pos < page_pos:
                    return False
            except ValueError:
                pass

    return True


def part1(rules: defaultdict[int, list[int]], pages: list[list[int]]) -> int:
    total = 0

    for page_set in pages:
        if page_set_valid(rules, page_set):
            middle_page = page_set[len(page_set) // 2]
            total += middle_page

    return total


def part2(rules: defaultdict[int, list[int]], pages: list[list[int]]) -> int:
    total = 0

    def comparison_function(page_a: int, page_b: int) -> int:
        if page_b in rules[page_a]:
            return -1
        elif page_a in rules[page_b]:
            return 1
        else:
            return 0

    key_comparison_function = cmp_to_key(comparison_function)

    for page_set in pages:
        if not page_set_valid(rules, page_set):
            # Work smarter, not harder!
            # ...By which I mean, just make the standard library
            # do the hard part. It's *probably* not cheating!
            new_page_set: list[int] = sorted(page_set, key=key_comparison_function)
            middle_page = new_page_set[len(new_page_set) // 2]
            total += middle_page

    return total


def main():
    with open("day05.input.txt") as fin:
        input_lines = [line for line in fin]
        rules, pages = parse_input(input_lines)
        print(part1(rules, pages))
        print(part2(rules, pages))


if __name__ == "__main__":
    main()
