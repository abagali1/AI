#!/usr/bin/env python3
from sys import argv
from random import seed


def parse_args():
    ineq, val = "", ""
    for char in argv[2][7:]:
        if char.isdigit() or char == ".":
            val += char
        else:
            ineq += char
    lines = open(argv[1]).read().splitlines()
    weights = []
    for line in lines:
        nums, tmp = line.replace(',', '').replace('[', '').replace(']', '').split(" "), []
        for num in nums:
            try:
                tmp.append(float(num))
            except ValueError:
                continue
        if tmp:
            weights.append(tmp)
    return weights, ineq, val


def construct_squaring_network(m, in_nodes=2):
    weights, count = [], 0
    for line in m[:-1]:
        w = [float(x) for x in line]
        amt = len(w)
        out_nodes = amt // in_nodes
        weights.append([w[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes, count = out_nodes, count + 1
    weights.append([[float(x)] for x in m[-1]])
    return weights, count




def main():
    seed(1738114)
    file_weights, inequal, val = parse_args()
    square_x = construct_squaring_network(file_weights)
    # square_y = ([[y.copy() for y in x] for x in square_x[0]], square_x[1])


if __name__ == "__main__":
    main()
