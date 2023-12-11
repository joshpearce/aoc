#!/usr/bin/env python3

from aocd.models import Puzzle
from collections import defaultdict
from operator import mul

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2023, day=3)
AllowSubmitA = True
AllowSubmitB = True
UseExampleData = False
data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data


lines = data.split("\n")

nums_locs = defaultdict(lambda: dict())
symbol_locs = []

for y in range(len(lines)):
    line = lines[y]
    x = 0
    while x < len(line):
        if line[x].isdigit():
            i = x
            while i < len(line) and line[i].isdigit():
                i += 1
            nl = [int(line[x:i]), False]
            for j in range(x, i):
                nums_locs[y][j] = nl
            x = i
        else:
            if line[x] != '.':
                symbol_locs.append((y, x))
            x += 1

def get_adj(y, x):
    for i in (y-1, y, y+1):
        for j in (x-1, x, x+1):
            if y >=0 and x >= 0:
                yield (i, j)


if not puzzle.answered_a:
    
    sum = 0
    for symbol in symbol_locs:
        for adj in get_adj(symbol[0], symbol[1]):
            if adj[0] in nums_locs.keys():
                if adj[1] in nums_locs[adj[0]].keys():
                    if not nums_locs[adj[0]][adj[1]][1]:
                        nums_locs[adj[0]][adj[1]][1] = True
                        sum += nums_locs[adj[0]][adj[1]][0]



    ans_a = sum

    if AllowSubmitA:
        puzzle.answer_a = ans_a
    else:
        print(f'Example A: {"Correct" if str(ans_a) == puzzle.examples[0].answer_a else "Wrong"}')

if not puzzle.answered_b:

    sum = 0
    for symbol in symbol_locs:
        parts = []
        for adj in get_adj(symbol[0], symbol[1]):
            if adj[0] in nums_locs.keys() and adj[1] in nums_locs[adj[0]].keys():
                if nums_locs[adj[0]][adj[1]] not in parts:
                    parts.append(nums_locs[adj[0]][adj[1]])
                    if len(parts) == 2:
                        sum += parts[0][0] * parts[1][0]
                        break

    
    ans_b = sum

    if AllowSubmitB:
        puzzle.answer_b = ans_b
    else:
        print(f'Example B: {"Correct" if str(ans_b) == puzzle.examples[0].answer_b else "Wrong"}')

