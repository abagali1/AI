#!/usr/bin/env python3
from sys import argv

MASKS = { # << = positive ///\\\ >>=negative
    1: 18374403900871474942,        
    -1: 9187201950435737471,    
    8: 18446744073709551360,    
    -8: 72057594037927935,     
    7: 9187201950435737344,
    -7: 71775015237779198,
    9: 18374403900871474688,
    -9: 35887507618889599
}                        
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



def bit_not(x):
    return 18446744073709551615 - x  


def fill(current, opponent, direction):
    flood = 0b0
    empty = bit_not( (current | opponent))
    w = (((current&MASKS[direction]) << direction) & opponent) if direction > 0 else (((current&MASKS[direction]) >> direction*-1) & opponent)
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    w |= (w << direction) & opponent if direction > 0 else (w>>direction*-1)&opponent
    return (flood|(w<<direction))&empty if direction > 0 else (flood|(w>>direction*-1))&empty


def possible_moves(board, piece):
    final = 0b0
    for d in MASKS:
        final |= fill(board[piece], board[not piece], d)
    return {pos for pos,elem in enumerate('{:064b}'.format(final)) if elem == '1'}
    

def to_string(b):
    return '\n'.join(
        [''.join(['{:064b}'.format(b)[i*8 +j][0] for j in range(8)]) for i in range(8)]).strip().lower()


def main():
    piece = ''
    board = '.'*27 + 'OX......XO'+'.'*27
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
        1: int(board.replace('.','0').replace('X','1').replace('O','0'), base=2),
        0: int(board.replace('.','0').replace('X','0').replace('O','1'), base=2)
    }

    p = possible_moves(board, piece)
    return p if len(p) > 0 else "No moves possible"




if __name__ == "__main__":
    print(main())
