#!/usr/bin/env python3

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from utils import advent
from typing import Iterator, Tuple, List

def mark(draw: int, board: List[List[int]]):
    return [[i if i != draw else 0 for i in row] for row in board]

def bingo(board: List[List[int]]):
    s1 = [sum(l) for l in zip(*board)]
    s2 = [sum(l) for l in zip(*advent.transpose(board))]
    if 0 in s1 or 0 in s2:
        return sum(s1)
    else:
        return 0

def run(draws: List[int], boards: List[List[List[int]]]):
    for draw in draws:
        for i in range(len(boards)):
            boards[i] = mark(draw, boards[i])
            bgo = bingo(boards[i])
            if bgo:
                print(f"bingo {bgo * draw}")
                return

def run2(draws: List[int], boards: List[List[List[int]]]):
    final = 0
    boards = [(b, 0) for b in boards]
    for draw in draws:
        for i in range(len(boards)):
            if not boards[i][1]:
                marked = mark(draw, boards[i][0])
                bgo = bingo(marked)
                boards[i] = (marked, 1 if bgo else 0)
                if bgo:
                    final = bgo * draw
    print(f"last bingo {final}")

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    lines = advent.read_lines_from_file(file_path)
    
    draws = list(map(int,lines[0].split(",")))

    boards = [[list(map(int, l.split())) for l in lines[i:i+5]] for i in range(2, len(lines), 6)]
    
    run(draws, boards)
    run2(draws, boards)




        

