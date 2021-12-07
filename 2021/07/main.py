#!/usr/bin/env python3

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from utils import advent
from collections import defaultdict, Counter

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    file_lines = advent.read_lines_from_file(file_path)
    hs = list(map(int, file_lines[0].split(",")))
    hr = range(min(hs), max(hs) + 1)

    # part 1
    hp = [sum([abs(r - s) for s in hs]) for r in hr]
    m = min(hp)
    print(m)

    # part 2
    hp = [sum([sum(range(0, abs(r - s) + 1)) for s in hs]) for r in hr]
    m = min(hp)
    print(m)
    