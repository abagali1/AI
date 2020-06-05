#!/usr/bin/env python3
import sys
import torch
from torchvision import datasets


def read_data(**kwargs):
    return datasets.MNIST(".", download=True, **kwargs)


def main():
    training = read_data(train=True)
    testing = read_data(train=False)


if __name__ == "__main__":
    main()
