#!/usr/bin/env python3

import numpy as np

def move_east(floor):
    move = np.array([
        [ 1 if floor[row, col] == 0 and floor[row, (col-1) % floor.shape[1]] == 1 
            else 0 if floor[row, (col+1) % floor.shape[1]] == 0 and floor[row, col] == 1 
            else floor[row, col]
        for col in range(floor.shape[1])] 
        for row in range(floor.shape[0])])
    return move

def move_south(floor):
    move = np.array([
        [ 2 if floor[row, col] == 0 and floor[(row-1) % floor.shape[0], col] == 2 
            else 0 if floor[(row+1) % floor.shape[0], col] == 0 and floor[row, col] == 2 
            else floor[row, col]
        for col in range(floor.shape[1])] 
        for row in range(floor.shape[0])])
    return move

def step(floor):
    east = move_east(floor)
    south = move_south(east)
    return south
    
def step_till_stopped(floor):
    s, steps = 1, 0
    f = floor
    while s:
        _f = step(f)
        s = np.sum(f ^ _f)
        steps += 1
        f = _f
    return steps

if __name__ == "__main__":

    from pathlib import Path

    test_lines = (Path(__file__).parent / "test.txt").open().read().split("\n")
    input_lines = (Path(__file__).parent / "input.txt").open().read().split("\n")

    lookup = ['.', '>', 'v']
    test_floor = np.array([[lookup.index(c) for c in l] for l in test_lines])
    real_floor = np.array([[lookup.index(c) for c in l] for l in input_lines])

    print(step_till_stopped(test_floor))
    print(step_till_stopped(real_floor))
    pass