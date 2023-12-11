#!/usr/bin/env python3

from aocd.models import Puzzle

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2022, day=4)

lines = puzzle.input_data.split()

def range_inclusive(start, end):
     return range(start, end+1)

assignments = [ 
    [set(range_inclusive(*map(int, r.split('-'))))
    for r in l.split(',')
    ]
for l in lines ]

if not puzzle.answered_a:

    fully_contained = [ p[0] >= p[1] or p[0] <= p[1] for p in assignments]

    ans_a = fully_contained.count(True)

    print(ans_a)
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    any_overlap = [ any(p[0] & p[1]) for p in assignments]

    ans_b = any_overlap.count(True)

    print(ans_b)
    puzzle.answer_b = ans_b

