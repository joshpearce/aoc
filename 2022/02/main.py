#!/usr/bin/env python3

from aocd.models import Puzzle

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2022, day=2)

lookup =  {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}
winners = [
    [3, 0, 6],
    [6, 3, 0],
    [0, 6, 3]
]

lines = puzzle.input_data.split('\n')
rounds = list(map(str.split, lines))


if not puzzle.answered_a:

    scores = [winners[lookup[r[1]]][lookup[r[0]]] + lookup[r[1]] + 1 for r in rounds]
    ans_a = sum(scores)

    print(ans_a)
    puzzle.answer_a = ans_a

if not puzzle.answered_b:

    winning_points = [2, 3, 1]
    losing_points = [3, 1, 2]

    def get_score(p, d):
        match d:
            case 'X':
                return losing_points[lookup[p]]
            case 'Y':
                return lookup[p] + 1 + 3
            case 'Z':
                return winning_points[lookup[p]] + 6
    
    scores = [get_score(r[0], r[1]) for r in rounds]

    ans_b = sum(scores)

    print(ans_b)
    puzzle.answer_b = ans_b

