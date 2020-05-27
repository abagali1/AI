#!/usr/bin/env python3
from sys import argv


def parse_args():
    val, ineq = "", ""
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
    return weights, ineq, (float(val) ** 0.5)


def construct_squaring_network(m, in_nodes=2):
    weights, count = [], 0
    for line in m:
        amt = len(line)
        out_nodes = amt // in_nodes
        weights.append([line[i:i + in_nodes] for i in range(0, amt, in_nodes)])
        in_nodes, count = out_nodes, count + 1
    return weights


def derive_network(n, r, ineq):
    weights = []
    for pos, x in enumerate(n[:-1]):
        layer, nodes = [], len(x)
        for y in range(nodes+nodes):
            layer_weights = x[y % nodes]
            if pos == 0:  # combine initial weights
                if y < nodes:
                    layer.append([layer_weights[0] / r, 0.0, layer_weights[1]])
                else:
                    layer.append([0.0, layer_weights[0] / r, layer_weights[1]])
            else:  # combine other layers
                if y < nodes:
                    layer.append([*layer_weights, *[0.0 for _ in layer_weights]])  # weights for top "x-squarer" network
                else:
                    layer.append([*[0.0 for _ in layer_weights], *layer_weights])  # weights for bottom "y-squarer" network
        weights.append(layer)
    if ">" in ineq:
        weights.append([n[-1][0]*2])  # network addition weights
        weights.append([[0.68394]])  # final weight
    else:
        weights.append([[n[-1][0][0]*-1, n[-1][0][0]*-1]])
        weights.append([[1.85914]])
    return weights


def main():
    file_weights, ineq, val = parse_args()
    square_x = construct_squaring_network(file_weights)
    network = derive_network(square_x, val, ineq)
    print("Layer Counts: {} {}".format(2 + 1, ' '.join(str(len(x)) for x in network)))
    print(
        '\n'.join(map(str, ([', '.join(map(str, weights)) for weights in layer] for layer in network)))
            .replace("'", ""), '\n'
    )


if __name__ == "__main__":
    main()
