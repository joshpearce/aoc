from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
from pprint import pprint


def status_at(r: int, c: int, seats: List[str]) -> str:
    width, height = len(seats[0]), len(seats)
    if r < 0 or r >= height:
        return " "
    if c < 0 or c >= width:
        return " "
    return seats[r][c]

def occ_sightline(r: int, c: int, seats: List[str], extent: int = 1) -> int:

    vecs = ['.'] * 8
    for m in range(1, extent+1):
        n = status_at(r-m,c, seats)
        ne = status_at(r-m, c+m, seats)
        e = status_at(r, c+m, seats)
        se = status_at(r+m, c+m, seats)
        s = status_at(r+m, c, seats)
        sw = status_at(r+m, c-m, seats)
        w = status_at(r, c-m, seats)
        nw = status_at(r-m, c-m, seats)

        cur = [n, ne, e, se, s, sw, w, nw]
        for i in range(8):
            if vecs[i] not in ('L', '#', ' '):
                vecs[i] = cur[i]

        if all(x in ('L', '#', ' ') for x in vecs):
            break

    return sum([1 if x == '#' else 0 for x in vecs])


def count_filled(seats: List[str]) -> int:
    return sum([1 if c == '#' else 0 for r in seats for c in r])

def seat_ppl(seats: List[str], extent: int = 1) -> List[str]:
    w, h = len(seats[0]), len(seats)
    new_seats = [
                ''.join(['#' 
                    if seats[r][c] == 'L' and occ_sightline(r, c, seats, extent) == 0 
                    else seats[r][c] 
                    for c in range(0, w)
                ])
            for r in range(0, h)]
    return new_seats

def unseat_ppl(seats: List[str], extent: int = 1, tolerence: int = 4) -> List[str]:
    w, h = len(seats[0]), len(seats)
    new_seats = [
                ''.join(['L' 
                    if seats[r][c] == '#' and occ_sightline(r, c, seats, extent) >= tolerence 
                    else seats[r][c] 
                    for c in range(0, w)
                ])
            for r in range(0, h)]
    return new_seats

def run_part(seats: List[str], extent: int, tolerence: int) -> None:
    seating, count, rounds = True, 0, 0

    while True:
        seats = seat_ppl(seats, extent) if seating else unseat_ppl(seats, extent, tolerence)
        new_count = count_filled(seats)
        rounds += 1
        if new_count == count:
            break
        else:
            count = new_count
            seating = not seating
    
    print(f'Seating stablized to {count} occupants in {rounds} rounds.')



def run(file_path: Path) -> None:
    seats = file_path.read_text().strip().split('\n')
    
    #run_part(seats, 1, 4)
    run_part(seats, 100, 5)


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)