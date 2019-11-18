#!/usr/bin/env python3
from time import process_time as time
from math import sqrt
from sys import argv


size_table = { # All possible symbols for each puzzle
    9:  {'1', '2', '3', '4', '5', '6', '7', '8', '9'},
    12: {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C'},
    16: {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G'}
}
size, dim, sub_pzl_row, sub_pzl_col = 0, 0, 0, 0 # global variables describing puzzle physical structure
constraint_table = {} # index points to tuple, (row_index, col_index, sub_pzl_index)
rows, cols, sub_pzls = [], [], [] # list of indices for each group of constraints
NEIGHBORS = {} # index points to neighbor indices
ALL_CONSTRAINTS = [] # rows + cols + sub_pzls


def set_globals(pzl: str, l: int) -> None:
    """
    Initializes global variables specific to the new puzzle
    @param: pzl Puzzle to derive variables from
    @param: l Length of the puzzle
    """
    global size, dim, sub_pzl_row, sub_pzl_col, constraint_table
    size = l # length of the puzzle
    dim = int(sqrt(size)) # dimensions of the puzzle 
    sub_pzl_row = int(sqrt(dim)) # row dimension of the sub puzzle 
    sub_pzl_col = dim // sub_pzl_row # column dimension of the sub puzzle
    gen_constraints() # sets all constraints


def gen_constraints() -> None:
    """
    Sets all global constraint variables
    """
    global rows, cols, sub_pzls, constraint_table, NEIGHBORS, ALL_CONSTRAINTS
    rows = [[] for i in range(dim)]
    cols = [[] for i in range(dim)]
    sub_pzls = [[] for i in range(dim)]
    constraint_table = {}
    for i in range(dim):
        for j in range(dim):
            index = i*dim + j
            r = index // dim
            c = index % dim
            s = (int(index // (dim * sub_pzl_row) *
                sub_pzl_row + (index % dim) // sub_pzl_col))
            constraint_table[index] = (r, c, s)
            rows[r].append(index)
            cols[c].append(index)
            sub_pzls[s].append(index)
    ALL_CONSTRAINTS = rows + cols + sub_pzls
    NEIGHBORS = {i: set(rows[constraint_table[i][0]] + cols[constraint_table[i][1]]
                        + sub_pzls[constraint_table[i][2]]) - set(str(i)) for i in range(0, size)}


def checksum(pzl: str) -> int:
    """
    Given a solution puzzle, generate a checksum. Used for solution verification
    @param: pzl Puzzle to generate checksum for
    """
    return sum([ord(x) for x in pzl]) - 48*dim*dim


def find_best_index(pzl: str) -> tuple:
    """
    Given a puzzle, find the index with the most amount of symbols able to be placed into that index
    @param: pzl Puzzle to find index for
    """
    max_pos = (-1,-1,set())
    for pos, elem in enumerate(pzl):
        if elem == '.':
            possibilities = set(pzl[j] for j in NEIGHBORS[pos] if pzl[j] != '.')
            length = len(possibilities)
            if length == len(size_table[dim])-1:
                return pos, possibilities
            elif length > max_pos[0]:
                max_pos = (length, pos, possibilities)
    return max_pos[1], max_pos[2]


def find_best_symbol(pzl: str, possibilities: set) -> tuple:
    """
    Given a puzzle, find the symbol with the least amount of places that symbol it can be placed into
    @param: pzl Puzzle to find symbol for
    @param: possibilities List of possibilities generated from find_best_index to help in optimization
    """
    for constraint in ALL_CONSTRAINTS:
        for symbol in size_table[dim] - {pzl[i] for i in constraint if i != '.'}:
            valid_positions = {index for index in constraint if pzl[index]=='.' \
                              and symbol not in {pzl[i] for i in NEIGHBORS[index]}}
            length = len(valid_positions)
            if length == 1 or length < len(possibilities):
                return symbol, valid_positions
    return None, None
          

def brute_force(pzl: str) -> str:
    """
    Given a puzzle, find its solution by judiciously placing symbols into every available position
    @param: pzl Puzzle to find solution for
    """
    if '.' not in pzl: 
        return pzl # This puzzle is solved

    index, c_s = find_best_index(pzl) # 2A
    set_of_choices = size_table[dim] - c_s  # If 2A is chosen
    symbol, positions = find_best_symbol(pzl, set_of_choices) # 2B

    if symbol:
        set_of_choices = positions # If 2B is chosen

    for choice in set_of_choices:
        if symbol:
            new_pzl = pzl[:choice] + symbol + pzl[choice+1:] # Splicing specific to 2B
        else:
            new_pzl = pzl[:index] + choice + pzl[index+1:] # Splicing specific to 2A
        b_f = brute_force(new_pzl) # recur on new puzzle
        if b_f:
            return b_f # return solution


if __name__ == '__main__':

    VERBOSE = True  # manually unset this variable for verbose output
    pzls = open('puzzles.txt' if len(argv) <
                2 else argv[1]).read().splitlines() # Read puzzles from file
    start_all = time()
    prev_len = -1 # record previous puzzle length
    for pos, pzl in enumerate(pzls):
        pzl_len = len(pzl)
        if prev_len != pzl_len: # only reset tables if size changes
            set_globals(pzl, pzl_len)
            prev_len = pzl_len
        start = time()
        sol = brute_force(pzl)
        end = time() - start
        if VERBOSE:
            if sol:
                check = checksum(sol)
                print("Pzl {0}:\t{1}\n\t{2} Checksum: {3} Solved in %.2lfs".format(
                    pos+1, pzl, sol, check) % end)
            else:
                print("Pzl {0}: {1} => Unsolvable Solved in %.2lfs".format(
                    pos+1, pzl) % end)
        else:
            if sol:
                check = checksum(sol)
                print("Pzl {0} Checksum {1} Solved in %.2lfs".format(pos+1, check) % end)
            else:
                print("Pzl {0} Unsolvable Solved in %.2lfs".format(pos+1) % end)
    print("Total Time: %.2lfs" % (time()-start_all))
