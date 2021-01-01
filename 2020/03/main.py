from pathlib import Path
import sys
from typing import List

def get_map(file_path: Path) -> List[List[int]]:
    map: List[List[int]] = []
    with file_path.open("r") as file:
        for line in file.readlines():
            map.append([1 if c == '#' else 0 for c in line])
    return map

def sled(right_by: int, down_by: int, map: List[List[int]]) -> int:
    width = len(map[0])-1
    height = len(map)-1
    x,y,trees = 0,0,0

    while (y <= height):
        pos = map[y][x%width]
        if pos:
            trees +=1
        x += right_by
        y += down_by
    
    return trees

def run(file_path: Path) -> None:
    map = get_map(file_path)
    print (sled(3, 1, map))
    print (
        sled(1, 1, map) *
        sled(3, 1, map) * 
        sled(5, 1, map) * 
        sled(7, 1, map) * 
        sled(1, 2, map)
    )

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)