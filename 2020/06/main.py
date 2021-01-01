from pathlib import Path
import sys
from typing import List, Tuple


def run(file_path: Path) -> None:
    ans: List[int] = [0] * 26
    total = 0
    group_size = 0
    with file_path.open("r") as file:
        for line in file.readlines():
            if len(line.strip()) == 0:
                total += sum([1 for a in ans if a == group_size])
                ans = [0] * 26
                group_size = 0
            else:
                group_size += 1
                for a in line.strip():
                    ans[ord(a)-97] += 1
    print (total)
    


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)