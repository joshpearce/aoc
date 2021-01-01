from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set


def part1(navs: List[Tuple[str, int]]) -> None:
    origin = [0, 0, 0]
    cur = [0, 0, 0]
    mag = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}
    c2d = {"E": 0, "N": 90, "W": 180, "S": 270}

    for n, m in navs:
        if n == "F":
            cur[0] += mag[cur[2]][0] * m
            cur[1] += mag[cur[2]][1] * m
        elif n in (c2d.keys()):
            cur[0] += mag[c2d[n]][0] * m 
            cur[1] += mag[c2d[n]][1] * m
        elif n == "R":
            cur[2] = (cur[2]-m)%360
        elif n == "L":
            cur[2] = (cur[2]+m)%360

    dist = abs(origin[0]-cur[0]) + abs(origin[1]-cur[1])
    print(dist)

def part2(navs: List[Tuple[str, int]]) -> None:
    way = [10, 1]
    origin = [0, 0, 0]
    cur = [0, 0, 0]
    mag = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}
    c2d = {"E": 0, "N": 90, "W": 180, "S": 270}
    
    for n, m in navs:
        if n == "F":
            cur[0] += way[0] * m
            cur[1] += way[1] * m
        elif n in (c2d.keys()):
            way[0] += mag[c2d[n]][0] * m 
            way[1] += mag[c2d[n]][1] * m
        elif n in ("R", "L"):
            ang = -m%360 if n == "R" else m%360
            while ang > 0:
                way[0], way[1] = -way[1], way[0]
                ang -= 90
    
    dist = abs(origin[0]-cur[0]) + abs(origin[1]-cur[1])
    print(dist)
        

def run(file_path: Path) -> None:
    navs = [(n[0], int(n[1:])) for n in file_path.read_text().strip().split('\n')]
    part1(navs)
    part2(navs)
    



if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)