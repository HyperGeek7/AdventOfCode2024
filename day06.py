#!/usr/bin/env python3

from collections import deque
from typing import Optional

coord = tuple[int, int]
coord_facing = tuple[coord, str]

facing_directions = deque(
    (
        "U",
        "R",
        "D",
        "L",
    )
)


def part1(input_lines: list[str]) -> set[coord]:
    visited_locations: set[coord] = set()

    guard_facing = facing_directions[0]
    location: coord = (-1, -1)

    for i, line in enumerate(input_lines):
        j = line.find("^")
        if j > -1:
            location = (i, j)
            break

    if location == (-1, -1):
        raise Exception("Where am I?")

    while True:
        visited_locations.add(location)
        i, j = location
        if guard_facing == "U":
            next_location = (i - 1, j)
        elif guard_facing == "R":
            next_location = (i, j + 1)
        elif guard_facing == "D":
            next_location = (i + 1, j)
        elif guard_facing == "L":
            next_location = (i, j - 1)
        else:
            raise Exception("The guard is having a nap.")

        try:
            if input_lines[next_location[0]][next_location[1]] == "#":
                facing_directions.rotate(-1)
                guard_facing = facing_directions[0]
            else:
                location = next_location
        except IndexError:
            break

    # return len(visited_locations)
    return visited_locations


def get_next_location(location: coord, facing: str) -> coord:
    i, j = location
    if facing == "U":
        next_location = (i - 1, j)
    elif facing == "R":
        next_location = (i, j + 1)
    elif facing == "D":
        next_location = (i + 1, j)
    elif facing == "L":
        next_location = (i, j - 1)
    else:
        raise Exception("The guard is having a nap.")

    return next_location


def trace_path(
    location: coord, facing: str, input_lines: list[str], my_facings: deque[str]
) -> bool:
    """Returns True if this path will loop, False otherwise"""
    my_location_facings = set()

    while True:
        this_location_facing = (location, facing)

        if this_location_facing in my_location_facings:
            # We've been here facing this direction before,
            # so we're in a loop.
            return True

        my_location_facings.add((location, facing))

        next_location = get_next_location(location, facing)

        i, j = next_location
        if i < 0 or j < 0:
            return False

        try:
            if input_lines[i][j] == "#":
                my_facings.rotate(-1)
                facing = my_facings[0]
            else:
                location = next_location
        except IndexError:
            return False


def part2(input_lines: list[str], possible_locations: Optional[set[coord]] = None) -> int:
    obstacle_locations: set[coord] = set()

    # Reset the queue, just in case part 1 messed it up.
    while facing_directions[0] != "U":
        facing_directions.rotate(-1)

    guard_facing = facing_directions[0]
    location: coord = (-1, -1)

    for i, line in enumerate(input_lines):
        j = line.find("^")
        if j > -1:
            location = (i, j)
            break

    if location == (-1, -1):
        raise Exception("Where am I?")

    if possible_locations is None:
        possible_locations = set((i, j) for i in range(len(input_lines)) for j in range(len(input_lines[0])))

    for i, j in possible_locations:
        char = input_lines[i][j]
        if char in ("#", "^"):
            continue

        this_input_set = input_lines.copy()
        this_input_set[i] = (
            this_input_set[i][0:j] + "#" + this_input_set[i][j + 1 :]
        )

        if trace_path(
            location, guard_facing, this_input_set, facing_directions.copy()
        ):
            obstacle_locations.add((i, j))

    return len(obstacle_locations)


def main():
    with open("day06.input.txt") as fin:
        input_lines = [line.strip() for line in fin if len(line) > 0]
        orig_path = part1(input_lines)
        print(len(orig_path))
        print(part2(input_lines, orig_path))


if __name__ == "__main__":
    main()
