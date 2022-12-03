#!/usr/bin/env python3

from aocd.models import Puzzle

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2022, day=3)

lines = puzzle.input_data.split()

pri = { chr(96+i):i for i in range(1,27) }
pri.update( { chr(38+i):i for i in range(27, 27+26) } )

if not puzzle.answered_a:

    rucksacks = [(l[0:len(l)//2], l[len(l)//2:]) for l in lines]
    common = [set(r[0]) & set(r[1]) for r in rucksacks]
    
    ans_a = sum([pri[c.pop()] for c in common])

    print(ans_a)
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    groups = [lines[i:i+3] for i in range(0, len(lines), 3)]
    common = [set(g[0]) & set(g[1]) & set(g[2]) for g in groups]

    ans_b = sum([pri[c.pop()] for c in common])

    print(ans_b)
    puzzle.answer_b = ans_b

