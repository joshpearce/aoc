#!/usr/bin/env python3

import itertools
import numpy
from collections import namedtuple

from numpy.lib.function_base import iterable

Perm = namedtuple('Perm', ['c', 's'])

coord_perms = itertools.permutations([0, 1, 2])
#sign_perms = [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]
sign_perms = [(i, j, k) for i in [1, -1] for j in [1, -1] for k in [1, -1]]
perms = [Perm(c, s) for c in coord_perms for s in sign_perms]

def project(i, b, reverse=False):
    p = perms[i]
    if reverse:
        b_ = numpy.multiply(b, p.s)
        b__ = tuple(b_[i] for i in p.c)
        return b__
    else:
        b_ = tuple(b[i] for i in p.c)
        b__ = tuple(numpy.multiply(b_, p.s))
        return b__

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    f = "input.txt"

    input = [[]]
    scanner = input[0]
    for line in (Path(__file__).parent / f).open().readlines():
        if line[0] == "\n":
            scanner = []
            input.append(scanner)
        elif line[0:2] != "--":
            scanner.append(tuple(*[map(int, line.split(","))]))

    input_plus = [
            (
                beacons, 
                list(list( map(lambda b: project(i, b), beacons)) for i in range(len(perms)))
            )
        for beacons in input]

    offset_mappings = {}
    offset_perm_mappings = {}

    for o_idx, o_scanner in enumerate(input_plus):
        o_beacons = o_scanner[0]
        o_beacons_set = set(o_beacons)
        print(f"outer index {o_idx}")
        for i_idx, i_scanner in enumerate(input_plus):
            if o_idx == i_idx or i_idx == 0:
                continue
            print(f"  inner index {i_idx}")
            for j_idx, i_beacons_perm in enumerate(i_scanner[1]):
                pairs = list(itertools.product(i_beacons_perm, o_beacons))
                for pair in pairs:
                    offset = numpy.subtract(pair[1], pair[0])
                    projected_i_beacons = set(list(map(lambda ib: tuple(numpy.add(ib, offset)), i_beacons_perm)))
                    projected_i_beacons_set = set(projected_i_beacons)
                    int_count = len(projected_i_beacons_set & o_beacons_set)
                    if int_count >= 12:
                        #if (i_idx, o_idx) not in offset_mappings and (o_idx, i_idx) not in offset_mappings:
                            offset_mappings[(i_idx, o_idx)] = offset
                            offset_perm_mappings[(i_idx, o_idx)] = j_idx
                            print(f"    {i_idx} is offset from {o_idx} by {offset}, with count {int_count}")
                            break
    
    
    distance_from_zero = {0:0}
    have_distance = []
    added = True
    while added:
        added = False
        for ft, off in offset_mappings.items():
            if ft not in have_distance:
                f, t = ft
                if t in distance_from_zero:
                    if f in distance_from_zero:
                        if distance_from_zero[t] >= distance_from_zero[f]:
                            continue
                    distance_from_zero[f] = distance_from_zero[t] + 1
                    have_distance.append(ft)
                    added = True
    
    destinations = {}
    for f, t in have_distance:
        destinations[f] = t

    processed = True
    while processed:
        processed = False
        for idx, beacons in enumerate(input):
            if len(beacons):
                if idx in destinations:
                    processed = True
                    key = (idx, destinations[idx])
                    offset = offset_mappings[key]
                    perm_idx = offset_perm_mappings[key]
                    p = list(map(lambda b: tuple(numpy.add(offset, project(perm_idx, b))), input[idx]))
                    input[idx] = []
                    input[destinations[idx]] += p
    
    print(len(set(input[0])))

    new_input = [[(0,0,0)] for _ in range(len(input))] 
    
    processed = True
    while processed:
        processed = False
        for idx, beacons in enumerate(new_input):
            if len(beacons):
                if idx in destinations:
                    processed = True
                    key = (idx, destinations[idx])
                    offset = offset_mappings[key]
                    perm_idx = offset_perm_mappings[key]
                    p = list(map(lambda b: tuple(numpy.add(offset, project(perm_idx, b))), new_input[idx]))
                    new_input[idx] = []
                    new_input[destinations[idx]] += p

    def manhattan(a, b):
        x0, y0, z0 = a
        x1, y1, z1 = b
        return abs(x1 - x0) + abs(y1 - y0) + abs(z1 - z0)

    print(max(manhattan(a, b) for a in new_input[0] for b in new_input[0]))
    pass


