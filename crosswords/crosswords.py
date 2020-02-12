#!/usr/bin/env python3
import sys
from re import compile, IGNORECASE, match

SEED_REGEX = compile(r"(V|H)(\d*)x(\d*)(.+)", IGNORECASE)
BLOCK = '#'
EMPTY = '-'


FILE = ""
BOARD = []
HEIGHT, WIDTH, AREA, BLOCKS = 0,0,0,0
SEEDS = []
INDICES, INDICES_2D = {}, {}
ROTATIONS = {}
NEIGHBORS = {}


def to_string(pzl):
    return '\n'.join([''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]).strip()


def rotate180(board, pivot):
    return board[INDICES_2D[(WIDTH - pivot[0] - 1, HEIGHT - pivot[1] - 1)]]


def place_words():
  global BOARD
  for seed in SEEDS:
    if seed[0] == 'H':
      BOARD[INDICES_2D[(seed[1],seed[2])]:len(seed[3])] = seed[3]
    if seed[0] == 'V':
      idx = INDICES_2D[(seed[1],seed[2])]
      for i in range(len(seed[3])):
        BOARD[idx+(WIDTH*i)] = seed[3][i]


def main():
  global HEIGHT, WIDTH, SEEDS, FILE, BOARD, BLOCKS, INDICES, INDICES_2D, ROTATIONS, NEIGHBORS
  for arg in sys.argv[1:]:
    if 'H' == arg[0].upper() or 'V' == arg[0].upper():
      groups = match(SEED_REGEX, arg).groups()
      SEEDS.append((groups[0].upper(), int(groups[1]), int(groups[2]), [*groups[3].lower()]))
    elif '.txt' in arg:
      FILE = arg
    elif arg.isdigit():
      BLOCKS = int(arg)
    else:
      HEIGHT, WIDTH = (int(x) for x in arg.split('x'))
  
  AREA = HEIGHT*WIDTH
  INDICES = {index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)} # idx -> (row, col)
  INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT) for j in range(WIDTH)} # (row, col) -> idx
  
  if BLOCKS == AREA:
    return to_string(BLOCK*AREA)
  
  BOARD = [*EMPTY*AREA]
  place_words()

  if BLOCKS == 0:
    return to_string(BOARD)

  for index in range(0, AREA):  # saves all possible neighbors for all indices
    row = index // WIDTH
    neighbors = [i for i in [index + WIDTH, index - WIDTH] if 0 <= i < AREA]
    if (index + 1) // WIDTH == row and index + 1 < AREA:
        neighbors.append(index + 1)
    if (index - 1) // WIDTH == row and index - 1 >= 0:
        neighbors.append(index - 1)
    NEIGHBORS[index] = neighbors
  


if __name__ == '__main__':
  print(main())
