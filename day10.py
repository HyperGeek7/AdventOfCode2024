#!/usr/bin/env python3

type coord = tuple[int, int]


def parse_input(input_lines: list[str]) -> dict[coord, int]:
    result: dict[coord, int] = {}
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            result[x, y] = int(char)

    return result


def trace_path(
    input_set: dict[coord, int], location: coord, visited_locations: set[coord]
) -> list[coord]:
    my_results = []
    visited_locations.add(location)

    my_height = input_set[location]
    possible_locations = [
        (location[0] - 1, location[1]),
        (location[0] + 1, location[1]),
        (location[0], location[1] - 1),
        (location[0], location[1] + 1),
    ]

    for this_location in possible_locations:
        if this_location not in input_set:
            continue
        elif input_set[this_location] != my_height + 1:
            continue
        elif this_location in visited_locations:
            continue
        elif input_set[this_location] == 9:
            my_results.append(this_location)
        else:
            my_results.extend(trace_path(input_set, this_location, visited_locations))

    return my_results


def part1(input_set: dict[coord, int]) -> int:
    result = 0

    trailheads = [k for k, v in input_set.items() if v == 0]

    for trailhead in trailheads:
        final_locations: set[coord] = set(trace_path(input_set, trailhead, set()))
        result += len(final_locations)

    return result


def trace_path_part2(input_set: dict[coord, int], location: coord) -> list[coord]:
    my_results = []

    my_height = input_set[location]
    possible_locations = [
        (location[0] - 1, location[1]),
        (location[0] + 1, location[1]),
        (location[0], location[1] - 1),
        (location[0], location[1] + 1),
    ]

    for this_location in possible_locations:
        if this_location not in input_set:
            continue
        elif input_set[this_location] != my_height + 1:
            continue
        elif input_set[this_location] == 9:
            my_results.append(this_location)
        else:
            my_results.extend(trace_path_part2(input_set, this_location))

    return my_results


def part2(input_set: dict[coord, int]) -> int:
    result = 0

    trailheads = [k for k, v in input_set.items() if v == 0]

    for trailhead in trailheads:
        this_trailhead_rating = trace_path_part2(input_set, trailhead)
        result += len(this_trailhead_rating)

    return result


def main():
    with open("day10.input.txt") as fin:
        input_lines = [line.strip() for line in fin if len(line) > 0]
        input_set = parse_input(input_lines)
        print(part1(input_set))
        print(part2(input_set))


if __name__ == "__main__":
    main()
