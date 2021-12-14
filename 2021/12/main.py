#!/usr/bin/env python3

from os import error
from collections import defaultdict

graph = defaultdict(set)
    

def part_one(lines):
    cons = [l.split("-") for l in lines]
    for c in cons + [x[::-1] for x in cons]:
        if c[1] != "start" and c[0] != "end":
            graph[c[0]].add(c[1])

    for k in graph.keys():
        print(f"{k}: {graph[k]}")

    v2x = filter(lambda k: k.islower(), graph.keys())

    paths = []

    for v2 in v2x:
    
        q = []

        p = ["start"]
        q += graph["start"]
        while len(q):
            nx = q.pop()
            if nx == "#":
                p.pop()
                continue
            if nx.isupper() or nx not in p or (sum([j == v2 for j in p]) == 1 and nx == v2):
                p.append(nx)
                if nx == "end":
                    paths.append(",".join(p))
                    p.pop()
                else:
                    q.append("#")
                    q += list(graph[nx])
    
    paths = list(set(paths))
    for path in sorted(paths):
        print(path)
    print(len(paths))
            
def part_two():
    
    pass


if __name__ == '__main__':
    from pathlib import Path

    #f = 'test.txt'
    f = 'input.txt'
    lines = (Path(__file__).parent / f).open().read().split('\n')
    print("Part one:")
    print(f"  {part_one(lines)}")

    #print("Part two:")
    #print(f"  {part_two()}")
    