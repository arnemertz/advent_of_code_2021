from typing import Iterable, Iterator


def split_bits(lines: Iterable[str]) -> Iterable[list[int]]:
    for line in lines:
        yield [int(digit) for digit in line]


def bits_to_int(bits: list[int]) -> int:
    result: int = 0
    for bit in bits:
        result = (result << 1) + bit
    return result


def calculate_gamma_epsilon_rates(input_lines: Iterable[str]) -> tuple[int, int]:
    lines: Iterator[list[int]] = iter(split_bits(input_lines))
    line_count: int = 1
    accumulated_bits: list[int] = next(lines)
    for bits in lines:
        line_count += 1
        accumulated_bits = [a + b for a, b in zip(accumulated_bits, bits, strict=True)]

    def common_is_1(accumulated_bit: int) -> bool:
        par: float = line_count / 2
        assert accumulated_bit != par
        return accumulated_bit > par

    gamma_bits: list[int] = [1 if common_is_1(a) else 0 for a in accumulated_bits]
    epsilon_bits: list[int] = [0 if common_is_1(a) else 1 for a in accumulated_bits]

    return bits_to_int(gamma_bits), bits_to_int(epsilon_bits)


with open('input.txt') as in_file:
    g, e = calculate_gamma_epsilon_rates(line.strip() for line in in_file)
    print(g * e)

EXAMPLE_INPUT = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]


def test_split_bits() -> None:
    assert list(split_bits(EXAMPLE_INPUT)) == [
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 1, 1, 0],
        [1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
    ]


def test_bits_to_int() -> None:
    assert bits_to_int([1, 0, 1, 1, 0]) == 22
    assert bits_to_int([0, 1, 0, 0, 1]) == 9


def test_calculate_gamma_epsilon_rates() -> None:
    assert calculate_gamma_epsilon_rates(EXAMPLE_INPUT) == (22, 9)
