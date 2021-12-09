#!/usr/bin/env python3

from os import error
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from utils import advent
import numpy as np
from math import prod

def get_neighbors(i, j, arr):
    neighbors_idxs = []
    if i > 0: 
        neighbors_idxs.append((i-1, j))
    if i < arr.shape[0] - 1:
        neighbors_idxs.append((i+1, j))
    if j > 0:
        neighbors_idxs.append((i, j-1))
    if j < arr.shape[1] - 1:
        neighbors_idxs.append((i, j+1))
    return neighbors_idxs

def mark_basin(pt, arr):
    basin_size = 0
    if arr[pt] == 9:
        return basin_size
    neighbors_idxs = get_neighbors(pt[0], pt[1], a)
    neighbors_idxs_t = np.array(neighbors_idxs).T.tolist() # transpose to [[i1, i2, ...], [j1, j2, ...]]
    neighbors_vals = a[tuple(neighbors_idxs_t)]

    if neighbors_vals.min() >= a[pt]:
        neighbors_idxs = list(filter(lambda n: arr[n] != 9, neighbors_idxs))
        basin_size = 1 
        a[pt] = 9
        basin_size += sum([mark_basin(pt, a) for pt in neighbors_idxs])
    return basin_size

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    file_lines = advent.read_lines_from_file(file_path)
    
    a = np.array([[*l] for l in file_lines], np.int32)

    # part 1
    total = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            v = np.concatenate((a[i, max(0, j-1): min(j+2, a.shape[1])], 
            a[max(0, i-1): min(i+2, a.shape[0]), j]))
            if v.min() == a[i, j] and np.sum(v == a[i, j]) == 2:
                total += a[i, j] +1
    
    print(total)

    # part 2
    basin_sizes = []
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            basin_size = mark_basin((i, j), a)
            if basin_size:
                basin_sizes.append(basin_size)
    
    print( prod(sorted(basin_sizes)[-3:] ))
