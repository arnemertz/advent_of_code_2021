from collections.abc import Iterable
from collections import Counter


def debug_dict(d: dict[int, int]) -> str:
    return ', '.join([f'{a}: {b}' for a, b in sorted(d.items()) if b != 0])


def lanternfish_simulation(start_population: list[int], days: int) -> Counter[int]:
    population = Counter(start_population)
    for i in range(days):
        younger_pop = Counter({days - 1: count for days, count in population.items() if days != 0})
        new_births = {6: population[0], 8: population[0]}
        population = younger_pop
        population.update(new_births)
    return population


def parse_start_population(input_lines: Iterable[str]) -> list[int]:
    return [int(p.strip()) for p in next(iter(input_lines)).strip().split(',')]


def task1(input_lines: Iterable[str]) -> int:
    start_population: list[int] = parse_start_population(input_lines)
    return lanternfish_simulation(start_population, 80).total()


if __name__ == '__main__':
    with open('input.txt') as in_file:
        print(task1(in_file))

EXAMPLE_INPUT = [
    "3,4,3,1,2"
]


def test_parse_start_population() -> None:
    assert parse_start_population(EXAMPLE_INPUT) == [3, 4, 3, 1, 2]


def equal_pops(lhs: Counter[int], rhs: list[int]) -> bool:
    return Counter({a: b for a, b in lhs.items() if b != 0}) == Counter(rhs)


def test_lanternfish_simulation() -> None:
    start_population: list[int] = parse_start_population(EXAMPLE_INPUT)
    assert equal_pops(lanternfish_simulation(start_population, 0), start_population)
    assert equal_pops(lanternfish_simulation(start_population, 1), [2, 3, 2, 0, 1])
    assert equal_pops(lanternfish_simulation(start_population, 2), [1, 2, 1, 6, 0, 8])
    assert equal_pops(lanternfish_simulation(start_population, 3), [0, 1, 0, 5, 6, 7, 8])
    assert equal_pops(lanternfish_simulation(start_population, 4), [6, 0, 6, 4, 5, 6, 7, 8, 8])
    assert equal_pops(lanternfish_simulation(start_population, 5), [5, 6, 5, 3, 4, 5, 6, 7, 7, 8])
    assert lanternfish_simulation(start_population, 18) == Counter(
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8]
    )
    assert lanternfish_simulation(start_population, 18).total() == 26
    assert lanternfish_simulation(start_population, 80).total() == 5934
