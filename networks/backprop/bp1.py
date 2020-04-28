#!/usr/bin/env python3
from math import exp
from sys import argv
from random import random


def tf(x):
    return 1 / (1 + exp(-x))


def dot(x: list, y: list) -> float:
    return sum(x[i] * y[i] for i in range(len(y)))


def read_data(file):
    inp = open(file).read().splitlines()
    inputs, outputs = [], []
    for x in inp:
        mid = x.find("=")
        inputs.append([float(y) for y in x[:mid-1].split(" ")])
        outputs.append([float(y) for y in x[mid+3:].split(" ")])
    return inputs, outputs, len(inputs[0])


def construct_network(in_nodes):
    weights = [
        [[random() for _ in range(in_nodes)] for _ in range(in_nodes+1)],
        [[random() for _ in range(in_nodes+1)] for _ in range(2)],
        [[random() for _ in range(2)] for _ in range(1)],
        [[random()]]
    ]
    return weights, len(weights)


def feedforward(inputs: list, layers: tuple) -> list:
    for pos, layer in enumerate(layers[0]):
        inputs = [tf(x) for x in [dot(inputs, weights) for weights in layer]] if pos < layers[1] else [dot([inputs[i]], weight) for i, weight in enumerate(layer)]
    return inputs


def main():
    train_in, train_out, in_nodes = read_data(argv[1])
    layers = construct_network(in_nodes)
    print(feedforward(train_in[0], layers))


if __name__ == "__main__":
    main()
