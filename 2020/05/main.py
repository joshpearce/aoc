from pathlib import Path
import sys
from typing import List, Tuple


def run(file_path: Path) -> None:
    seats = bytearray(128)

    with file_path.open("r") as file:
        for line in file.readlines():
            idx, bit = 0, 64
            for i in range(7):
                if line[i] == "B":
                    idx ^= bit 
                bit = bit >> 1
            shift, bit = 0, 4 
            for i in range(7,10):
                if line[i] == "R":
                    shift ^= bit 
                bit = bit >> 1
            seats[idx] ^= (1 << shift)
    
    row = 127
    while row >= 0:
        if (int(seats[row]) < 255):
            print (f'row: {row}, seat int: {int(seats[row])}')
        row -= 1
    


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)