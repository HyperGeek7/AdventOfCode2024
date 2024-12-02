#!/usr/bin/env python3


def part1(input_lines: list[str]) -> int:
    safe_count = 0
    for line in input_lines:
        inc_dec = None
        last_reading = None
        readings = [int(reading) for reading in line.split()]

        try:
            for reading in readings:
                if last_reading is None:
                    last_reading = reading
                    continue

                if inc_dec is None:
                    if reading > last_reading:
                        inc_dec = "inc"
                    elif reading < last_reading:
                        inc_dec = "dec"
                    else:
                        raise Exception("First readings were equal")

                if reading < last_reading and inc_dec == "inc":
                    raise Exception("Reading curve inverted")
                elif reading > last_reading and inc_dec == "dec":
                    raise Exception("Reading curve inverted")

                diff = abs(reading - last_reading)
                last_reading = reading
                if diff < 1 or diff > 3:
                    raise Exception("Readings out of safe range")

            safe_count += 1
        except Exception as e:
            print("Loop iteration was aborted for reason:", e)
            pass

    return safe_count


def part2_brute_force(input_lines: list[str]) -> int:
    # If you're wondering about the function name,
    # I had a whole setup involving multiple levels of
    # exceptions that tried to catch and throw out the
    # one bad input per line.
    # It didn't work. And I got tired of messing with it.
    # So here's the lazy way of handing it instead.
    safe_count = 0
    for line in input_lines:
        readings = [int(reading) for reading in line.split()]
        for i in range(-1, len(readings)):
            these_readings = readings.copy()
            if i > -1:
                these_readings.pop(i)
            if part2_process_line(these_readings):
                safe_count += 1
                break

    return safe_count


def part2_process_line(readings: list[int]) -> bool:
    inc_dec = None
    last_reading = None
    for reading in readings:
        if last_reading is None:
            last_reading = reading
            continue

        if inc_dec is None:
            if reading > last_reading:
                inc_dec = "inc"
            elif reading < last_reading:
                inc_dec = "dec"
            else:
                return False

        if reading < last_reading and inc_dec == "inc":
            return False
        elif reading > last_reading and inc_dec == "dec":
            return False

        diff = abs(reading - last_reading)
        if diff < 1 or diff > 3:
            return False
        last_reading = reading
    return True


def main():
    with open("day02.input.txt") as fin:
        input_lines = [line for line in fin if len(line.strip()) > 0]
        print(part1(input_lines))
        print(part2_brute_force(input_lines))


if __name__ == "__main__":
    main()
