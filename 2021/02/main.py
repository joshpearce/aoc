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
    commands = list(advent.read_tuples_from_file(file_path))

    #part 1
    horz, depth = 0, 0
    for v, m in commands:
        m = int(m)
        if v == 'forward':
            horz += m
        elif v == 'up':
            depth -= m
        elif v == 'down':
            depth += m
    print (horz * depth)

    # part 2
    horz, depth, aim = 0, 0, 0
    for v, m in commands:
        m = int(m)
        if v == 'forward':
            horz += m
            depth += m*aim
        elif v == 'up':
            aim -= m
        elif v == 'down':
            aim += m
    print (horz * depth)


        

