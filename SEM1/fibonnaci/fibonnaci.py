#!/usr/bin/env python3
from sys import argv


def fib(n):
  return n if n<2 else fib(n-1) + fib(n-2)


print(fib(int(argv[1])))
