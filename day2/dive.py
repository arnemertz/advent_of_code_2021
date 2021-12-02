from typing import Iterable


def parse_line(line: str) -> tuple[str, int]:
    words: list[str] = line.split(' ')
    cmd: str = words[0]
    amount: int = int(words[1])
    return cmd, amount


def calculate_position(lines: Iterable[str]) -> tuple[int, int]:
    horizontal_pos: int
    depth: int
    horizontal_pos, depth = 0, 0
    for line in lines:
        cmd, amount = parse_line(line)
        match cmd:
            case "forward": horizontal_pos += amount
            case "down": depth += amount
            case "up": depth -= amount
            case _: assert False, f"unknown command: {cmd}"
    return horizontal_pos, depth


def calculate_position_with_aim(lines: Iterable[str]) -> tuple[int, int]:
    horizontal_pos: int
    depth: int
    aim: int
    horizontal_pos, depth, aim = 0, 0, 0
    for line in lines:
        cmd, amount = parse_line(line)
        match cmd:
            case "down":
                aim += amount
            case "up":
                aim -= amount
            case "forward":
                horizontal_pos += amount
                depth += aim*amount
            case _: assert False, f"unknown command: {cmd}"
    return horizontal_pos, depth


with open('input.txt') as in_file:
    hp, d = calculate_position_with_aim(line.strip() for line in in_file)
    print(hp * d)


EXAMPLE_INPUT = [
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2",
]


def test_calculate_position():
    assert calculate_position(EXAMPLE_INPUT) == (15, 10)


def test_calculate_position_with_aim():
    assert calculate_position_with_aim(EXAMPLE_INPUT) == (15, 60)
