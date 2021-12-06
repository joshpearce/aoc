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

    # part 1
    state = list(map(int, file_lines[0].split(",")))

    for _ in range(80):
        new = [8] * state.count(0)
        new_state = [
            (v-1) % 7 if v < 7 else v-1  for i, v in enumerate(state)
        ]
        new_state.extend(new)
        state = new_state
    
    print(len(state))

    # part 2
    next_state = {
        8 : 7,
        7 : 6,
        6 : 5,
        5 : 4, 
        4 : 3,
        3 : 2,
        2 : 1,
        1 : 0,
        0 : 6 
    }

    state_0 = list(map(int, file_lines[0].split(",")))
    state_count = Counter(state_0)

    for _ in range(256):
        new = state_count[0]
        new_state_count = defaultdict(int)
        for k, v in state_count.items():
            if v > 0:
                new_state_count[next_state[k]] += v
        new_state_count[8] = new
        state_count = new_state_count
    
    print(sum(state_count.values()))

    
