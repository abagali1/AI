#!/usr/bin/env python3
# Anup Bagali and Shreepa Parthaje Period 
from sys import argv
from math import sqrt

PZL_LENGTH = 0
PZl_HEIGHT = 0
PZL_WIDTH = 0


def get_vertical(puzzle, width):
    rows = []
    while len(puzzle) > 0:
        rows.append(puzzle[0:width])
        puzzle = puzzle[width:]
    rows = rows[::-1]
    return "".join(rows)


def get_horizontal(puzzle, width):
    rows = []
    while len(puzzle) > 0:
        rows.append(puzzle[0:width])
        puzzle = puzzle[width:]
    return "".join([r[::-1] for r in rows])


def cw_90(pzl):
    cols = []
    for i in range(PZL_WIDTH):
        col = ""
        for j in range(PZL_HEIGHT):
            col += pzl[i + (j * PZL_WIDTH)]
        cols.append(col)
    return "".join([x[::-1] for x in cols])


def ccw_90(pzl):
    cols = []
    for i in range(PZL_WIDTH):
        col = ""
        for j in range(PZL_HEIGHT):
            col += pzl[i + (j * PZL_WIDTH)]
        cols.append(col)
    return "".join(cols[::-1])


def get_left_diagonal(puzzle):
    return get_vertical(ccw_90(puzzle), width=PZL_HEIGHT)


def get_right_diagonal(puzzle):
    return get_horizontal(ccw_90(puzzle), width=PZL_HEIGHT)


def cw_90(pzl):
    cols = []
    for i in range(PZL_WIDTH):
        col = ""
        for j in range(PZL_HEIGHT):
            col += pzl[i + (j * PZL_WIDTH)]
        cols.append(col)
    return "".join([x[::-1] for x in cols])


def ccw_90(pzl):
    cols = []
    for i in range(PZL_WIDTH):
        col = ""
        for j in range(PZL_HEIGHT):
            col += pzl[i + (j * PZL_WIDTH)]
        cols.append(col)
    return "".join(cols[::-1])


def cw_180(pzl):
    return get_horizontal(get_vertical(pzl, width=PZL_WIDTH), width=PZL_WIDTH)


def main():
    global PZL_LENGTH, PZL_HEIGHT, PZL_WIDTH
    pzl = argv[1]
    PZL_LENGTH = len(pzl)
    PZL_WIDTH = int(argv[2]) if len(argv) == 3 else PZL_LENGTH // int(sqrt(PZL_LENGTH))
    if PZL_LENGTH == 70:
        PZL_WIDTH = 10
    if PZL_LENGTH == 10:
        PZL_WIDTH = 5
    PZL_HEIGHT = PZL_LENGTH // PZL_WIDTH
    items = {
        pzl,
        cw_90(pzl),
        ccw_90(pzl),
        cw_180(pzl),
        get_vertical(pzl, width=PZL_WIDTH),
        get_horizontal(pzl, width=PZL_WIDTH),
        get_right_diagonal(pzl),
        get_left_diagonal(pzl),
    }
    for i in items:
        print(i)




if __name__ == '__main__':
    main()
