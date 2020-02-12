#!/usr/bin/env python3
import sys
from re import compile, IGNORECASE, match

SEED_REGEX = compile(r"(V|H)(\d*)x(\d*)(.+)", IGNORECASE)
BLOCK = '#'
EMPTY = '-'
FILE = ""

BOARD, SEEDS = [], []
HEIGHT, WIDTH, AREA, BLOCKS = 0,0,0,0
INDICES = {} # idx -> (row, col)
INDICES_2D = {} # (row, col) -> idx
ROTATIONS = {} # idx -> rotated 180 idx
NEIGHBORS = {} # idx -> [neighbors]
ROWS = [] # [ [idxs in row 0], [idxs in row 1]]
COLS = [] # [ [idxs in col 0], [idxs in col 1]]
CONSTRAINTS = [] # [[row0], [row1], [col0], col[1]]
FULL_WALL = [] # [*'#'*WIDTH]

# print 2d board
to_string = lambda pzl: '\n'.join([''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]).strip()


def is_invalid(board, remaining_blocks):
  return False


def brute_force(board, num_blocks, possible=[]):
  if not num_blocks:
    return board
  
  if is_invalid(board, num_blocks):
    return False

  set_of_choices = possible if possible else [pos for pos,elem in enumerate(board) if elem == EMPTY]

  for choice in set_of_choices:
    board[choice] = BLOCK
    b_f = brute_force(board, num_blocks-1)
    if b_f:
      return b_f
    board[choice] = EMPTY 


# helper methods try not to use these
def get_vertical(puzzle, width):
    rows = []
    while len(puzzle) > 0:
        rows.append(puzzle[0:width])
        puzzle = puzzle[width:]
    rows = rows[::-1]
    return rows


def get_horizontal(puzzle, width):
    rows = []
    while len(puzzle) > 0:
        rows.append(puzzle[0:width])
        puzzle = puzzle[width:]
    return [r[::-1] for r in rows]


def cw_180(pzl):
    return get_horizontal(get_vertical(pzl, width=WIDTH), width=WIDTH)


def place_words():
  global BOARD
  for seed in SEEDS:
    if seed[0] == 'H':
      BOARD[INDICES_2D[(seed[1],seed[2])]:len(seed[3])] = seed[3]
    if seed[0] == 'V':
      idx = INDICES_2D[(seed[1],seed[2])]
      for i in range(len(seed[3])):
        BOARD[idx+(WIDTH*i)] = seed[3][i]


def parse_args():
  global HEIGHT, WIDTH, SEEDS, FILE, BOARD, BLOCKS, INDICES, INDICES_2D, ROTATIONS, NEIGHBORS, AREA, FULL_WALL
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
  FULL_WALL = [*BLOCK*WIDTH]
  INDICES = {index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)} # idx -> (row, col)
  INDICES_2D = {(i, j): i * WIDTH + j for i in range(HEIGHT) for j in range(WIDTH)} # (row, col) -> idx


def gen_lookups():
  global NEIGHBORS, ROTATIONS, ROWS, COLS, CONSTRAINTS
  for index in range(0, AREA):  # saves all possible neighbors for all indices
    row = index // WIDTH
    neighbors = [i for i in [index + WIDTH, index - WIDTH] if 0 <= i < AREA]
    if (index + 1) // WIDTH == row and index + 1 < AREA:
        neighbors.append(index + 1)
    if (index - 1) // WIDTH == row and index - 1 >= 0:
        neighbors.append(index - 1)
    NEIGHBORS[index] = neighbors

  ROTATIONS = {i: INDICES_2D[(HEIGHT - INDICES[i][0] - 1, WIDTH - INDICES[i][1] - 1)] for i in range(AREA)}

  ROWS = [[*range(i, i+WIDTH)] for i in range(0, AREA, WIDTH)]
  COLS = [[*range(i,AREA,WIDTH)] for i in range(0, WIDTH)]
  CONSTRAINTS = ROWS + COLS


def main():
  parse_args()

  # bailouts
  if BLOCKS == AREA:
    return to_string(BLOCK*AREA)
  
  BOARD = [*EMPTY*AREA]
  place_words()
  
  if BLOCKS == 0:
    return to_string(BOARD)
  
  # generate any lookup tables, including constraints
  gen_lookups()

  return to_string(brute_force(BOARD, BLOCKS))



if __name__ == '__main__':
  print(main())
