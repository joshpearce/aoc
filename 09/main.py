from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
import itertools


def part1(nums: List[int]) -> int:
    i, dist,  = 0, 25
    end_loop = len(nums) - dist
    for i in range(end_loop):
        win = nums[i:i+dist]
        sums = [a+b for a,b in itertools.combinations(win, 2)]
        if nums[i+dist] not in sums:
            return nums[i+dist]

def part2(nums: List[int], invalid_num: int) -> int:
    for i in range(2, len(nums)):
        for j in range(0, len(nums)-i):
            if invalid_num == sum(nums[j:j+i]):
                return min(nums[j:j+i]) + max(nums[j:j+i])

def run(file_path: Path) -> None:
    nums = [int(l) for l in file_path.read_text().split('\n')[0:-1]]
    invalid_num = part1(nums)
    print(invalid_num)
    print(part2(nums, invalid_num))

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)