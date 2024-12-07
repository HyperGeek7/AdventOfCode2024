#!/usr/bin/env python3


def crunch_operands(result: int, operands: list[int], permit_concat=False) -> bool:
    if len(operands) == 1:
        return result == operands[0]

    # Our operations can never decrease the value,
    # so if we ever overshoot the result, we can stop
    # processing this path.
    if operands[0] > result:
        return False

    first_operand = operands.pop(0)
    second_operand = operands.pop(0)

    add_operands = operands.copy()
    add_operands.insert(0, first_operand + second_operand)

    mult_operands = operands.copy()
    mult_operands.insert(0, first_operand * second_operand)

    if permit_concat:
        concat_operands = operands.copy()
        concat_operands.insert(0, int(f"{first_operand}{second_operand}"))

    return (
        crunch_operands(result, add_operands, permit_concat)
        or crunch_operands(result, mult_operands, permit_concat)
        or (permit_concat and crunch_operands(result, concat_operands, permit_concat))
    )


def part1(input_lines: list[str]) -> int:
    total = 0

    for line in input_lines:
        result, operands = parse_input(line)

        if crunch_operands(result, operands):
            total += result

    return total


def part2(input_lines: list[str]) -> int:
    total = 0

    for line in input_lines:
        result, operands = parse_input(line)

        if crunch_operands(result, operands, True):
            total += result

    return total


def parse_input(line: str) -> tuple[int, list[int]]:
    result_str, operand_segment = line.split(":", 1)
    result = int(result_str)
    operands = [int(operand) for operand in operand_segment.split()]

    return result, operands


def main():
    with open("day07.input.txt") as fin:
        input_lines = [line.strip() for line in fin if len(line) > 0]
        print(part1(input_lines))
        print(part2(input_lines))


if __name__ == "__main__":
    main()
