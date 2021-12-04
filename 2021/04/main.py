#!/usr/bin/env python3

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from utils import advent
from typing import Iterator, Tuple, List

def get_bingo(draw: int, board: List[List[Tuple[int, bool]]]) -> int:
    rows = [True] * 5
    cols = [True] * 5
    sum = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if draw == board[r][c][0]:
                board[r][c] = (board[r][c][0], True)
            if not board[r][c][1]:
                sum += board[r][c][0]
            cols[c] = board[r][c][1] and cols[c]
            rows[r] = board[r][c][1] and rows[r]
    
    if True in rows or True in cols:
        return sum * draw
    else:
        return 0

def run(draws: List[int], boards: List[List[List[Tuple[int, bool]]]]):
    for draw in draws:
        for board in boards:
            result = get_bingo(draw, board)
            if result:
                print(result)
                return

def run2(draws: List[int], boards: List[List[List[Tuple[int, bool]]]]):
    for draw in draws:
        for board in boards:
            result = get_bingo(draw, board)
            if result:
                print(result)
                boards = list(filter(lambda b: id(b) != id(board), boards))

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    lines = advent.read_lines_from_file(file_path)
    
    draws = list(map(int,lines[0].split(",")))

    boards = []
    i = 2
    while i < len(lines):
        boards.append([list(map(lambda n: (int(n), False), l.split())) for l in lines[i:i+5]])
        i += 6
    
    run(draws, boards)
    run2(draws, boards)




        

