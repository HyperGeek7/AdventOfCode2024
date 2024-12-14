#!/usr/bin/env python3

from collections import defaultdict
from math import ceil, prod
from typing import NamedTuple
import re


type coord = tuple[int, int]


class Robot(NamedTuple):
    pos: coord
    vel: coord


def parse_input(input_lines: list[str]) -> list[Robot]:
    robots: list[Robot] = []

    for line in input_lines:
        # Yes, writing [0-9] was getting a little clunky,
        # even for me.
        match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
        if match is None:
            raise Exception("Malformed input line: " + line)

        pos_x, pos_y, vel_x, vel_y = match.groups()
        robots.append(Robot((int(pos_x), int(pos_y)), (int(vel_x), int(vel_y))))

    return robots


def print_field(robots: list[Robot], field_size: coord) -> None:
    robots_by_coord: defaultdict[coord, int] = defaultdict(int)

    for robot in robots:
        robots_by_coord[robot.pos] += 1

    for y in range(field_size[1]):
        for x in range(field_size[0]):
            if (x, y) in robots_by_coord:
                print(robots_by_coord[x, y], end="")
            else:
                print(".", end="")
        print("\n", end="")


def run_robots(
    robots: list[Robot], field_size: coord, seconds_to_run: int
) -> list[Robot]:
    new_robots: list[Robot] = []

    for robot in robots:
        new_x = (robot.pos[0] + (robot.vel[0] * seconds_to_run)) % field_size[0]
        new_y = (robot.pos[1] + (robot.vel[1] * seconds_to_run)) % field_size[1]

        new_robot = Robot((new_x, new_y), robot.vel)
        new_robots.append(new_robot)

    return new_robots


def part1(robots: list[Robot], field_size: coord):
    print_field(robots, field_size)
    print("\n")
    robots = run_robots(robots, field_size, 100)
    print_field(robots, field_size)

    # Quadrantize me, cap'n!
    # 01
    # 23

    quadrant_counts = [0, 0, 0, 0]
    lost_axes = (field_size[0] // 2, field_size[1] // 2)
    horizontal_cutoff = ceil(field_size[0] / 2)
    vertical_cutoff = ceil(field_size[1] / 2)

    for robot in robots:
        if robot.pos[0] == lost_axes[0] or robot.pos[1] == lost_axes[1]:
            continue

        quadrant = 0
        if robot.pos[0] >= horizontal_cutoff:
            quadrant += 1
        if robot.pos[1] >= vertical_cutoff:
            quadrant += 2

        quadrant_counts[quadrant] += 1

    print(quadrant_counts)
    return prod(quadrant_counts)


def part2(robots: list[Robot], field_size: coord):
    # There's almost certainly a smarter way to do this.
    # But smart isn't how we do things around here,
    # and grep is fast. This gets the job done.

    seconds_elapsed = 0

    with open("images.txt", "w") as fout:
        robots = run_robots(robots, field_size, 0)
        for _ in range(10000):
            robot_coords: set[coord] = set(robot.pos for robot in robots)
            field_lines: list[str] = [
                f"Seconds elapsed: {seconds_elapsed}",
                "",
            ]
            for y in range(field_size[1]):
                field_lines.append(
                    "".join(
                        "#" if (x, y) in robot_coords else "."
                        for x in range(field_size[0])
                    )
                )

            fout.write("\n".join(field_lines))
            fout.write("\n\n")
            robots = run_robots(robots, field_size, 1)
            seconds_elapsed += 1


def main():
    with open("day14.input.txt") as fin:
        input_lines = [line.strip() for line in fin if len(line.strip()) > 0]
        robots = parse_input(input_lines)
        # field_size = (11, 7)  # For demo input
        field_size = (101, 103)  # For real input
        print(part1(robots, field_size))
        part2(robots, field_size)


if __name__ == "__main__":
    main()
