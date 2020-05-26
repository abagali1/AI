#!/usr/bin/env python3
from sys import argv
from random import random, seed


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
    return weights, ineq, float(val)


def construct_squaring_network(m, in_nodes=2):
    weights, count = [], 0
    for line in m:
        w = [float(x) for x in line]
        amt = len(w)
        out_nodes = amt // in_nodes
        weights.append([w[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes, count = out_nodes, count + 1
    return weights, count


def derive_network(n, r, ineq):
    weights = []
    for pos, x in enumerate(n[0][:-1]):
        layer = []
        if pos == 0:
            nodes = len(x)
            for y in range(nodes+nodes):
                layer_weights = x[y % nodes]
                if y < nodes:
                    layer.append([layer_weights[0], 0, layer_weights[1]])
                else:
                    layer.append([0, layer_weights[0], layer_weights[1]])
        else:
            nodes = len(x)
            for y in range(nodes+nodes):
                layer_weights = x[y % nodes]
                if y < nodes:
                    layer.append([*layer_weights, *[0 for _ in layer_weights]])
                else:
                    layer.append([*[0 for _ in layer_weights], *layer_weights])
        weights.append(layer)
    weights.append([[1.0, 1.0]])  # adding weight
    weights.append([[random()]])  # TODO: Figure out determining weight
    return weights


def main():
    seed(1738114)
    file_weights, inequal, val = parse_args()
    square_x = construct_squaring_network(file_weights)
    network = derive_network(square_x, val, inequal)
    print("Layer Counts: {} {}".format(2 + 1, ' '.join(str(len(x)) for x in network)))
    print(
        '\n'.join(map(str, ([', '.join(map(str, weights)) for weights in layer] for layer in network)))
            .replace("'", ""), '\n'
    )


if __name__ == "__main__":
    main()
