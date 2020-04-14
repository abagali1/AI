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
    file = open(file).read().splitlines()
    for line in file[:-1]:
        w = [float(x) for x in line.split(" ")]
        amt = len(w)
        out_nodes = amt // in_nodes
        weights.append([w[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes = out_nodes
        count += 1
    weights.append([[float(x)] for x in file[-1].split(" ")])
    return weights, count


def dot(x, y):
    return sum([x[i] * y[i] for i in range(len(y))])


def feedforward(inputs, layers, tf):
    for pos, layer in enumerate(layers[0]):
        inputs = [tf(x) for x in [dot(inputs, weights) for weights in layer]] if pos < layers[1] else [dot([inputs[i]], weight) for i, weight in enumerate(layer)]
    return inputs


def main():
    tf, inputs = TRANSFERS[argv[2]], [*map(float, argv[3:])]
    layers = read_weights(argv[1], len(inputs))
    print(' '.join([*map(str, feedforward(inputs, layers, tf))]))


if __name__ == "__main__":
    main()
