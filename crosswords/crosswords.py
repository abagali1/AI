#!/usr/bin/env python3
import sys
from re import compile, IGNORECASE, match

SEED_REGEX = compile(r"(V|H)(\d*)x(\d*)(\w+|#)", IGNORECASE)
BLOCK = '#'
EMPTY = '-'


FILE = ""
BOARD = []
HEIGHT, WIDTH, AREA, BLOCKS = 0,0,0,0
SEEDS = []
INDICES, INDICES_2D = {}, {}


def to_string(pzl):
    return '\n'.join([''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]).strip()


def rotate180(pivot):
    return (WIDTH - pivot[0] - 1, HEIGHT - pivot[1] - 1)


def place_words():
  global BOARD, SEEDS


def main():
  global HEIGHT, WIDTH, SEEDS, FILE, BOARD, BLOCKS, INDICES, INDICES_2D
  for arg in sys.argv[1:]:
    if 'H' == arg[0].upper() or 'V' == arg[0].upper():
      groups = match(SEED_REGEX, arg).groups()
      SEEDS.append((groups[0], (int(groups[1]), int(groups[2])), groups[3].lower()))
    elif '.txt' in arg:
      FILE = arg
    elif arg.isdigit():
      BLOCKS = int(arg)
    else:
      HEIGHT, WIDTH = (int(x) for x in arg.split('x'))
      AREA = HEIGHT*WIDTH
  INDICES = {index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)}
  INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT) for j in range(WIDTH)}
  
  if BLOCKS == AREA:
    print(to_string(BLOCK*AREA))
    return
  
  BOARD = [*EMPTY*AREA]
  place_words()

  if BLOCKS == 0:
    print(to_string(BOARD))
    return
  


if __name__ == '__main__':
  main()
