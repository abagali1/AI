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
    return weights, ineq, float(val)


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


def derive_network(n, r, ineq):
    weights = []
    for pos, x in enumerate(n[0][:-1]):
        layer = []
        if pos == 0:
            nodes = len(x)
            for y in range(nodes+nodes):
                layer_weights = x[y % nodes]
                if y < nodes:
                    layer.append([layer_weights[0] / r, 0, layer_weights[1] / r])
                else:
                    layer.append([0, layer_weights[0] / r, layer_weights[1] / r])
        else:
            nodes = len(x)
            for y in range(nodes+nodes):
                layer_weights = x[y % nodes]
                if y < nodes:
                    layer.append([*layer_weights, 0, 0, 0])
                else:
                    layer.append([0, 0, 0, *layer_weights])
        weights.append(layer)
    weights.append([[1.0, 1.0]])  # adding weight
    weights.append([[99999]])  # TODO: Figure out determining weight
    return weights


def main():
    seed(1738114)
    file_weights, inequal, val = parse_args()
    network = derive_network(construct_squaring_network(file_weights), val, inequal)
    print(
        '\n'.join(map(str, ([', '.join(map(str, weights)) for weights in layer] for layer in network)))
            .replace("'", ""), '\n'
    )


if __name__ == "__main__":
    main()
