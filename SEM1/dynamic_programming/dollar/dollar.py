#!/usr/bin/env python3
from sys import argv


def change(total, coins):
  return total, coins



val = int(argv[1])
coins = [int(x) for x in argv[2:]]
print(change(val,coins))
