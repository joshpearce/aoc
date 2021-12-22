#!/usr/bin/env python3

# figure this out
# https://github.com/ebouteillon/advent-of-code-2021/blob/main/day-20/part12.py

import numpy as np

PADDING = 5

def pad(a, n=PADDING):
    return np.pad(a, ((n, n), (n, n)))

def a2i(a):
    a_ = a.flatten()
    return int("".join(str(x) for x in a_), 2)

def printa(a):
    print()
    for row in a:
        print("".join(["#" if x == 1 else "." for x in row]))
    print()

def enhance(a, alg):
    ap = pad(a)
    an = np.zeros(ap.shape, dtype=int)
    for j in range(1, ap.shape[0]-1):
        for i in range(1, ap.shape[0]-1):
            x3 = ap[j-1:j+2, i-1:i+2]
            v = a2i(x3)
            px = alg[v]
            an[j, i] = px
    return an[1:-1, 1:-1]

def part_one(img, alg):
    printa(img)
    img = enhance(img, alg)
    printa(img)
    img = enhance(img, alg)
    printa(img)
    img = img[PADDING+1: -PADDING-1, PADDING+1: -PADDING-1]
    printa(img)

    return np.sum(img)

def part_two(img, alg):
    
    printa(img)
    for i in range(25):
        img = enhance(img, alg)
        printa(img)
        img = enhance(img, alg)
        printa(img)
        img = img[PADDING+1: -PADDING-1, PADDING+1: -PADDING-1]
        printa(img)
    

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    #f = "input.txt"
    lines = (Path(__file__).parent / f).open().read().split("\n")
    
    alg = [1 if x == "#" else 0 for x in lines[0]]
    img = np.array([ [1 if x == "#" else 0 for x in l] for l in lines[2:]])

    print("\nPart one:")
    print(f"{part_one(img, alg)}")

    print("Part two:")
    #print(f"{part_two(img, alg)}")
    