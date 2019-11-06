#!/usr/bin/env python3
from sys import argv

max_range = set(range(0,20))
syms = {'A', 'B', 'C'}


ADJACENTS = {
    0: {1, 19, 10},
    1: {0, 2, 8},
    2: {1, 3, 6},
    3: {2, 4, 19},
    4: {3, 5, 17},
    5: {4, 6, 15},
    6: {2, 5, 7},
    7: {6, 8, 14},
    8: {1, 7, 9},
    9: {8, 10, 13},
    10: {0, 9, 11},
    11: {10, 12, 18},
    12: {11, 13, 16},
    13: {12, 14, 9},
    14: {7, 15, 13},
    15: {14, 5, 16},
    16: {15, 12, 17},
    17: {14, 13, 16},
    18: {13, 9, 11},
    19: {0, 3, 18},
}


def brute_force_set():
    results = []
    for i in ADJACENTS:
        tmp, restricted = {i}, {i}
        restricted.update(ADJACENTS[i])
        for j in max_range:
            if j not in restricted:
                tmp.add(j)
                restricted.update(ADJACENTS[j])
        results.append(tmp)
    return max(results, key=lambda x: len(x))


def brute_force_colors(pzl):
    if is_invalid(pzl):
        return ""
    if is_solved(pzl):
        return pzl

    i = pzl.find('.')
    new_pzls = [pzl[:i] + str(j) + pzl[i + 1:] for j in syms]
    for new_pzl in new_pzls:
        b_f = brute_force_colors(new_pzl)
        if b_f:
            return b_f


def is_invalid(pzl):
    for i in ADJACENTS:
        if pzl[i] != '.':
            if pzl[i] in [pzl[j] for j in ADJACENTS[i] if pzl[j] != '.']:
                return True
    return False


def is_solved(pzl):
    return '.' not in pzl


pzl = 'AB..................'
print(brute_force_set())
print(brute_force_colors(pzl))