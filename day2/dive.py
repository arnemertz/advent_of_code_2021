from typing import Iterable


def calculate_position(lines: Iterable[str]) -> tuple[int, int]:
    horizontal_pos: int
    depth: int
    horizontal_pos, depth = 0, 0
    for line in lines:
        words: list[str] = line.split(' ')
        cmd: str = words[0]
        amount: int = int(words[1])
        match cmd:
            case "forward": horizontal_pos += amount
            case "down": depth += amount
            case "up": depth -= amount
            case _: assert False, f"unknown command: {cmd}"
    return horizontal_pos, depth


with open('input.txt') as in_file:
    hp, d = calculate_position(line.strip() for line in in_file)
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
