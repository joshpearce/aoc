from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
import re
from collections import defaultdict

def part1(numbers: List[int], stop: int) -> int:
    last_seen: Dict[int, List[int]] = defaultdict(list, {v: [i] for i, v in enumerate(numbers)})
    i = len(numbers)
    last = numbers[-1]
    
    while i < stop:
        prev = last_seen.get(last)
        if len(prev) == 1 and prev[0] == i-1:
            last = 0 
        else:
            last = prev[1] - prev[0]
        last_seen |= {last: last_seen[last][-1:] + [i]}
        i += 1
    return last
    

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])

    print(part1([6,3,15,13,1,0], 2020))
    print(part1([6,3,15,13,1,0], 30000000))
    #part2(file_path)