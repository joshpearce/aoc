#!/usr/bin/env python3

from aocd.models import Puzzle

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2022, day=6)

lines = puzzle.input_data.split('\n')

if not puzzle.answered_a:

    ans_a = "ha"

    print(ans_a)
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    ans_b = ""

    print(ans_b)
    #puzzle.answer_b = ans_b

