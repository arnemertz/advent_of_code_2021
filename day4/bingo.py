from itertools import islice
from typing import Iterable, Optional

Numbers = list[int]
Entries = list[tuple[int, bool]]


class Board:

    def __init__(self, rows: list[Numbers]) -> None:
        assert len(rows) == 5
        assert all([len(row) == 5 for row in rows])
        self._rows: list[Entries] = [list(zip(row, [False] * len(row))) for row in rows]

    def row(self, idx: int) -> Entries:
        return self._rows[idx]

    def col(self, idx: int) -> Entries:
        return [row[idx] for row in self._rows]

    def mark(self, called_number: int) -> None:
        for row in self._rows:
            for n, entry in enumerate(row):
                if entry[0] == called_number:
                    row[n] = (called_number, True)

    @staticmethod
    def _full(entries: Entries) -> bool:
        return all(entry[1] for entry in entries)

    def has_bingo(self) -> bool:
        return any(self._full(row) for row in self._rows) \
               or any(self._full(self.col(n)) for n in range(0, len(self.row(0))))

    def unmarked_sum(self) -> int:
        return sum(sum(n for n, marked in row if not marked) for row in self._rows)


Boards = list[Board]


def parse_numbers(line: str, delim: Optional[str] = None) -> Numbers:
    return [int(number_str.strip()) for number_str in line.strip().split(delim)]


def parse_boards(lines: Iterable[str]) -> Iterable[Board]:
    # skip line 0, use lines 1-5 for the next board
    while values := list(parse_numbers(row) for row in islice(lines, 1, 6)):
        yield Board(values)


def parse_bingo(input_lines: Iterable[str]) -> tuple[Numbers, Boards]:
    lines = iter(input_lines)
    bingo_numbers = parse_numbers(next(lines), delim=',')
    return bingo_numbers, list(parse_boards(lines))


def bingo_score_first(input_lines: Iterable[str]) -> int:
    bingo_numbers, boards = parse_bingo(input_lines)
    for called_number in bingo_numbers:
        for board in boards:
            board.mark(called_number)
            if board.has_bingo():
                return board.unmarked_sum() * called_number
    return -1


def bingo_score_last(input_lines: Iterable[str]) -> int:
    bingo_numbers, boards = parse_bingo(input_lines)
    for called_number in bingo_numbers:
        for board in boards:
            board.mark(called_number)
        if len(boards) == 1 and boards[0].has_bingo():
            return boards[0].unmarked_sum() * called_number
        boards = [board for board in boards if not board.has_bingo()]
    return -1


if __name__ == '__main__':
    with open('input.txt') as in_file:
        print(bingo_score_last(in_file))

EXAMPLE_INPUTS = [
    "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
    "",
    "22 13 17 11  0",
    " 8  2 23  4 24",
    "21  9 14 16  7",
    " 6 10  3 18  5",
    " 1 12 20 15 19",
    "",
    " 3 15  0  2 22",
    " 9 18 13 17  5",
    "19  8  7 25 23",
    "20 11 10 24  4",
    "14 21 16 12  6",
    "",
    "14 21 17 24  4",
    "10 16 15  9 19",
    "18  8 23 26 20",
    "22 11 13  6  5",
    " 2  0 12  3  7",
]

EXAMPLE_BOARD_VALUES: list[Numbers] = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25],
]


def test_board_values() -> None:
    board = Board(EXAMPLE_BOARD_VALUES)
    assert board.row(4) == [(21, False), (22, False), (23, False), (24, False), (25, False)]
    assert board.col(2) == [(3, False), (8, False), (13, False), (18, False), (23, False)]


def test_board_vertical_bingo() -> None:
    board = Board(EXAMPLE_BOARD_VALUES)
    for n in [2, 7, 12, 17, 22]:
        board.mark(n)
    assert board.has_bingo()


def test_board_horizontal_bingo() -> None:
    board = Board(EXAMPLE_BOARD_VALUES)
    for n in [11, 12, 13, 14, 15]:
        board.mark(n)
    assert board.has_bingo()


def test_parse_bingo() -> None:
    bingo_numbers, boards = parse_bingo(EXAMPLE_INPUTS)
    assert bingo_numbers[0] == 7
    assert bingo_numbers[-1] == 1
    assert len(bingo_numbers) == 27
    assert len(boards) == 3
    board: Board = boards[0]
    assert board.row(0) == list(zip([22, 13, 17, 11, 0], [False]*5))
    assert board.col(1) == list(zip([13, 2, 9, 10, 12], [False]*5))


def test_bingo_score_first() -> None:
    assert bingo_score_first(EXAMPLE_INPUTS) == 4512


def test_bingo_score_last() -> None:
    assert bingo_score_last(EXAMPLE_INPUTS) == 1924
