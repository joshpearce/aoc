#!/usr/bin/env python3

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pathlib import Path
from utils import advent
from math import gcd
from collections import defaultdict
from itertools import chain

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def equals(self, point):
        return self.x == point.x and self.y == point.y

    def increment(self, dx, dy):
        return Point(self.x + dx, self.y + dy)
    
    def key(self):
        # return f"{self.x},{self.y}" # slower
        # return self.x << 12 + self.y # slowest
        return self.x * 1000 + self.y # fastest

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.dx = end.x - start.x
        self.dy = end.y - start.y
        _gcd = gcd(self.dx, self.dy)
        self.dx = int(self.dx / _gcd)
        self.dy = int(self.dy / _gcd)

class Ocean:
    def __init__(self):
        self.vents = defaultdict(int)

    def add_lines(self, lines):
        for line in lines:
            self.vents[line.start.key()] += 1
            self.vents[line.end.key()] += 1
            new_pt = line.start.increment(line.dx, line.dy)
            for _ in range(1, max(abs(line.end.x - line.start.x), abs(line.end.y - line.start.y))):
            # while not line.end.equals(new_pt): # little slower
                self.vents[new_pt.key()] += 1
                new_pt = new_pt.increment(line.dx, line.dy)

    def overlapping_points(self, minimum):
        return len(list(filter(lambda c: c >= minimum, self.vents.values())))

if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    file_lines = advent.read_lines_from_file(file_path)
    
    lines = [
        Line(
            Point(x=x1, y=y1),
            Point(x=x2, y=y2)
        ) 
        for x1, y1, x2, y2 in 
        [map(int, l) for l in
        [','.join(l.split('->')).split(',') for l in file_lines]]
    ]

    # part 1
    ocean = Ocean()
    ocean.add_lines(filter(lambda l: l.dx == 0 or l.dy == 0, lines))
    print(f"part 1: {ocean.overlapping_points(2)}")

    # part 2
    ocean = Ocean()
    ocean.add_lines(lines)
    print(f"part 2: {ocean.overlapping_points(2)}")
    
