#!/usr/bin/env python3
from sys import argv
from time import process_time as time

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

# MASKS = { # FIXME: fix these numbers
#     1: 18374403900871474942,        
#     -1: 9187201950435737471,    
#     8: 18446744073709551360,    
#     -8: 72057594037927935,     
#     9: 9187201950435737344,
#     -7: 71775015237779198,
#     7: 18374403900871474688,
#     -9: 35887507618889599
# }   

MASKS = { #TODO: Make these all single numbers
    1: lambda x:  (x & 18374403900871474942) >> 1,
    -1: lambda x: (x & 9187201950435737471) << 1,
    8: lambda x: x<<8,
    -8: lambda x: x>>8,
    9: lambda x: ((x & 18374403900871474942) >> 1)<<8,
    7: lambda x: ((x & 9187201950435737471) << 1)<<8,
    -9: lambda x: ((x & 9187201950435737471) << 1)>>8,
    -7: lambda x: ((x & 18374403900871474942) >> 1)>>8
}
bit_not = lambda x: 18446744073709551615 - x
is_on = lambda x, pos: x & (1<<pos)

binary_to_board = lambda board: "".join(['o' if is_on(board[0], 63-i) else 'x' if is_on(board[1],63-i) else '.' for i in range(64)])

board_to_string = lambda x: '\n'.join([''.join([x[i*8+j]][0] for j in range(8)) for i in range(8)]).strip().lower()
binary_to_string = lambda x: '\n'.join([''.join(['{:064b}'.format(x)[i*8 +j][0] for j in range(8)]) for i in range(8)]).strip().lower()

print_binary = lambda x: print(binary_to_string(x))
print_board = lambda x: print(board_to_string(x))
print_board_binary = lambda x: print(board_to_string(binary_to_board(x)))


LETTERS = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7, 'A1': 0, 'B1': 1, 'C1': 2, 'D1': 3, 'E1': 4, 'F1': 5, 'G1': 6, 'H1': 7, 'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15, 'A2': 8, 'B2': 9, 'C2': 10, 'D2': 11, 'E2': 12, 'F2': 13, 'G2': 14, 'H2': 15, 'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23, 'A3': 16, 'B3': 17, 'C3': 18, 'D3': 19, 'E3': 20, 'F3': 21, 'G3': 22, 'H3': 23, 'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31, 'A4': 24, 'B4': 25, 'C4': 26, 'D4': 27, 'E4': 28, 'F4': 29, 'G4': 30, 'H4': 31, 'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39, 'A5': 32, 'B5': 33, 'C5': 34, 'D5': 35, 'E5': 36, 'F5': 37, 'G5': 38, 'H5': 39, 'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47, 'A6': 40, 'B6': 41, 'C6': 42, 'D6': 43, 'E6': 44, 'F6': 45, 'G6': 46, 'H6': 47, 'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55, 'A7': 48, 'B7': 49, 'C7': 50, 'D7': 51, 'E7': 52, 'F7': 53, 'G7': 54, 'H7': 55, 'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63, 'A8': 56, 'B8': 57, 'C8': 58, 'D8': 59, 'E8': 60, 'F8': 61, 'G8': 62, 'H8': 63, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23, '24': 24, '25': 25, '26': 26, '27': 27, '28': 28, '29': 29, '30': 30, '31': 31, '32': 32, '33': 33, '34': 34, '35': 35, '36': 36, '37': 37, '38': 38, '39': 39, '40': 40, '41': 41, '42': 42, '43': 43, '44': 44, '45': 45, '46': 46, '47': 47, '48': 48, '49': 49, '50': 50, '51': 51, '52': 52, '53': 53, '54': 54, '55': 55, '56': 56, '57': 57, '58': 58, '59': 59, '60': 60, '61': 61, '62': 62, '63': 63}
moves = []

def fill(current, opponent, direction):
    mask = MASKS[direction]
    w = mask(current) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    w |= mask(w) & opponent
    return (0b0|mask(w)) & (18446744073709551615 - (current|opponent))



def possible_moves(board, piece):
    final = 0b0
    for d in MASKS:
        final |= fill(board[piece], board[not piece], d)
    return {63-p for p in range(64) if is_on(final,p)}


def place(b, piece, move):
    board = b.copy()
    board[piece] |= move

    for i in MASKS:
        c = MASKS[i](move) & board[not piece]
        c |= MASKS[i](c)&board[not piece]
        c |= MASKS[i](c)&board[not piece]
        c |= MASKS[i](c)&board[not piece]
        c |= MASKS[i](c)&board[not piece]
        c |= MASKS[i](c)&board[not piece]
        if MASKS[i](c)&board[piece] != 0:
            board[piece] |= c
            board[not piece] &= bit_not(c)
    return board


def parse_args():
    global moves
    piece = ''
    board = '.'*27 + 'OX......XO'+'.'*27
    if len(argv) != 0:
        for arg in argv[1:]:
            if len(arg) == 64:
                board = arg.upper()
            elif arg.lower() == 'x' or arg.lower() == 'o':
                piece = arg.upper()
            else:
                moves.append(arg)
    if not piece:
        piece = 0 if board.count(".") % 2 != 0 else 1
    else:
       piece = 0 if piece == "O" else 1
    moves = [LETTERS[x] if x in LETTERS else int(x) for x in moves]
    board = {
        1: int(board.replace('.','0').replace('X','1').replace('O','0'), base=2),
        0: int(board.replace('.','0').replace('X','0').replace('O','1'), base=2)
    }
    return piece, board


def main():
    piece, board = parse_args()

    p = possible_moves(board, piece)
    s = binary_to_board(board)
    print("{0} {1}/{2}".format(s, s.count('x'), s.count('o')))
    s = [*s]
    for i in p:
        s[i] = '*'
    print_board(s)
    print("Possible moves for {0}: {1}".format('X' if piece else 'O', ", ".join([*map(str,[x for x in p])])))


    for move in moves:
        print("{0} moves to {1}".format('X' if piece else 'O', move))
        
        board = place(board, piece, 1<<(63-move))
        s = binary_to_board(board)
        print("{0} {1}/{2}".format(s, s.count('x'), s.count('o')))
        
        piece = not piece
        possible = possible_moves(board, piece)
        
        s = [*s]
        for i in possible:
            s[i] = '*'
        print_board(s)
        
        print("Possible moves for {0}: {1}".format('X' if piece else 'O', ", ".join([*map(str,[x for x in possible])])))

    return board # for debugging
    

if __name__ == "__main__":
    start = time() 
    main()
    print("{0}".format(time()-start))
