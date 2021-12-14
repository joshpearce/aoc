#!/usr/bin/env python3

from collections import namedtuple
import numpy as np

Point = namedtuple('Point', ['x', 'y'])

def print_paper(p):
    print(p.T)
    print()

def print_paper2(p):
    text = [['X' if x > 0 else ' ' for x in line ] for line in p]
    for t in text:
        print("".join(t))

def part_one(points, folds):
    mx = max(p.x for p in points)
    my = max(p.y for p in points)
    paper = np.zeros((mx+1, my+1))
    paper[tuple(np.array(points).T.tolist())] += 1
    print_paper(paper)
    pfs = [paper]
    for fold in folds:
        
        p1_ = np.delete(pfs[-1], slice(fold[0], None), fold[1])
        p2_ = np.delete(pfs[-1], slice(fold[0]+1), fold[1])

        print_paper(p1_)
        print_paper(p2_)
        p1, p2 = p1_, p2_ #pad_resize(p1_, p2_)
        print_paper(p1)
        print_paper(p2)
        folded = p1 + np.flip(p2, fold[1])
        pfs.append(folded)
        print_paper(folded)
        print(f"Folded points: {sum(x > 0 for x in folded.flatten())}\n")

    print_paper2(pfs[-1].T)
            
def part_two():
    
    pass


if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    #f = "input.txt"
    parts = (Path(__file__).parent / f).open().read().split("\n\n")
    points = []
    for coord in parts[0].split("\n"):
        points.append(Point(*map(int, coord.split(","))))
    
    folds = []
    for fold in parts[1].split("\n"):
        fold = fold.split(" ")[2].split("=")
        folds.append((int(fold[1]), 0 if fold[0] == "x" else 1))

    print("Part one:")
    print(f"  {part_one(points, folds)}")

    #print("Part two:")
    #print(f"  {part_two()}")
    