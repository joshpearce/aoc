#!/usr/bin/env python3

from collections import namedtuple

Box = namedtuple("Box", "x1, x2, y1, y2")
Point = namedtuple("Point", "x, y")

def y_gen(p0, v0):
    pn = p0 + v0
    vn = v0
    yield pn
    while True:
        vn -= 1
        pn = pn + vn
        yield pn

def x_gen(p0, v0):
    pn = p0 + v0
    vn = v0
    yield pn
    while True:
        if vn != 0:
            vn = vn -1 if v0 > 0 else vn + 1
        pn = pn + vn
        yield pn

# check if box is in negative part of graph and return true/false
# also if box straddles the origin, return largest chuck on one
# side of the origin, and it's sign
def box_x_sign(box):
    if box.x1 < 0 and box.x2 <= 0:
        return -1, box
    elif box.x1 >= 0 and box.x2 > 0:
        return 1, box
    else:
        if abs(box.x1) > abs(box.x2):
            return -1, Box(box.x1, 0, box.y1, box.y2)
        else:
            return 1, Box(0, box.x2, box.y1, box.y2)

def in_box(p, box):
    past_x = p.x > box.x2
    past_y = p.y < box.y1
    in_box = p.x >= box.x1 and p.x <= box.x2 and p.y >= box.y1 and p.y <= box.y2
    return in_box, past_x, past_y

def part_one(bits):

    Y_START = 500
    X_STOP = 100
    SERIES_STOP = 10000
    vxsign, newbox = box_x_sign(box)
    success = False
    max_y = 0
    inbox, pastx, pasty = False, False, False
    for vy in range(Y_START, 1, -1):
        for vx in range(0, X_STOP * vxsign, vxsign):
            #print(f"{vx}, {vy}")
            yg = y_gen(0, vy)
            xg = x_gen(0, vx)
            local_max_y = 0
            for _ in range(SERIES_STOP):
                p = Point(next(xg), next(yg))
                #print(f"Point: {p}")
                local_max_y = max(local_max_y, p.y)
                inbox, pastx, pasty = in_box(p, newbox)
                if pastx or pasty:
                    break
                if inbox:
                    max_y = max(local_max_y, max_y)
                    #print(f"Initial Velocities: {vx}, {vy}")
                    #print(f"Intersect Point: {p.x}, {p.y}")
                    #print(f"Local max y: {local_max_y}")
                    break

    return max_y

def part_two(box):
    Y_START = 600
    Y_STOP = -300
    X_STOP = 400
    SERIES_STOP = 10000
    vxsign, newbox = box_x_sign(box)
    int_vecs = set()
    inbox, pastx, pasty = False, False, False
    for vy in range(Y_START, Y_STOP, -1):
        for vx in range(0, X_STOP * vxsign, vxsign):
            #print(f"{vx}, {vy}")
            yg = y_gen(0, vy)
            xg = x_gen(0, vx)
            for _ in range(SERIES_STOP):
                p = Point(next(xg), next(yg))
                #print(f"Point: {p}")
                inbox, pastx, pasty = in_box(p, newbox)
                if pastx or pasty:
                    break
                if inbox:
                    #print(f"Initial Velocities: {vx}, {vy}")
                    #print(f"Intersect Point: {p.x}, {p.y}")
                    int_vecs.add((vx, vy))

    return len(int_vecs)

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    f = "input.txt"
    lines = (Path(__file__).parent / f).open().read().split("\n")
    xp, yp = lines[0].replace(",", "").split(" ")[2:4]
    x1, x2, = map(int, xp[2:].split(".."))
    y1, y2, = map(int, yp[2:].split(".."))
    box = Box(x1, x2, y1, y2)

    print("\nPart one:")
    print(f"{part_one(box)}")

    print("Part two:")
    print(f"{part_two(box)}")
    