from pathlib import Path
import sys
from typing import List, Tuple, Dict, Set
import re
from collections import defaultdict
import math

def set_valid_idx(line:str, idxs:List[int], set_val = 0) -> str:
    p1 = line.split(":")
    p2 = p1[1].strip().split(" ")
    r1 = p2[0].split("-")
    r2 = p2[2].split("-")
    r1a, r1b = int(r1[0]), int(r1[1])
    r2a, r2b = int(r2[0]), int(r2[1])
    idxs[r1a:r1b+1] = [set_val] * ((r1b+1) - r1a)
    idxs[r2a:r2b+1] = [set_val] * ((r2b+1) - r2a)
    return p1[0]
    

def part1(lines: List[str]) -> int:
    valid_idxs = [1] * 1000
    errors = 0
    for i in range(len(lines)):
        line = lines[i]
        if i < 20:
            set_valid_idx(line, valid_idxs)
        elif i > 24:
            tix_vals = map(int, line.split(","))
            errors += sum([x if valid_idxs[x] else 0 for x in tix_vals])
    
    return errors

def part2(lines: List[str]) -> int:
    valid_idxs = [1] * 1000
    valid_tix = []
    labels = {}
    my_ticket = None
    errors = 0
    for i in range(len(lines)):
        line = lines[i]
        if i < 20:
            idx_idx = [-1] * 1000
            label = set_valid_idx(line, idx_idx, i)
            labels[label] = list(idx_idx)
            set_valid_idx(line, valid_idxs)
        if i == 22:
            my_ticket = list(map(int, line.split(",")))
        elif i > 24:
            tix_vals = list(map(int, line.split(",")))
            errors = sum([valid_idxs[x] for x in tix_vals])
            if (errors == 0):
                valid_tix.append(tix_vals)
    
    pos = {}
    for i in range(len(valid_tix[0])):
        possible_labels = set()
        for j in valid_tix:
            possible_labels2 = set()
            for k in labels:
                if labels[k][j[i]] > -1:
                    possible_labels2.add(k)
            if not possible_labels:
                possible_labels = possible_labels2
            else:
                possible_labels = possible_labels & possible_labels2

        pos[i] = possible_labels
    
    sorted_pos = sorted(pos.items(), key=lambda item: len(item[1]))

    found = set()
    index = {}
    for pos in sorted_pos:
        labels = set(pos[1]) - found
        found.add(list(labels)[0])
        index[pos[0]] = list(labels)[0]
    
    ans = math.prod([x for i, x in enumerate(my_ticket) if index[i].find('departure') == 0])

    return ans


if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    lines = file_path.read_text().strip().split('\n')

    print(part1(lines))
    print(part2(lines))
