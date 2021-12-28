#!/usr/bin/env python3

from collections import namedtuple
import re
from dataclasses import dataclass


@dataclass
class Cuboid:
    def __init__(self, on=None, x1=None, x2=None, y1=None, y2=None, z1=None, z2=None):
        self.on = on
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
    
    def area(self):
        dx = (self.x2 - self.x1 + 1)
        dy = (self.y2 - self.y1 + 1)
        dz = (self.z2 - self.z1 + 1)
        if dx < 0 or dy < 0 or dz < 0:
            return 0
        else:
            return dx * dy * dz
    
    def to_tuple(self):
        return (self.on, self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)

def intersect(c1, c2):
    result = Cuboid(True, max(c1.x1, c2.x1), min(c1.x2, c2.x2), max(c1.y1, c2.y1), min(c1.y2, c2.y2), max(c1.z1, c2.z1), min(c1.z2, c2.z2))
    return result

def split_remaining(c, intersection):
    ix = intersection

    # Try to extrude the full rectangle inward from the face of the lower x axis
    box1 = Cuboid(c.on)
    box1.x1 = c.x1
    box1.x2 = ix.x1-1
    box1.y1, box1.y2, box1.z1, box1.z2 = c.y1, c.y2, c.z1, c.z2

    # Try to extrude the full rectangle inward from the face of the upper x axis
    box2 = Cuboid(c.on)
    box2.x1 = ix.x2+1
    box2.x2 = c.x2
    box2.y1, box2.y2, box2.z1, box2.z2 = c.y1, c.y2, c.z1, c.z2

    # Try to extrude the full rectangle inward from the face of the lower y axis,
    # constrained on the x axis by prior takings
    box3 = Cuboid(c.on)
    box3.y1 = c.y1
    box3.y2 = ix.y1-1
    box3.x1, box3.x2, box3.z1, box3.z2 = box1.x2+1, box2.x1-1, c.z1, c.z2

    # Try to extrude the full rectangle inward from the face of the upper y axis,
    # constrained on the x axis by prior takings
    box4 = Cuboid(c.on)
    box4.y1 = ix.y2+1
    box4.y2 = c.y2
    box4.x1, box4.x2, box4.z1, box4.z2 = box1.x2+1, box2.x1-1, c.z1, c.z2

    # Try to extrude the full rectangle inward from the face of the lower z axis,
    # constrained on the x and y axes by prior takings
    box5 = Cuboid(c.on)
    box5.z1 = c.z1
    box5.z2 = ix.z1-1
    box5.x1, box5.x2, box5.y1, box5.y2 = box1.x2+1, box2.x1-1, box3.y2+1, box4.y1-1

    # Try to extrude the full rectangle inward from the face of the upper z axis,
    # constrained on the x and y axes by prior takings
    box6 = Cuboid(c.on)
    box6.z1 = ix.z2+1
    box6.z2 = c.z2
    box6.x1, box6.x2, box6.y1, box6.y2 = box1.x2+1, box2.x1-1, box3.y2+1, box4.y1-1

    cuboids =  (box1, box2, box3, box4, box5, box6)
    # Discard any cuboids with negative volume
    remaining_cuboids_w_volume = [r for r in cuboids if r.area() > 0]
    return remaining_cuboids_w_volume


def solve(lines):

    steps = [Cuboid(bool(re.findall('^([onf]{2,3})', l)[0] == "on"), *map(int, re.findall('([-0-9]+)', l))) for l in lines]
    cuboids = [steps[0]]

    for step in steps[1:]:

        new_cuboids = []
        if step.on:
            # add in the new cuboid
            new_cuboids.append(step)
        # for all existing cuboids, find the portions that do not intersect the newly added
        # cuboid, and add those portions back in
        for cuboid in cuboids:
            intersection = intersect(cuboid, step)
            if intersection.area() > 0:
                remaining_rects = split_remaining(cuboid, intersection)
                new_cuboids += remaining_rects
            else:
                # if there was no intersection, add whole cuboid back in
                new_cuboids.append(cuboid)
        
        # Needed to debug a couple errors in the split_remaining method, so looking
        # for any intersections between cubiods in the reactor. There should be none.
        
        #print(f"Length of new cuboids: {len(new_cuboids)}")
        #p = list(itertools.combinations(new_cuboids, 2))
        #ints = [intersect(a, b) for (a, b) in p ]
        #print(f"Sum of all intersection areas: {sum([ ix.area() for ix in ints if ix.area() > 0 ])}")
        cuboids = new_cuboids
    
    return sum([c.area() for c in cuboids])


if __name__ == "__main__":
    from pathlib import Path

    lines = (Path(__file__).parent / "test_1.txt").open().read().split("\n")
    print("\nPart one test:")
    print(f"{solve(lines[:20])}")

    lines = (Path(__file__).parent / "input.txt").open().read().split("\n")
    print("\nPart one:")
    print(f"{solve(lines[:20])}")

    lines = (Path(__file__).parent / "test_2.txt").open().read().split("\n")
    print("\nPart two test:")
    print(f"{solve(lines)}")

    lines = (Path(__file__).parent / "input.txt").open().read().split("\n")
    print("\nPart two:")
    print(f"{solve(lines)}")
    
