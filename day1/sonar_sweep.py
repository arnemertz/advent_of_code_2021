from typing import Optional, Iterable


def count_depth_increases(depths: Iterable[int]) -> int:
    depth_increases: int = 0
    previous_depth: Optional[int] = None
    for depth in depths:
        if previous_depth is not None and depth > previous_depth:
            depth_increases += 1
        previous_depth = depth
    return depth_increases


# test with the example from the task
def test_count_depth_increases():
    example_input = [
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
    assert count_depth_increases(example_input) == 7


with open('input.txt') as in_file:
    print(count_depth_increases(int(line.strip()) for line in in_file))
