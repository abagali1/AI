#!/usr/bin/env python3
from sys import argv

CACHE = {}
seen = set()

def change(total, coins):
  if(total < 0):
    return 0
  if(total == 0):
    return 1

  if total not in CACHE:
    CACHE[total] = sum([change(total-x, coins) for x in coins])
    print(CACHE[total])
  return CACHE[total]


val = int(argv[1])
coins = [int(x) for x in argv[2:]]

print(change(val,coins))
