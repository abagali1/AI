import sys
import torch
import pickle


def read_data(filename):
    if '.pkl' in filename:
        in_val, out_val = pickle.load(open(filename, 'rb'))
    else:
        lines = open(filename).read().splitlines()
        name = filename.split('.')[0]
        in_val, out_val = [], []
        for line in lines:
            parts = line.split(',')
            in_val.append([float(x) for x in parts[1:]])
            out_val.append(float(parts[0]))
        pickle.dump((in_val, out_val), open("{}.pkl".format(name), 'wb'))
    return torch.tensor(in_val), torch.tensor(out_val)


def main():
    train_in, train_out = read_data(sys.argv[1])
    print(train_in, train_out)


if __name__ == "__main__":
    main()
