#!/usr/bin/env python3

from os import error
import numpy as np
from itertools import product

def get_neighbors(x, y, mx, my):
    return { *list(product(
        range(max(x - 1, 0), min(x + 1, mx) + 1), 
        range(max(y - 1, 0), min(y + 1, my) + 1))) } - {(x, y)}
    

def part_one(lines, steps):
    a = np.array([[*l] for l in lines], np.int32)
    lx, ly = a.shape[0], a.shape[1]
    flashed = set()
    for _ in range(steps):
        for x, y in flashed:
            a[(x, y)] = 0
        if (a == 0).all():
            return _
        flashed = set()
        a = a + 1
        pl = -1
        
        while len(flashed) > pl:
            pl = len(flashed)
            for x in range(lx):
                for y in range(ly):
                    if (x, y) not in flashed:
                        if a[(x, y)] > 9:
                            flashed.add((x, y))
                            for i, j in get_neighbors(x, y, lx - 1, ly - 1):
                                a[(i, j)] += 1
    return flash_count


def part_two():
    
    pass


if __name__ == '__main__':
    from pathlib import Path

    #f = 'test.txt'
    f = 'input.txt'
    lines = (Path(__file__).parent / f).open().read().split('\n')
    print("Part one:")
    print(f"  {part_one(lines, 10000)}")

    #print("Part two:")
    #print(f"  {part_two()}")
    