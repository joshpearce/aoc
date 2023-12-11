#!/usr/bin/env python3

from aocd.models import Puzzle
from collections import defaultdict

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2023, day=2)

lines = puzzle.input_data.split("\n")
games = [None] * (len(lines) + 1)

for line in lines:
    id, grabs = line.split(':')
    cubes = defaultdict(list)
    for grab in grabs.split(';'):
        for group in grab.split(','):
            num, color = group.split()
            cubes[color].append(int(num))
        games[int(id.split()[1])] = cubes

if not puzzle.answered_a:
    
    total = 0
    for i in range(1, len(games)):
        if max(games[i]['red']) <= 12 and max(games[i]['green']) <= 13 and max(games[i]['blue']) <= 14:
            total += i

    ans_a = total

    print(f"Part A: {ans_a}")
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    total = 0
    for i in range(1, len(games)):
        total += max(games[i]['red']) * max(games[i]['green']) * max(games[i]['blue'])

    ans_b = total

    print(f"Part B: {ans_b}")
    puzzle.answer_b = ans_b

