#!/usr/bin/env python3
from math import exp
from sys import argv
from random import uniform


def tf(x):
    return 1 / (1 + exp(-x))


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


def construct_network(file, in_nodes):
    weights, count, file = [], 0, open(file).read().splitlines()
    for line in file[:-1]:
        w = [float(x) for x in line.split(" ")]
        amt = len(w)
        out_nodes = amt // in_nodes
        weights.append([w[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes, count = out_nodes, count + 1
    weights.append([[float(x)] for x in file[-1].split(" ")])
    return weights, count


def test(network, inputs):
    for i in range(network[1]):
        inputs = [tf(dot(inputs, weights)) for weights in network[0][i]]
    return [dot([i], weight) for i, weight in zip(inputs, network[0][-1])]


def test_points(network, s):
    train_in, train_out, actual_out, error, bad = [], [], [], [], []
    for i in range(100000):
        x, y = uniform(-1.5, 1.5), uniform(-1.5, 1.5)
        train_in.append([x, y, 1])
        train_out.append([int(eval(s.format(x, y)))])
        actual_out.append(test(network, train_in[i]))
        bad.append(actual_out[i][0] >= .5 if not train_out[i][0] else actual_out[i][0] < .5)

        if bad.count(True) >= 15:
            print("15 BAD VALUES CAUGHT, EXITING")
            count = 0
            for j in range(len(bad)):
                if bad[j]:
                    print("{}: {} => {}; {} {}".format(j, train_in[j], train_out[j], actual_out[j],
                                                       '*' if bad[j] else ''))
                    count += 1
                if count >= 15:
                    break
            break
    with open("output.txt", 'w') as w:
        for i in range(len(bad)):
            w.write("{}: {} => {}; {} {}\n".format(i, train_in[i], train_out[i], actual_out[i],
                                                 '*' if bad[i] else ''))


def main():
    network = construct_network("weights.txt", 3)
    ineq, val = parse_args(argv[1])
    test_points(network, "({})**2+({})**2" + ineq + val)


if __name__ == "__main__":
    main()
