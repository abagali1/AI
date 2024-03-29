#!/usr/bin/env python3
from sys import argv
from time import time as time

# << = positive ///\\\ >>=negative   
#     NW     N     NE 
#    <<9    <<8    <<7
#
#     W     .     E
#   <<1          (-1)
# 
#    SW     S     SE
#   (-7)  (-8)    (-9)
# N: 18446744073709551360
# E: 9187201950435737471
# S: 72057594037927935
# W: 18374403900871474942
# NE: 9187201950435737344
# SE: 35887507618889599
# SW: 71775015237779198
# NW: 18374403900871474688

UNMASKS = {  # TODO: Make these all single numbers
    -1: lambda x: (x & 18374403900871474942) >> 1,
    1: lambda x: (x & 9187201950435737471) << 1,
    8: lambda x: x << 8,
    -8: lambda x: x >> 8,
    7: lambda x: (x & 18374403900871474942) << 7,
    9: lambda x: (x & 9187201950435737471) << 9,
    -7: lambda x: (x & 9187201950435737471) >> 7,
    -9: lambda x: (x & 18374403900871474942) >> 9
}

MASKS = {
    -1: 18374403900871474942,
    1: 9187201950435737471,
    8: 0xffffffffffffffff,
    -8: 0xffffffffffffffff,
    7: 18374403900871474942,
    9: 9187201950435737471,
    -7: 9187201950435737471,
    -9: 18374403900871474942
}

POS = {1 << i: 63-i for i in range(64)}


def bit_not(x):
    return 18446744073709551615 - x


def fill(current, opponent, direction):
    mask = MASKS[direction]
    if direction > 0:
        w = ((current & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        w |= ((w & mask) << direction) & opponent
        return w
    else:
        direction *= -1
        w = ((current & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        w |= ((w & mask) >> direction) & opponent
        return w


def possible_moves(board, piece):
    final = 0b0
    possible = set()
    for direction, mask in MASKS.items():
        f = ((fill(board[piece], board[not piece], direction) & mask) << direction) if direction > 0 else (
                    (fill(board[piece], board[not piece], direction) & mask) >> direction * -1)
        final |= f & (18446744073709551615 - (board[piece] | board[not piece]))
    while final:
        b = final & -final
        possible.add(POS[b])
        final -= b
    return possible


def to_string(b):
    return '\n'.join(
        [''.join(['{:064b}'.format(b)[i * 8 + j][0] for j in range(8)]) for i in range(8)]).strip().lower()


def main():
    piece = ''
    board = '.' * 27 + 'OX......XO' + '.' * 27
    if len(argv) != 0:
        for arg in argv[1:]:
            if len(arg) == 64:
                board = arg.upper()
            elif arg.lower() == 'x' or arg.lower() == 'o':
                piece = arg.upper()
    if not piece:
        piece = 0 if board.count(".") % 2 != 0 else 1
    else:
        piece = 0 if piece == "O" else 1
    board = {
        1: int(board.replace('.', '0').replace('X', '1').replace('O', '0'), base=2),
        0: int(board.replace('.', '0').replace('X', '0').replace('O', '1'), base=2)
    }

    p = possible_moves(board, piece)
    return p if len(p) > 0 else "No moves possible"


if __name__ == "__main__":
    start = time()
    print(main())
    print("{0}".format(time() - start))
