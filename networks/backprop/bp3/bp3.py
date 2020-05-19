#!/usr/bin/env python3
from math import exp
from sys import argv
from random import random, seed

ALPHA = 0.15
DATASET_LENGTH = 100000
EPOCHS = 5


def tf(x):
    return 1 / (1 + exp(-x))


def derivative(x):
    return x * (1 - x)


def dot(x: list, y: list) -> float:
    return sum(i * j for i, j in zip(x, y))


def parse_args():
    return argv[1]


def construct_network(filename, in_nodes):
    weights = [
        [[random() for _ in range(in_nodes + 1)] for _ in range(4)],
        [[random() for _ in range(4)] for _ in range(2)],
        [[random() for _ in range(2)]],
        [[random()]]
    ]
    return weights, len(weights) - 1


def feedforward(layers, inputs):
    values = [inputs]
    for i in range(layers[1]):
        inputs = [tf(dot(inputs, weights)) for weights in layers[0][i]]
        values.append(inputs)
    return values


def backprop(layers, ff_outputs, t):
    x, w = ff_outputs[-1][0], layers[0][-1][0][0]
    grad = [[[(t - (x * w)) * x]]]
    prev_error = [(t - (x * w)) * w * derivative(x)]

    for ff_in, layer in zip(ff_outputs[:-1][::-1], layers[0][:-1][::-1]):
        grad.append([[x * e for x in ff_in] for e in prev_error])
        error = [0 for _ in range(len(layer[0]))]
        for pos, weights in enumerate(layer):
            for p2, weight in enumerate(weights):
                error[p2] += (weight * prev_error[pos]) * derivative(ff_in[p2])
        prev_error = error
    return grad[::-1]


def update_weights(network, grad):
    for layer_idx in range(len(network[0])):
        for weights_idx in range(len(network[0][layer_idx])):
            for weight_idx in range(len(network[0][layer_idx][weights_idx])):
                network[0][layer_idx][weights_idx][weight_idx] += grad[layer_idx][weights_idx][weight_idx] * ALPHA
    return network


def train(network, s):
    print('\n'.join(map(str, ([', '.join(map(str, weights)) for weights in layer] for layer in network[0]))).replace("'", ""), '\n')


def main():
    seed(1738114)
    filename = parse_args()
    network = construct_network(2)
    print("Layer Counts: {} {}".format(2 + 1, ' '.join(str(len(x)) for x in network[0])))


if __name__ == "__main__":
    main()
