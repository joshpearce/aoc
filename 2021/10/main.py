#!/usr/bin/env python3

from os import error

pairs = {"(" : ")", "[" : "]", "{" : "}", "<" : ">"}
points = {")" : 3, "]" : 57, "}" : 1197, ">" : 25137}
incomplete_lines = []

def part_one(lines):
    
    score = 0
    for line in lines:
        s = []
        corrupted = True
        for t in line:
            if t in pairs.keys():
                s.append(t)
            elif pairs[s.pop()] != t:
                score += points[t]
                corrupted = False
                break
        if corrupted:
            incomplete_lines.append(line)
    return score

def part_two():
    from functools import reduce
    points = {")" : 1, "]" : 2, "}" : 3, ">" : 4}
    scores = []
    for line in incomplete_lines:
        score = 0
        s = []
        for t in line:
            if t in pairs.keys():
                s.append(t)
            else:
                o = s.pop()
        scores.append(reduce(lambda a, b : a * 5 + b, [0] + [points[pairs[i]] for i in s[::-1]]))
        scores.sort()
    return scores[int(len(scores) / 2)]


if __name__ == '__main__':
    from pathlib import Path

    #f = 'test.txt'
    f = 'input.txt'
    lines = (Path(__file__).parent / f).open().read().split('\n')
    print("Part one:")
    print(f"  {part_one(lines)}")
    print("Part two:")
    print(f"  {part_two()}")
    