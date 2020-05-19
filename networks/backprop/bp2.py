#!/usr/bin/env python3
from math import exp
from sys import argv
from random import random, uniform, seed

ALPHA = 0.15
DATASET_LENGTH = 100000
EPOCHS = 5


def tf(x):
    return 1 / (1 + exp(-x))


def derivative(x):
    return x * (1 - x)


def hadamard(x: list, y: list) -> list:
    return [i * j for i, j in zip(x, y)]


def dot(x: list, y: list) -> float:
    return sum(hadamard(x, y))


def parse_args(s):
    ineq, val = "", ""
    for char in s[7:]:
        if char.isdigit() or char == ".":
            val += char
        else:
            ineq += char
    return ineq, val


def construct_network(in_nodes):
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
    train_in, train_out = [], []
    for i in range(DATASET_LENGTH):
        x, y = uniform(-1.5, 1.5), uniform(-1.5, 1.5)
        train_in.append([x, y, 1])
        train_out.append([int(eval(s.format(x, y)))])
    while True:
        for inputs, output in zip(train_in, train_out):
            update_weights(network, backprop(network, feedforward(network, inputs), output[0]))
        print(
            '\n'.join(map(str, ([', '.join(map(str, weights)) for weights in layer] for layer in network[0]))).replace(
                "'", ""), '\n')


def main():
    seed(1738114)
    network = construct_network(2)
    print("Layer Counts: {} {}".format(2 + 1, ' '.join(str(len(x)) for x in network[0])))
    ineq, val = parse_args(argv[1])
    train(network, "({})**2+({})**2" + ineq + val)


if __name__ == "__main__":
    main()
