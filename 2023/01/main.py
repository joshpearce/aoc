#!/usr/bin/env python3

from aocd.models import Puzzle

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2023, day=1)

lines = puzzle.input_data.split("\n")

digits = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

if not puzzle.answered_a:
    digit_lines = [ [c for c in l if c.isdigit()] for l in lines]
    cals = [int(l[0]+l[-1]) for l in digit_lines]
    ans_a = sum(cals)

    print(f"Part A: {ans_a}")
    puzzle.answer_a = ans_a

if not puzzle.answered_b:
    ans_b = 0
    for l in lines:
        cal = []
        for i in range(len(l)):
            if l[i].isdigit():
                cal.append(l[i])
            else:
                for j in range(len(digits)):
                    if l[i:i+len(digits[j])] == digits[j]:
                        cal.append(str(j))
                        break
        ans_b += int(cal[0]+cal[-1])

    print(f"Part B: {ans_b}")
    puzzle.answer_b = ans_b

