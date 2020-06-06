#!/usr/bin/env python3
import sys
import torch
import pickle

ALPHA = 0.1
EPOCHS = 10000


def read_data(filename):
    if filename.endswith(".pkl"):
        in_val, out_val, labels = pickle.load(open(filename, 'rb'))
    else:
        lines = open(filename).read().splitlines()
        in_val, out_val, labels = [], [], []
        for line in lines:
            parts = line.split(',')
            in_val.append([float(x) for x in parts[1:]])
            out_val.append([1.0 if x == int(parts[0]) else 0.0 for x in range(10)])
            labels.append([int(parts[0])])
        pickle.dump((in_val, out_val, labels), open("{}.pkl".format(filename.split('.')[0]), 'wb'))
    return torch.tensor(in_val), torch.tensor(out_val), torch.tensor(labels)


def create_network():
    return torch.nn.Sequential(
        torch.nn.Linear(784, 300, bias=True),
        torch.nn.Sigmoid(),
        torch.nn.Linear(300, 100, bias=False),
        torch.nn.Sigmoid(),
        torch.nn.Linear(100, 10, bias=False)
    )


def test(network, test_in, test_out, labels, criterion):
    print(network.eval())

    with torch.no_grad():
        output = network(test_in)
        total_loss = criterion(output, test_out)
        pred = output.argmax(dim=1, keepdim=True)
        correct = pred.eq(labels.view_as(pred)).sum().item()

    print("\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
        total_loss, correct, len(test_out),
        100. * correct / len(test_out)))


def main():
    network = create_network()
    train_in, train_out = read_data(sys.argv[1])[:2]
    test_in, test_out, labels = read_data(sys.argv[2])

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(network.parameters(), lr=ALPHA)

    if "--gpu" in sys.argv[-1]:
        dev = torch.device("cuda")
        train_in, train_out = train_in.to(dev), train_out.to(dev)
        test_in, test_out, labels = test_in.to(dev), test_out.to(dev), labels.to(dev)
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
    test(network, test_in, test_out, labels, criterion)

if __name__ == "__main__":
    main()
