from pathlib import Path
import sys
from typing import Iterator, Tuple

def read_values_from_file(path: Path) -> Iterator[Tuple[str, int, int, str, bool]]:
    with path.open("r") as file:
        for line in file.readlines():
            parts = line.split(' ')
            min, max = [int(n) for n in parts[0].split('-')]
            char = parts[1][0]
            pwd = parts[2]
            count = pwd.count(char)
            valid = count >= min and count <= max
            yield (char, min, max, pwd, valid)


def run(file_path: Path) -> None:
    values = list(read_values_from_file(file_path))
    total = sum([1 if v[4] else 0 for v in values])
    print (total)
    total2 = sum([1 if (v[3][v[1]-1] == v[0]) ^ (v[3][v[2]-1] == v[0]) else 0 for v in values])
    print (total2)



if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)