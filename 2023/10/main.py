#!/usr/bin/env python3
from aocd.models import Puzzle
import numpy as np
from collections import defaultdict

def expand_field(lines):
    top_bottom = [['.' for _ in range(len(lines[0])+2)]]
    return top_bottom + [
        ['.'] + list(line) + ['.'] for line in lines
        ] + top_bottom
    
def map_tile(x, y, tile):
    match tile:
        case '|':
            return (x-1, y), (x+1, y)
        case '-':
            return (x, y-1), (x, y+1)
        case 'L':
            return (x-1, y), (x, y+1)
        case 'J':
            return (x-1, y), (x, y-1)
        case '7':
            return (x, y-1), (x+1, y)
        case 'F': 
            return (x, y+1), (x+1, y)
        case 'S':
            return (x-1, y), (x+1, y), (x, y-1), (x, y+1)
        case _:
            return ()
        
def part_a(lines):

    field = expand_field(lines)
    
    x, y = next ((x, y) for (x, y), tile in np.ndenumerate(field) if tile == 'S')
    path = [(x, y)]

    while next_tile := next((
            (x_, y_)
            for x_, y_ in map_tile(x, y, field[x][y]) 
            for m in map_tile(x_, y_, field[x_][y_])
            if (x, y) == m
        ), None):
        field[x][y] = 'X'
        path.append(next_tile)
        x, y = path[-1]

    field[x][y] = 'X'
    return path, field



def part_b(path, field):
    # Trapezoid formula, https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula
    area = abs(
        sum(
            (y + path[(i+1)%len(path)][1])*(x - path[(i+1)%len(path)][0])
            for i, (x, y) in enumerate(path)
        )
    ) // 2

    # Pick's theorem, https://en.wikipedia.org/wiki/Pick%27s_theorem
    return area - len(path)//2 + 1


puzzle = Puzzle(year=2023, day=10)
UseExampleData = False
data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data

lines = data.split('\n')

path, field = part_a(lines)
if not puzzle.answered_a:
    puzzle.answer_a = len(path) // 2

#for el in field:
#    print(''.join(el))

if not puzzle.answered_b:
    ans_b = part_b(path, field)
    print(ans_b)
    puzzle.answer_b = ans_b
