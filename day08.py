#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations

type coord = tuple[int, int]


def parse_input(input_lines: list[str]) -> tuple[defaultdict[str, list[coord]], coord]:
    result: defaultdict[str, list[coord]] = defaultdict(list)

    y_bound = len(input_lines)
    x_bound = len(input_lines[0])
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            result[char].append((x, y))

    return result, (x_bound, y_bound)


def check_bounds(point: coord, map_bounds: coord) -> bool:
    if point[0] < 0 or point[1] < 0:
        return False
    if point[0] >= map_bounds[0] or point[1] >= map_bounds[1]:
        return False
    return True


def make_antinodes(a: coord, b: coord) -> tuple[coord, coord]:
    distance = (b[0] - a[0], b[1] - a[1])

    anti_a = (a[0] - distance[0], a[1] - distance[1])
    anti_b = (b[0] + distance[0], b[1] + distance[1])

    return anti_a, anti_b


def make_all_antinodes(a: coord, b: coord, map_bounds: coord) -> list[coord]:
    result = [
        a,
        b,
    ]

    distance = (b[0] - a[0], b[1] - a[1])

    last_position = a
    while True:
        new_antinode = (last_position[0] - distance[0], last_position[1] - distance[1])
        if not check_bounds(new_antinode, map_bounds):
            break
        result.append(new_antinode)
        last_position = new_antinode

    last_position = b
    while True:
        new_antinode = (last_position[0] + distance[0], last_position[1] + distance[1])
        if not check_bounds(new_antinode, map_bounds):
            break
        result.append(new_antinode)
        last_position = new_antinode

    return result


def part1(antenna_coords: defaultdict[str, list[coord]], map_bounds: coord) -> int:
    antinodes: set[coord] = set()

    for coords in antenna_coords.values():
        coord_pairs = combinations(coords, 2)
        for pair in coord_pairs:
            these_antinodes = make_antinodes(*pair)
            for antinode in these_antinodes:
                if check_bounds(antinode, map_bounds):
                    antinodes.add(antinode)

    return len(antinodes)


def part2(antenna_coords: defaultdict[str, list[coord]], map_bounds: coord) -> int:
    antinodes: set[coord] = set()

    for coords in antenna_coords.values():
        coord_pairs = combinations(coords, 2)
        for pair in coord_pairs:
            these_antinodes = make_all_antinodes(*pair, map_bounds)
            for antinode in these_antinodes:
                antinodes.add(antinode)

    return len(antinodes)


def main():
    with open("day08.input.txt") as fin:
        input_lines = [line.strip() for line in fin if len(line) > 0]
        antenna_coords, map_bounds = parse_input(input_lines)
        print(part1(antenna_coords, map_bounds))
        print(part2(antenna_coords, map_bounds))


if __name__ == "__main__":
    main()
