#!/usr/bin/env python3

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from typing import Iterator
from contextlib import suppress
from utils import advent


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    nums = list(advent.read_numbers_from_file(file_path))

    # part 1
    increases = [1 if nums[i-1] < nums[i] else 0 for i in range(1, len(nums))]
    print(sum(increases))

    # part 2
    increases = [1 if sum(nums[i-3:i]) < sum(nums[i-2:i+1]) else 0 for i in range(3, len(nums))]
    print(sum(increases))

    