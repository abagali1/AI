#!/usr/bin/env python3
from sys import argv
from math import exp

TRANSFERS = {
    'T1': lambda x: x,
    'T2': lambda x: max(0, x),
    'T3': lambda x: 1 / (1 + exp(-x)),
    'T4': lambda x: -1 + 2 / (1 + exp(-x))
}


def read_weights(file: str, in_nodes: int) -> tuple:
    """
    Takes in a filename and amount of input nodes and returns a tuple of layers and amount of layers
    :param file: file to read weights from
    :param in_nodes: amount of input nodes
    :return: ([layers], amount of layers)
    """
    weights, count, file = [], 0,  open(file).read().splitlines()
    for line in file[:-1]:
        w = [float(x) for x in line.split(" ")]
        amt = len(w)
        out_nodes = amt // in_nodes
        weights.append([w[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes, count = out_nodes, count + 1
    weights.append([[float(x)] for x in file[-1].split(" ")])
    return weights, count


def dot(x: list, y: list) -> float:
    """
    Returns the dot product of two matrices, assumes matrices are of equal dimension
    :param x: First matrix
    :param y: Second matrix
    :return: dot product of two matrices
    """
    return sum(x[i] * y[i] for i in range(len(y)))


def feedforward(inputs: list, layers: tuple, tf: callable) -> list:
    """
    Iteratively feeds inputs through neural network with layers and transfer function tf
    :param inputs: initial inputs
    :param layers: neural network layers
    :param tf: transfer function to use
    :return: list of final values outputted after feedforward
    """
    for i in range(layers[1]):
        inputs = [tf(dot(inputs, weights)) for weights in layers[0][i]]
    return [dot([i], weight) for i, weight in zip(inputs, layers[0][-1])]


def main():
    inputs = [*map(float, argv[3:])]
    print(' '.join([*map(str, feedforward(inputs, read_weights(argv[1], len(inputs)), TRANSFERS[argv[2]]))]))


if __name__ == "__main__":
    main()
