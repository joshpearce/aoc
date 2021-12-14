#!/usr/bin/env python3
from collections import defaultdict, Counter
from more_itertools import windowed as win


def part_one(template, rules, steps):

    for i in range(steps):
        template = "".join([pair[0] + rules["".join(pair)] for pair in win(template, 2, step=1)]) + template[-1]
        counts = Counter(template)
        print(f"round: {i}, len: {len(template)}")

    return counts.most_common(100)[0][1] - counts.most_common(100)[-1][1]
            
def part_two(template, rules, steps):
    d = defaultdict(int)

    for p in win(template, 2, step=1):
        d["".join(p)] += 1
    
    for s in range(steps):
        dc = defaultdict(int)
        for p in d.keys():
            dc[p[0] + rules[p]] += d[p]
            dc[rules[p] + p[1]] += d[p]
        d = dc.copy()
        print(sum(v for k, v in dc.items()))
    
    counts = Counter()
    for k, v in d.items():
        counts[k[0]] += v
        counts[k[1]] += v
    counts["P"] += 1
    return counts.most_common(100)[0][1]/2 - counts.most_common(100)[-1][1]/2
    

if __name__ == "__main__":
    from pathlib import Path

    #f = "test.txt"
    f = "input.txt"
    lines = (Path(__file__).parent / f).open().read().split("\n")
    
    template = lines[0]
    rules = defaultdict(str, [(m[0], m[1]) for m in [l.split(" -> ") for l in lines[2:]]])
    
    
    print("Part one:")
    print(f"  {part_one(template, rules, 10)}")

    print("Part two:")
    print(f"  {part_two(template, rules, 40)}")
    