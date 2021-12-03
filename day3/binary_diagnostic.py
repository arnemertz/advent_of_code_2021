from typing import Iterable, Iterator, Callable

Bits = list[int]


def split_bits(lines: Iterable[str]) -> Iterable[Bits]:
    for line in lines:
        yield [int(digit) for digit in line]


def bits_to_int(bits: Bits) -> int:
    result: int = 0
    for bit in bits:
        result = (result << 1) + bit
    return result


def accumulate_bits(bit_lines: Iterable[Bits]):
    lines: Iterator[Bits] = iter(bit_lines)
    line_count: int = 1
    accumulated_bits: Bits = next(lines)
    for bits in lines:
        line_count += 1
        accumulated_bits = [a + b for a, b in zip(accumulated_bits, bits, strict=True)]
    return line_count, accumulated_bits


def most_common_bit(bit_lines: Iterable[Bits], index: int) -> int:
    line_count: int
    accumulated_bits: Bits
    line_count, accumulated_bits = accumulate_bits(bit_lines)
    par: float = line_count / 2
    return 1 if accumulated_bits[index] >= par else 0


def least_common_bit(bit_lines: Iterable[Bits], index: int) -> int:
    line_count: int
    accumulated_bits: Bits
    line_count, accumulated_bits = accumulate_bits(bit_lines)
    par: float = line_count / 2
    return 0 if accumulated_bits[index] >= par else 1


def calculate_gamma_epsilon_rates(input_lines: Iterable[str]) -> tuple[int, int]:
    bit_lines: list[Bits] = list(split_bits(input_lines))
    gamma_bits: Bits = [most_common_bit(bit_lines, idx) for idx in range(0, len(bit_lines[0]))]
    epsilon_bits: Bits = [least_common_bit(bit_lines, idx) for idx in range(0, len(bit_lines[0]))]
    return bits_to_int(gamma_bits), bits_to_int(epsilon_bits)


def filter_bit_lines(bit_lines: Iterable[Bits], criteria: Bits) -> Iterable[Bits]:
    for bits in bit_lines:
        if all(bit == filter_bit for bit, filter_bit in zip(bits, criteria)):
            yield bits


def _calculate_filter_bit_rating(input_bits: list[Bits], get_filter_bit: Callable[[Iterable[Bits], int], int]) -> int:
    candidates: list[Bits] = input_bits
    filter_criteria: Bits = []
    while len(candidates) > 1:
        significant_bit_index: int = len(filter_criteria)
        filter_criteria.append(get_filter_bit(candidates, significant_bit_index))
        candidates = list(filter_bit_lines(candidates, filter_criteria))
    assert len(candidates) == 1
    return bits_to_int(candidates[0])


def calculate_oxygen_co2_scrubber_rating(input_lines: Iterable[str]) -> tuple[int, int]:
    input_bits: list[Bits] = list(split_bits(input_lines))
    oxygen_rating: int = _calculate_filter_bit_rating(input_bits, most_common_bit)
    co2_scrubber_rating = _calculate_filter_bit_rating(input_bits, least_common_bit)
    return oxygen_rating, co2_scrubber_rating


with open('input.txt') as in_file:
    o, c = calculate_oxygen_co2_scrubber_rating(line.strip() for line in in_file)
    print(o * c)

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


def test_most_common_bit() -> None:
    bit_lines = list(split_bits(EXAMPLE_INPUT))
    assert most_common_bit(bit_lines, 0) == 1
    assert most_common_bit(bit_lines, 1) == 0
    assert most_common_bit([[0], [1]], 0) == 1


def test_least_common_bit() -> None:
    bit_lines = list(split_bits(EXAMPLE_INPUT))
    assert least_common_bit(bit_lines, 0) == 0
    assert least_common_bit(bit_lines, 1) == 1
    assert least_common_bit([[0], [1]], 0) == 0


def test_filter_bit_lines() -> None:
    bit_lines = list(split_bits(EXAMPLE_INPUT))
    assert list(filter_bit_lines(bit_lines, [1, 0])) == [
        [1, 0, 1, 1, 0],
        [1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0],
    ]
    assert list(filter_bit_lines(bit_lines, [1, 1, 1])) == [
        [1, 1, 1, 1, 0],
        [1, 1, 1, 0, 0],
    ]


def test_calculate_oxygen_co2_scrubber_rating() -> None:
    assert calculate_oxygen_co2_scrubber_rating(EXAMPLE_INPUT) == (23, 10)
