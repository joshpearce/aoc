#!/usr/bin/env python3

from collections import Counter;
from math import floor, ceil
import itertools

class Node:
    def __init__(self, v):
        if type(v) == int:
            self.val = v
            self.left = None
            self.right = None
        else:
            self.left = Node(v[0])
            self.right = Node(v[1])
            self.val = None
    
def magnitude(n):
    if type(n.val) == int:
        return n.val
    else:
        return 3 * magnitude(n.left) + 2 * magnitude(n.right)

def node_to_list(n):
    if type(n.val) == int:
        return n.val
    else:
        return [node_to_list(n.left), node_to_list(n.right)]

def explode(n):
    status = {"r": None, "l": None, "exploded": False}
    def descend(x, d, status):
        if d == 4 and type(x.val) != int:
            status["l"] = x.left.val
            status["r"] = x.right.val
            x.left = None
            x.right = None
            x.val = 99
            status["exploded"] = True
            return True
        else:
            if x.left:
                if descend(x.left, d+1, status):
                    return True
            if x.right:
                if descend(x.right, d+1, status):
                    return True
    
    descend(n, 0, status)
    s = str(node_to_list(n))
    i99 = -1
    try:
        i99 = s.index("99")
    except:
        pass
    if i99 > -1:
        for i in range(i99+2, len(s)):
            j = i + 1
            if s[i].isdigit():
                if s[i:j+1].isdigit():
                    j = j+1
                s = s[0:i] + str(int(s[i:j]) + status["r"]) + s[j:]
                break
        for i in range(i99-1, 0, -1):
            j = i
            if s[i].isdigit():
                if s[i-1:j+1].isdigit():
                    i = i - 1
                s = s[0:i] + str(int(s[i:j+1]) + status["l"]) + s[j+1:]
                break
        s = s.replace("99", "0")
        n = Node(eval(s))

    return n, status["exploded"]

def split(n):
    l = node_to_list(n)
    s = str(l)
    p = 0
    split = False
    while not split and p < len(s) - 2:
        c = s[p:p+2]
        if c.isdigit():
            c = int(c)
            ca = floor(c/2)
            cb = ceil(c/2)
            s = s[0:p] + f"[{ca},{cb}]" + s[p+2:]
            split = True
        p += 1
    l = eval(s)
    n = Node(l)
    return n, split

def reduce (n, debug=False):
    keep_going = True
    while keep_going:
        n, keep_going = explode(n)
        if not keep_going:
            n, keep_going = split(n)
    return n

def part_one(sfns):

    total = sfns[0]
    for n in sfns[1:]:
        total = Node([node_to_list(total), node_to_list(n)])
        total = reduce(total)

    return magnitude(total)

def part_two(sfns):
    max_mag = 0
    combos = itertools.product(sfns, sfns)
    for i, j in combos:
        max_mag = max(max_mag, magnitude(reduce(Node([node_to_list(i), node_to_list(j)]))))

    return max_mag

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    f = "input.txt"
    lines = (Path(__file__).parent / f).open().read().split("\n")
    sfns = [Node(eval(line)) for line in lines]

    print("\nPart one:")
    print(f"{part_one(sfns)}")

    print("Part two:")
    print(f"{part_two(sfns)}")
    