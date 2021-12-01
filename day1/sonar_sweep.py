from typing import Optional, Iterable


def count_depth_increases(depths: Iterable[int]) -> int:
    depth_increases: int = 0
    previous_depth: Optional[int] = None
    for depth in depths:
        if previous_depth is not None and depth > previous_depth:
            depth_increases += 1
        previous_depth = depth
    return depth_increases


SLIDING_WINDOW_SIZE: int = 3


def sliding_windows(numbers: Iterable[int]) -> Iterable[int]:
    windows = []

    def add_to_windows(number: int):
        for i in range(0, len(windows)):
            windows[i] += number
        windows.append(number)

    # prime the deque so the following iterations can return a value
    number_iter = iter(numbers)
    for _ in range(0, SLIDING_WINDOW_SIZE - 1):
        add_to_windows(next(number_iter))

    for n in number_iter:
        add_to_windows(n)
        yield windows.pop(0)


def count_sliding_window_increases(depths: Iterable[int]):
    return count_depth_increases(sliding_windows(depths))


with open('input.txt') as in_file:
    print(count_sliding_window_increases(int(line.strip()) for line in in_file))

# test with the example from the task
EXAMPLE_INPUT = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263
]


def test_count_depth_increases():
    assert count_depth_increases(EXAMPLE_INPUT) == 7


def test_sliding_windows():
    assert list(sliding_windows(EXAMPLE_INPUT)) == [607, 618, 618, 617, 647, 716, 769, 792]


def test_count_sliding_window_increases():
    assert count_sliding_window_increases(EXAMPLE_INPUT) == 5
