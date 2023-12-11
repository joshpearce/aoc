#!/usr/bin/env python3

from aocd.models import Puzzle
from collections import defaultdict
from operator import mul

# Reading session cookie value from: ~/.config/aocd/token
puzzle = Puzzle(year=2023, day=4)
AllowSubmitA = True
AllowSubmitB = True
UseExampleData = False

data = puzzle.examples[0].input_data if UseExampleData else puzzle.input_data



if not puzzle.answered_a:
    total = 0

    for line in data.split('\n'):
        winners, mine = (set(x.split()) for x  in line.split(':')[1].split('|'))
        wins = winners & mine
        if wins:
            total += 2**(len(wins)-1)

    ans_a = total

    if AllowSubmitA:
        puzzle.answer_a = ans_a
    else:
        print(f'Example A: {"Correct" if str(ans_a) == puzzle.examples[0].answer_a else "Wrong"}')

if not puzzle.answered_b:
    cards = defaultdict(lambda: 1)
    lines = data.split('\n')
    total = len(lines)

    i = 0
    for line in lines:
        while cards[i]:
            winners, mine = (set(x.split()) for x  in line.split(':')[1].split('|'))
            wins = len(winners & mine)
            for j in range(wins):
                cards[i+1+j] += 1
                total += 1
            pass
            cards[i] -= 1
        i += 1

    ans_b = total

    if AllowSubmitB:
        puzzle.answer_b = ans_b
    else:
        print(f'Example B: {"Correct" if str(ans_b) == puzzle.examples[0].answer_b else "Wrong"}')

