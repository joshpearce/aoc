#!/usr/bin/env python3

from aocd.models import Puzzle

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2022, day=1)

cal_groups = puzzle.input_data.split("\n\n")
elf_cals = [sum(map(int,cals.split())) for cals in cal_groups]

if not puzzle.answered_a:

    ans_a = max(elf_cals)

    print(f"Part A: {ans_a}")
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    sorted_cals = sorted(elf_cals, reverse=True)

    ans_b = sum(sorted_cals[0:3])

    print(f"Part B: {ans_b}")
    puzzle.answer_b = ans_b

