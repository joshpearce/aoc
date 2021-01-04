from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
import re
from itertools import product

# refactored with some python simplifications from 
# https://github.com/James-Ansley/adventofcode/blob/master/answers/day14.py

def part1(file_path: Path):
    mem_line_re = re.compile('mem\\[([0-9]+)\\] = ([0-9]+)')
    mem: Dict[int, List[int]] = {}
    and_mask = 0
    or_mask = 0

    for line in file_path.read_text().strip().split('\n'):
        if line[0:2] == "ma":
            mask = line[7:]
            and_mask = int(mask.replace("X", "1"), 2)
            or_mask = int(mask.replace("X", "0"), 2)
        else:
            idx, val = map(int, mem_line_re.match(line).groups())
            mem[idx] = val & and_mask | or_mask

    print(sum(mem.values()))

def part2(file_path: Path):
    mem_line_re = re.compile('mem\\[([0-9]+)\\] = ([0-9]+)')
    mem: Dict[int, int] = {}
    flt_idxs = None
    or_mask = 0

    for line in file_path.read_text().strip().split('\n'):
        if line[0:2] == "ma":
            mask = line[7:]
            flt_idxs = [i for i,v in enumerate(reversed(mask)) if v == 'X']
            or_mask = int(mask.replace("X", "0"), 2)
        else:
            idx, val = map(int, mem_line_re.match(line).groups())
            addrs = [idx | or_mask]

            for i in flt_idxs:
                temp_addrs = [addr | (1 << i)for addr in addrs]
                addrs = [addr & ~(1 << i)for addr in addrs]
                addrs += temp_addrs
            mem |= {addr: int(val) for addr in addrs}

    print(sum(mem.values()))

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])

    part1(file_path)
    part2(file_path)
