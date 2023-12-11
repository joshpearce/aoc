#!/usr/bin/env python3

from aocd.models import Puzzle
import re

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2022, day=5)

lines = puzzle.input_data.split('\n')

idxs = list(range(1, len(lines[0]), 4))
stacks = [[] for _ in idxs]

i = 0
for line in lines:
    i += 1
    if '[' not in line:
        break
    for j, idx in enumerate(idxs):
        if line[idx].strip():
            stacks[j].extend(line[idx])

dig_re = re.compile('[0-9]+')
moves = [list(map(int, dig_re.findall(line))) for line in lines[i+1:]]

if not puzzle.answered_a:

    for move in moves:
        stacks[move[2]-1] = list(reversed(stacks[move[1]-1][0:move[0]])) + stacks[move[2]-1]
        stacks[move[1]-1] = stacks[move[1]-1][move[0]:]

    ans_a = ''.join([stack[0] for stack in stacks])

    print(ans_a)
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    for move in moves:
        stacks[move[2]-1] = stacks[move[1]-1][0:move[0]] + stacks[move[2]-1]
        stacks[move[1]-1] = stacks[move[1]-1][move[0]:]

    ans_b = ''.join([stack[0] for stack in stacks])

    print(ans_b)
    puzzle.answer_b = ans_b

