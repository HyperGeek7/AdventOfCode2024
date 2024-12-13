#!/usr/bin/env python3

from typing import Optional


type coord = tuple[int, int]


def part1(input_set: dict[coord, str]) -> int:
    result = 0

    unprocessed_coords = set(key for key in input_set.keys())

    while len(unprocessed_coords):
        seed_coord = unprocessed_coords.pop()
        unprocessed_coords, this_group = flood_fill(
            input_set, seed_coord, unprocessed_coords, set()
        )

        result += score_group(this_group)

    return result


def part2(input_set: dict[coord, str]) -> int:
    result = 0

    unprocessed_coords = set(key for key in input_set.keys())

    while len(unprocessed_coords):
        seed_coord = unprocessed_coords.pop()
        unprocessed_coords, this_group = flood_fill(
            input_set, seed_coord, unprocessed_coords, set()
        )

        result += count_sides(this_group) * len(this_group)

    return result


def score_group(group: set[coord]):
    perimiter = 0
    for this_coord in group:
        next_coords = [
            (this_coord[0] - 1, this_coord[1]),
            (this_coord[0] + 1, this_coord[1]),
            (this_coord[0], this_coord[1] - 1),
            (this_coord[0], this_coord[1] + 1),
        ]
        this_perimiter = 4

        for next_coord in next_coords:
            if next_coord in group:
                this_perimiter -= 1
        perimiter += this_perimiter

    return len(group) * perimiter


def count_sides(group: set[coord]) -> int:
    # There is a lot of repeated code in this function.
    # I'd apologize, but it was pretty much the only way
    # I could keep all the operations straight in my head.
    top_coords: list[coord] = []
    left_coords: list[coord] = []
    right_coords: list[coord] = []
    bottom_coords: list[coord] = []

    for this_coord in group:
        if (this_coord[0], this_coord[1] - 1) not in group:
            top_coords.append(this_coord)
        if (this_coord[0] - 1, this_coord[1]) not in group:
            left_coords.append(this_coord)
        if (this_coord[0], this_coord[1] + 1) not in group:
            bottom_coords.append(this_coord)
        if (this_coord[0] + 1, this_coord[1]) not in group:
            right_coords.append(this_coord)

    top_coords.sort(key=lambda x: (x[1], x[0]))
    bottom_coords.sort(key=lambda x: (x[1], x[0]))
    left_coords.sort()
    right_coords.sort()
    side_count = 0

    last_coord: Optional[coord] = None
    side_count += 1
    for this_coord in top_coords:
        if last_coord is None:
            last_coord = this_coord
            continue
        if this_coord[1] != last_coord[1] or this_coord[0] != last_coord[0] + 1:
            side_count += 1

        last_coord = this_coord

    last_coord = None
    side_count += 1
    for this_coord in bottom_coords:
        if last_coord is None:
            last_coord = this_coord
            continue
        if last_coord[1] != this_coord[1] or this_coord[0] != last_coord[0] + 1:
            side_count += 1

        last_coord = this_coord

    last_coord = None
    side_count += 1
    for this_coord in left_coords:
        if last_coord is None:
            last_coord = this_coord
            continue
        if last_coord[0] != this_coord[0] or this_coord[1] != last_coord[1] + 1:
            side_count += 1
        last_coord = this_coord

    last_coord = None
    side_count += 1
    for this_coord in right_coords:
        if last_coord is None:
            last_coord = this_coord
            continue
        if last_coord[0] != this_coord[0] or this_coord[1] != last_coord[1] + 1:
            side_count += 1
        last_coord = this_coord

    return side_count


def flood_fill(
    input_set: dict[coord, str],
    this_coord: coord,
    unprocessed_coords: set[coord],
    this_group: set[coord],
) -> tuple[set[coord], set[coord]]:
    this_group.add(this_coord)

    next_coords = [
        (this_coord[0] - 1, this_coord[1]),
        (this_coord[0] + 1, this_coord[1]),
        (this_coord[0], this_coord[1] - 1),
        (this_coord[0], this_coord[1] + 1),
    ]

    for next_coord in next_coords:
        if next_coord not in unprocessed_coords:
            continue
        if input_set[this_coord] != input_set[next_coord]:
            continue

        unprocessed_coords.remove(next_coord)

        unprocessed_coords, this_group = flood_fill(
            input_set, next_coord, unprocessed_coords, this_group
        )

    return unprocessed_coords, this_group


def parse_input(input_lines: list[str]) -> dict[coord, str]:
    result: dict[coord, str] = {}

    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            result[x, y] = char

    return result


def main():
    with open("day12.input.txt") as fin:
        input_set = parse_input(
            [line.strip() for line in fin.readlines() if len(line.strip()) > 0]
        )
        print(part1(input_set))
        print(part2(input_set))


if __name__ == "__main__":
    main()
