#!/usr/bin/env python3

from pathlib import Path
import sys
from typing import Iterator
from contextlib import suppress

def read_numbers_from_file(path: Path) -> Iterator[int]:
    with path.open("r") as file:
        for line in file.readlines():
            with suppress(ValueError):
                yield int(line)


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    nums = list(read_numbers_from_file(file_path))

    # part 1
    increases = sum(b > a for a, b in zip(nums, nums[1:]))
    print(increases)

    # part 2
    increases = sum(b > a for a, b in zip(nums, nums[3:]))
    print(increases)

    