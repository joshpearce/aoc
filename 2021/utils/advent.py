from pathlib import Path
from typing import Iterator, Tuple, List
from contextlib import suppress


def read_tuples_from_file(path: Path) -> Iterator[tuple]:
    with path.open("r") as file:
        for line in file.readlines():
                yield tuple(line.split(" "))

def read_num_array_from_file(path: Path) -> List[List[int]]:
    with path.open("r") as file:
        lines = file.read().split()
        return [list(map(int, list(line))) for line in lines]

def read_numbers_from_file(path: Path) -> Iterator[int]:
    with path.open("r") as file:
        for line in file.readlines():
            with suppress(ValueError):
                yield int(line)