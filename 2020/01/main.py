from pathlib import Path
import sys
from typing import Iterable, Iterator, List, Tuple, Union
from contextlib import suppress

def read_numbers_from_file(path: Path) -> Iterator[int]:
    with path.open("r") as file:
        for line in file.readlines():
            with suppress(ValueError):
                yield int(line)

def find_two_for_total(sorted_numbers: List[int], total: int) -> Union[Tuple[int, int], None]:
    i = 0
    j = len(sorted_numbers)-1

    while i != j:
        n1 = sorted_numbers[i]
        n2 = sorted_numbers[j]
        sum = n1 + n2
        if sum == total:
            return n1,n2
        elif sum > total:
            j -= 1
        else:
            i += 1
    
    return None

def part1(numbers: List[int]) -> int:
    sorted_numbers = sorted(numbers)
    values = find_two_for_total(sorted_numbers, 2020)
    if values:
        n1,n2 = values
        return n1*n2
    return -1

def part2(numbers: List[int]) -> int:
    sorted_numbers = sorted(numbers)
    for n in numbers:
        total = 2020-n
        if total > 1:
            values = find_two_for_total(sorted_numbers, total)
            if values:
                n1,n2 = values
                return n*n1*n2
    return -1
            

def run(file_path: Path) -> None:
    nums = list(read_numbers_from_file(file_path))
    print(part1(nums))
    print(part2(nums))


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)