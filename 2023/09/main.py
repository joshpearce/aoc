#!/usr/bin/env python3
from aocd.models import Puzzle

def process_seq(seq, left=False):
    subs = [seq]
    while any(s != 0 for s in subs[-1]):
        subs.append([subs[-1][i+1] - subs[-1][i] for i in range(len(subs[-1])-1)])
    
    temp = subs[-2][0]
    for sub in subs[::-1][2:]:
        temp = sub[0 if left else -1] + -temp if left else temp 
    return temp
    

def part_a(lines):
    return sum(process_seq([int(n) for n in l.split()]) for l in lines)
    
def part_b(lines):
    return sum(process_seq([int(n) for n in l.split()], True) for l in lines)


puzzle = Puzzle(year=2023, day=9)
UseExampleData = False
data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data

lines = data.split('\n')


if not puzzle.answered_a:
    ans_a = part_a(lines)
    print(ans_a)
    puzzle.answer_a = ans_a


if not puzzle.answered_b:
    ans_b = part_b(lines)
    print(ans_b)
    puzzle.answer_b = ans_b
