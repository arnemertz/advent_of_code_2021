from collections.abc import Iterable, Reversible

Coordinate = tuple[int, int]
Line = tuple[Coordinate, Coordinate]


def parse_coordinate(in_c: str) -> Coordinate:
    numbers = in_c.split(',')
    assert len(numbers) == 2
    return int(numbers[0]), int(numbers[1])


def parse_lines(input_lines: Iterable[str]) -> Iterable[Line]:
    for line in input_lines:
        coordinates = line.strip().split(' -> ')
        assert len(coordinates) == 2
        yield parse_coordinate(coordinates[0]), parse_coordinate(coordinates[1])


def inclusive_asc_range(n1: int, n2: int) -> Reversible[int]:
    if n1 <= n2:
        return range(n1, n2 + 1)
    return range(n2, n1 + 1)


def diagonal_coordinates(start: Coordinate, end: Coordinate) -> set[Coordinate]:
    if start[0] > end[0]:
        return diagonal_coordinates(end, start)
    x_range: Iterable[int] = range(start[0], end[0] + 1)
    y_range: Iterable[int]
    if start[1] <= end[1]:
        assert end[1] - start[1] == end[0] - start[0]
        y_range = inclusive_asc_range(start[1], end[1])
    else:
        assert start[1] - end[1] == end[0] - start[0]
        y_range = reversed(inclusive_asc_range(start[1], end[1]))
    return set(zip(x_range, y_range, strict=True))


def to_coordinates(line: Line) -> set[Coordinate]:
    c1, c2 = line
    if c1[0] == c2[0]:  # vertical
        return {(c1[0], y) for y in inclusive_asc_range(c1[1], c2[1])}
    elif c1[1] == c2[1]:  # horizontal
        return {(x, c1[1]) for x in inclusive_asc_range(c1[0], c2[0])}
    return diagonal_coordinates(c1, c2)


def collect_overlaps(lines: Iterable[Line]) -> set[Coordinate]:
    overlaps: set[Coordinate] = set()
    single_coordinates: set[Coordinate] = set()
    for line in lines:
        new_coordinates: set[Coordinate] = to_coordinates(line)
        overlaps |= single_coordinates & new_coordinates
        single_coordinates = single_coordinates ^ (new_coordinates - overlaps)
    return overlaps


def count_overlaps(lines: Iterable[Line]) -> int:
    return len(collect_overlaps(lines))


def task2() -> None:
    with open('input.txt') as in_file:
        lines: Iterable[Line] = parse_lines(in_file)
        print(count_overlaps(lines))


if __name__ == '__main__':
    task2()

EXAMPLE_INPUT = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]


def test_parse_lines() -> None:
    assert list(parse_lines(EXAMPLE_INPUT)) == [
        ((0, 9), (5, 9)),
        ((8, 0), (0, 8)),
        ((9, 4), (3, 4)),
        ((2, 2), (2, 1)),
        ((7, 0), (7, 4)),
        ((6, 4), (2, 0)),
        ((0, 9), (2, 9)),
        ((3, 4), (1, 4)),
        ((0, 0), (8, 8)),
        ((5, 5), (8, 2)),
    ]


def test_to_coordinates() -> None:
    horizontal_line: Line = ((0, 6), (5, 6))
    vertical_line: Line = ((1, 3), (1, 7))
    vertical_desc_line = ((1, 7), (1, 3))
    assert to_coordinates(horizontal_line) == {(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)}
    assert to_coordinates(vertical_line) == {(1, 3), (1, 4), (1, 5), (1, 6), (1, 7)}
    assert to_coordinates(vertical_desc_line) == {(1, 3), (1, 4), (1, 5), (1, 6), (1, 7)}
    diagonal_line1: Line = ((1, 3), (3, 5))
    diagonal_line2: Line = ((3, 5), (1, 3))
    diagonal_line3: Line = ((4, 1), (1, 4))
    assert to_coordinates(diagonal_line1) == {(1, 3), (2, 4), (3, 5)}
    assert to_coordinates(diagonal_line2) == {(1, 3), (2, 4), (3, 5)}
    assert to_coordinates(diagonal_line3) == {(4, 1), (3, 2), (2, 3), (1, 4)}


def test_collect_overlaps() -> None:
    assert collect_overlaps(parse_lines(EXAMPLE_INPUT)) == {
        (7, 1), (2, 2), (5, 3), (7, 3),
        (3, 4), (4, 4), (6, 4), (7, 4),
        (5, 5), (0, 9), (1, 9), (2, 9),
    }


def test_count_overlaps() -> None:
    assert count_overlaps(parse_lines(EXAMPLE_INPUT)) == 12
