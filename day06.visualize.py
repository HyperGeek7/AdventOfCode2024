#!/usr/bin/env python3

from collections import defaultdict, deque
from time import sleep
from typing import Optional

from rich.console import Console
from rich.live import Live

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

facing_chars = {
    "U": "^",
    "R": ">",
    "D": "v",
    "L": "<",
}


def render_path(
    input_lines: list[str],
    guard_state: coord_facing,
    location_states: defaultdict[coord, set[str]],
    live: Live,
):
    # Listen. This whole function is hilariously inefficient.
    # I'm not fixing it. It works just enough to do what I want.
    console = live.console
    width, height = console.size

    y, x = guard_state[0]

    start_y = 0
    start_x = 0

    if len(input_lines) > height:
        if y > height // 2:
            start_y = y - (height // 2)
        else:
            start_y = 0

    if len(input_lines[0]) > width:
        if x > width // 2:
            start_x = len(input_lines[0]) - width
        else:
            start_x = x // 2

    out_lines: list[str] = []
    for i in range(start_y, start_y + height):
        this_line = []
        for j in range(start_x, start_x + width):
            try:
                char = input_lines[i][j]
            except IndexError:
                break
            if (i, j) == guard_state[0]:
                char = f"[bold green1]{facing_chars[guard_state[1]]}[/]"
            elif (i, j) in location_states:
                if "U" in location_states[i, j] or "D" in location_states[i, j]:
                    if (
                        "L" not in location_states[i, j]
                        and "R" not in location_states[i, j]
                    ):
                        char = "[bold magenta1]│[/]"
                    else:
                        char = "[bold magenta1]┼[/]"
                else:
                    char = "[bold magenta1]─[/]"

            this_line.append(char)

        out_lines.append("".join(this_line))

    live.update("\n".join(out_lines), refresh=True)


def part1(input_lines: list[str], live: Optional[Live] = None) -> set[coord]:
    visited_locations: set[coord] = set()
    location_states: defaultdict[coord, set[str]] = defaultdict(set)

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
        location_states[location].add(guard_facing)
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

        if live is not None:
            render_path(input_lines, (location, guard_facing), location_states, live)
            sleep(0.01)

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


def part2(
    input_lines: list[str], possible_locations: Optional[set[coord]] = None
) -> int:
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
        possible_locations = set(
            (i, j) for i in range(len(input_lines)) for j in range(len(input_lines[0]))
        )

    for i, j in possible_locations:
        char = input_lines[i][j]
        if char in ("#", "^"):
            continue

        this_input_set = input_lines.copy()
        this_input_set[i] = this_input_set[i][0:j] + "#" + this_input_set[i][j + 1 :]

        if trace_path(location, guard_facing, this_input_set, facing_directions.copy()):
            obstacle_locations.add((i, j))

    return len(obstacle_locations)


def main():
    console = Console(highlight=False)
    with Live(console=console, screen=True) as live:
        with open("day06.input.txt") as fin:
            input_lines = [line.strip() for line in fin if len(line) > 0]
            orig_path = part1(input_lines, live)
            print(len(orig_path))
            input()
            # print(part2(input_lines, orig_path))


if __name__ == "__main__":
    main()
