#!/usr/bin/env python3
from sys import argv
from math import exp

TRANSFERS = {
    'T1': lambda x: x,
    'T2': lambda x: max(0, x),
    'T3': lambda x: 1 / (1 + exp(-x)),
    'T4': lambda x: -1 + 2 / (1 + exp(-x))
}


def read_weights(file, in_nodes):
    weights, count = [], 0
    for line in open(file).read().splitlines():
        w = [float(x) for x in line.split(" ")]
        amt = len(w)
        out_nodes = amt // in_nodes
        weights.append([w[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes = out_nodes
        count += 1
    return weights, count-1


def dot(x, y):
    return sum([x[i] * y[i] for i in range(len(y))])


def feedforward(inputs, layers, tf):
    for pos, layer in enumerate(layers[0]):
        new_inputs = [dot(inputs, weights) for weights in layer]
        inputs = [tf(x) for x in new_inputs] if pos < layers[1] else new_inputs
    return inputs


def main():
    tf, inputs = TRANSFERS[argv[2]], [*map(float, argv[3:])]
    layers = read_weights(argv[1], len(inputs))
    print(' '.join([*map(str, feedforward(inputs, layers, tf))]))


if __name__ == "__main__":
    main()
