#!/usr/bin/env python3
from aocd.models import Puzzle
import re
from itertools import count
import math

MAP = re.compile(r'^([1-9A-Z]{3}) = \(([1-9A-Z]{3}), ([1-9A-Z]{3})\)')

def part_a(map, turns):

    node = 'AAA'
    
    for i in count():
        node = map[node][turns[i%len(turns)]]
        if node == 'ZZZ':
            return i+1

def part_b(map, turns):

    nodes = [n for n in map.keys() if n[2] == 'A']

    cycles = [0] * len(nodes)
    for j in range(len(nodes)):
        for i in count():
            nodes[j] = map[nodes[j]][turns[i%len(turns)]]
            if nodes[j][2] == 'Z':
                cycles[j] = i+1
                break
    return math.lcm(*cycles)
        


puzzle = Puzzle(year=2023, day=8)
UseExampleData = False
data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data

lines = data.split('\n')

map = {
        s: (r, l)
        for s, r, l in 
        (MAP.match(l).groups() for l in lines[2:])
    }

turns = [1 if t == 'R' else 0 for t in lines[0]]

if not puzzle.answered_a:
    ans_a = part_a(map, turns)
    puzzle.answer_a = ans_a


if not puzzle.answered_b:
    ans_b = part_b(map, turns)
    print(ans_b)
    puzzle.answer_b = ans_b
