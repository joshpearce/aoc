from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set

def part1(sorted_nums: List[int]) -> None:
    ones = 1 if sorted_nums[0] > 0 else 0
    threes = 1
    for i in range(len(sorted_nums)-1):
        if sorted_nums[i+1] - sorted_nums[i] == 1:
            ones += 1
        elif sorted_nums[i+1] - sorted_nums[i] == 3:
            threes += 1
        elif sorted_nums[i+1] - sorted_nums[i] > 3:
            raise Exception('greater than 3')
    print (ones*threes)

# from rune_kg here: https://www.reddit.com/r/adventofcode/comments/ka8z8x/2020_day_10_solutions/
def dfc(dag: Dict[int, Tuple[int, int, int]], v: int, mem: Dict[int, int]={}) -> int:
    if v in mem:
        return mem[v]
    elif dag[v]: 
        mem[v] = sum(dfc(dag, x, mem) for x in dag[v])
        return mem[v]

    return 1

#from https://github.com/James-Ansley/adventofcode/blob/master/answers/day10.py
def walk(adapters: List[int]) -> int:
    paths = [0] * (len(adapters)-1) + [1]
    for i in range(len(adapters)-1, -1, -1):
        for j in range(i+1, i+4):
            if j < len(adapters) and adapters[j] - 3 <= adapters[i]:
                paths[i] += paths[j]
    return paths[0]

def part2(sorted_nums: List[int]) -> None:
    adapters = [0] + sorted_nums + [sorted_nums[-1]+3]
    dag = dict([(x, {y for y in range(x+1, x+4) if y in adapters}) for x in adapters])

    print(dfc(dag, 0, {}))
    print(walk(adapters))
    

def run(file_path: Path) -> None:
    nums = [int(l) for l in file_path.read_text().split('\n')[0:-1]]
    sorted_nums = sorted(nums)

    part1(sorted_nums)
    part2(sorted_nums)

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)