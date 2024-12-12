#!/usr/bin/env python3

from collections import defaultdict, deque
from math import ceil, log10


def part2(input_set: list[int], steps: int) -> int:
    stone_counts: defaultdict[int, int] = defaultdict(int)
    stone_breaks: dict[int, list[int]] = {}

    for stone in input_set:
        stone_counts[stone] += 1

    for _ in range(steps):
        next_counts: defaultdict[int, int] = defaultdict(int)

        for stone_no, stone_count in stone_counts.items():
            if stone_no not in stone_breaks:
                stone_breaks[stone_no] = hard_process_stone(stone_no)

            for next_stone in stone_breaks[stone_no]:
                next_counts[next_stone] += stone_count

        stone_counts = next_counts

    return sum(stone_counts.values())


def hard_process_stone(this_stone: int) -> list[int]:
    if this_stone == 0:
        return [
            1,
        ]
    elif ((digit_count := int(log10(this_stone))) % 2) == 1:
        # This means an even number of digits.
        # I am...*very* sincerely hoping this is more efficient than
        # converting back and forth from strings.

        divisor = 10 ** ceil(digit_count / 2)
        return [this_stone // divisor, this_stone % divisor]
    else:
        return [
            this_stone * 2024,
        ]


def part1(input_set: deque[int]) -> int:
    for i in range(25):
        for _ in range(len(input_set)):
            this_stone = input_set[0]

            if this_stone == 0:
                input_set[0] = 1
            elif ((digit_count := int(log10(this_stone))) % 2) == 1:
                # This means an even number of digits.
                # I am...*very* sincerely hoping this is more efficient than
                # converting back and forth from strings.

                input_set.popleft()

                divisor = 10 ** ceil(digit_count / 2)
                input_set.appendleft(this_stone % divisor)
                input_set.appendleft(this_stone // divisor)

                # We increased the number of elements in the set, so we need to
                # do one extra rotate here to keep the loop working as intended.
                input_set.rotate(-1)
            else:
                input_set[0] *= 2024

            input_set.rotate(-1)

    return len(input_set)


def main():
    with open("day11.input.txt") as fin:
        input_line = fin.readline().strip()
        # This is going to involve a lot of "splitting" list elements.
        # That's slow, but I bet a deque can get around it.
        input_set = deque(int(stone) for stone in input_line.split())
        print(part1(input_set))
        input_set = [int(stone) for stone in input_line.split()]
        print(part2(input_set, 75))


if __name__ == "__main__":
    main()
