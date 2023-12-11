#!/usr/bin/env python3

from aocd.models import Puzzle
import operator
from functools import reduce

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2023, day=6)
AllowSubmitA = True
AllowSubmitB = True
UseExampleData = False

data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data

def part_a(lines):

    return reduce(operator.mul,
        (sum([h*(time-h) > distance for h in range(time+1)])
        for time, distance in zip(*
            ((int(x) for x in l.split(':')[1].split())
            for l in lines
        )))
    )

def part_b(lines):

    return part_a(l.replace(' ', '') for l in lines)

if not puzzle.answered_a:
    
    ans_a = part_a(data.split('\n'))

    if AllowSubmitA:
        puzzle.answer_a = ans_a
    else:
        print(f'Example A: {"Correct" if str(ans_a) == puzzle.examples[0].answer_a else "Wrong"}')

if not puzzle.answered_b:

    ans_b = part_b(data.split('\n'))

    if AllowSubmitB:
        puzzle.answer_b = ans_b
    else:
        print(f'Example B: {"Correct" if str(ans_b) == puzzle.examples[0].answer_b else "Wrong"}')


# From Karen Lyons, quadratic
# def solve_one(lines):
# 	return reduce(
# 		operator.mul,
# 		(
# 			(
# 				1
# 				+ floor((time + ((time**2 - 4 * (distance + 1)) ** 0.5)) / 2)
# 				- ceil((time - ((time**2 - 4 * (distance + 1)) ** 0.5)) / 2)
# 			)
# 			for time, distance in zip(*(
# 				(int(s) for s in l.split(':', 1)[1].split())
# 				for l in lines
# 			))
# 		)
# 	)