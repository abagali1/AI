#!/usr/bin/env python3
from sys import argv

CACHE = {}

def fib(n):
    if n < 2:
        return n
    if n not in CACHE:
        x = fib(n-1) + fib(n-2)
        CACHE[n] = x
    return CACHE[n]


print(fib(int(argv[1])))
x = fib(998)
print(fib(1000))
y = fib(1500)
print("")
print(fib(2000))
