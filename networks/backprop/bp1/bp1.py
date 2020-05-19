#!/usr/bin/env python3
from math import exp
from sys import argv
from random import random, seed

ALPHA = 0.1


def tf(x):
    return 1 / (1 + exp(-x))


def derivative(x):
    return x * (1 - x)


def dot(x: list, y: list) -> float:
    return sum(i * j for i, j in zip(x, y))


def read_data(file):
    inputs, outputs = [], []
    for x in open(file).read().splitlines():
        mid = x.find("=")
        inputs.append([float(y) for y in x[:mid - 1].split(" ")] + [1.0])
        outputs.append([float(y) for y in x[mid + 3:].split(" ")])
    return inputs, outputs, len(inputs[0]) - 1


def construct_network(in_nodes):
    weights = [
        [[random() for _ in range(in_nodes + 1)] for _ in range(2)],
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


def train(network, train_in, train_out):
    for _ in range(75000):
        for inputs, output in zip(train_in, train_out):
            update_weights(network, backprop(network, feedforward(network, inputs), output[0]))
    return network


def test(network, *inputs):
    inputs = [*inputs, 1]
    for i in range(network[1]):
        inputs = [tf(dot(inputs, weights)) for weights in network[0][i]]
    return [dot([i], weight) for i, weight in zip(inputs, network[0][-1])]


def main():
    seed(1738114)
    train_in, train_out, in_nodes = read_data(argv[1])
    network = construct_network(in_nodes)
    print("Layer Counts: {} {}".format(in_nodes + 1, ' '.join(str(len(x)) for x in network[0])))
    network = train(network, train_in, train_out)
    print('\n'.join(map(str, ([', '.join(map(str, weights)) for weights in layer] for layer in network[0]))).replace("'", ""), '\n')


if __name__ == "__main__":
    main()
