#!/usr/bin/env python3

from typing import Optional, TypedDict


class FileBlock(TypedDict):
    file_no: Optional[int]
    length: int


def parse_input(input_line: str) -> list[FileBlock]:
    result: list[FileBlock] = []
    file_id = 0
    placing_file = True

    for length_char in input_line:
        file_length = int(length_char)
        if not placing_file:

            placing_file = True
            if file_length > 0:
                result.append(FileBlock(file_no=None, length=file_length))
            continue

        placing_file = False
        result.append(FileBlock(file_no=file_id, length=file_length))
        file_id += 1

    return result


def calc_checksum(input_state: list[FileBlock]) -> int:
    result = 0
    pos = 0

    for block in input_state:
        for _ in range(block["length"]):
            if block["file_no"] is not None:
                result += pos * block["file_no"]
            pos += 1

    return result


def draw_blocks(input_state: list[FileBlock]) -> str:
    result: list[str] = []
    for block in input_state:
        block_char = str(block["file_no"]) if block["file_no"] is not None else "."
        result.append(block_char * block["length"])

    return "".join(result)


def part1(input_state: list[FileBlock]) -> int:
    while True:
        first_open = None
        last_block = None
        data_pos = -1
        open_pos = -1

        for i, block in reversed(
            [enumed_block for enumed_block in enumerate(input_state)]
        ):
            if block["file_no"] is not None:
                data_pos = i
                last_block = block
                break

        for i, block in enumerate(input_state):
            if block["file_no"] is None:
                open_pos = i
                first_open = block
                break

        if first_open is None or last_block is None:
            print("Pretty sure this can't happen.")
            break

        if open_pos > data_pos:
            break

        del input_state[data_pos]
        del input_state[open_pos]

        if last_block["length"] <= first_open["length"]:
            empty_length = first_open["length"] - last_block["length"]
            if empty_length > 0:
                new_empty = FileBlock(file_no=None, length=empty_length)
                input_state.insert(open_pos, new_empty)

            input_state.insert(open_pos, last_block)
        else:
            remaining_length = last_block["length"] - first_open["length"]
            new_data = FileBlock(
                file_no=last_block["file_no"], length=first_open["length"]
            )
            last_block["length"] = remaining_length
            input_state.insert(open_pos, new_data)
            input_state.insert(data_pos, last_block)

    return calc_checksum(input_state)


def part2(input_state: list[FileBlock]) -> int:
    for block in reversed(
        [block for block in input_state if block["file_no"] is not None]
    ):
        data_pos = None
        last_block = block
        first_open = None
        open_pos = -1

        for j, block in enumerate(input_state):
            if block["file_no"] == last_block["file_no"]:
                data_pos = j
                break

        if data_pos is None:
            print("Bad bad bad bad")
            break

        for j, block in enumerate(input_state):
            if block["file_no"] is None and block["length"] >= last_block["length"]:
                open_pos = j
                first_open = block
                break

        if first_open is None:
            continue

        if open_pos > data_pos:
            continue

        input_state[data_pos] = FileBlock(file_no=None, length=last_block["length"])
        del input_state[open_pos]

        empty_length = first_open["length"] - last_block["length"]
        if empty_length > 0:
            new_empty = FileBlock(file_no=None, length=empty_length)
            input_state.insert(open_pos, new_empty)

        input_state.insert(open_pos, last_block)

    return calc_checksum(input_state)


def main():
    with open("day09.input.txt") as fin:
        input_line = fin.readline().strip()
        input_state = parse_input(input_line)
        print(part1(input_state))
        input_state = parse_input(input_line)
        print(part2(input_state))


if __name__ == "__main__":
    main()
