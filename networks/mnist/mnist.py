#!/usr/bin/env python3
import sys
import torch
import pickle

ALPHA = 0.1
EPOCHS = 100000
BATCH_SIZE = 128


def read_data(filename):
    if filename.endswith(".pkl"):
        in_val, out_val = pickle.load(open(filename, 'rb'))
    else:
        lines = open(filename).read().splitlines()
        in_val, out_val = [], []
        for line in lines:
            parts = line.split(',')
            in_val.append([float(x) for x in parts[1:]])
            out_val.append([1.0 if x == int(parts[0]) else 0.0 for x in range(10)])
        pickle.dump((in_val, out_val), open("{}.pkl".format(filename.split('.')[0]), 'wb'))
    return torch.tensor(in_val), torch.tensor(out_val)


def create_network():
    return torch.nn.Sequential(
        torch.nn.Linear(784, 300, bias=True),
        torch.nn.Sigmoid(),
        torch.nn.Linear(300, 100, bias=False),
        torch.nn.Sigmoid(),
        torch.nn.Linear(100, 10, bias=False)
    )


def main():
    network = create_network()
    train_in, train_out = read_data(sys.argv[1])
    test_in, test_out = read_data(sys.argv[2])

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(network.parameters(), lr=ALPHA)

    if "--gpu" in sys.argv[-1]:
        dev = torch.device("cuda")
        train_in, train_out = train_in.to(dev), train_out.to(dev)
        test_in, test_out = test_in.to(dev), test_out.to(dev)
        network = network.cuda()

    for epoch in range(EPOCHS + 1):  # training stuff
        loss = criterion(network(train_in), train_out)
        if not epoch % 500 or epoch < 10:
            print('epoch: ', epoch, ' loss: ', loss.item())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print("Finished Training")
    torch.save(network, 'mnist_model.torch')
    print("Saved model to mnist_model.torch")
    print("Final Total Loss: {}".format(criterion(network(test_in), test_out)))


if __name__ == "__main__":
    main()
