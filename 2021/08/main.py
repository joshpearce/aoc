#!/usr/bin/env python3

from os import error
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from utils import advent
from collections import Counter
from itertools import chain

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    file_lines = advent.read_lines_from_file(file_path)
    
    # part 1
    input = [line.split("|") for line in file_lines]
    entries = [[tuple(p[0].split()), tuple(p[1].split())] for p in input]
    counter = Counter([len(w) for w in chain(*[e[1] for e in entries])])
    ans = sum(counter[i] for i in (2, 3, 4, 7))
    print(ans)

    # part 2
    lookup = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9
    }

    def makeMapping(one, seven, four, eight, others): # lengths: 2, 3, 4, 7
        c = {}

        c[(set(seven) - set(one)).pop()] = "a"
        
        e_or_g = list(set(eight) - set(four) - set(seven))
        if all([e_or_g[0] in o for o in others]):
            c[e_or_g[0]] = "g"
            c[e_or_g[1]] = "e"
        else:
            c[e_or_g[0]] = "e"
            c[e_or_g[1]] = "g"

        # have: a, (b), (c), (d), e, (f), g
        
        c_or_f = one
        if [c_or_f[0] in o for o in others].count(True) == 5:
            c[c_or_f[0]] = "f"
            c[c_or_f[1]] = "c"
        else:
            c[c_or_f[0]] = "c"
            c[c_or_f[1]] = "f"
        
        # have: a, (b), c, (d), e, f, g
        b_or_d = list(set(four) - set(one))
        if [b_or_d[0] in o for o in others].count(True) == 5:
            c[b_or_d[0]] = "d"
            c[b_or_d[1]] = "b"
        else:
            c[b_or_d[0]] = "b"
            c[b_or_d[1]] = "d"
        
        return c

    values = []

    for entry in entries:
        one, seven, four, eight = None, None, None, None # lengths: 2, 3, 4, 7
        for word in entry[0]:
            if len(word) == 2:
                one = word
            elif len(word) == 3:
                seven = word
            elif len(word) == 4:
                four = word
            elif len(word) == 7:
                eight = word
        
        if None in (one, seven, four, eight):
            raise error("don't have all four args")
        
        others = set(entry[0]) - set([one, seven, four, eight])

        mapping = makeMapping(one, seven, four, eight, others)
        
        v = 0
        for val in entry[1]:
            fixed_val = "".join(sorted([mapping[c] for c in val]))
            v = v*10 + lookup[fixed_val]
        values.append(v)
    
    print(sum(values))
    