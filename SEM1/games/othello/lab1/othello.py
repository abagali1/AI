#!/usr/bin/env python3
from sys import argv

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}

class Othello:
    def __init__(self, board, starting_piece):
        self.board = [*board]
        self.width = self.height = 8
        self.gamepiece = starting_piece.upper()
        self.black = self.white = 0

    def __str__(self):
        return self.to_string(self.board)

    def to_string(self, board):
        return '\n'.join(
            [''.join([board[i*self.width +j][0] for j in range(self.width)]) for i in range(self.height)]).strip()

    def move(self, index):
        self.board[index] = self.gamepiece
        if self.gamepiece == 'O':
            self.white += 1
        else:
            self.black += 1
        self.gamepiece = 'O' if self.gamepiece == 'X' else 'O'

    def possible_moves(self):
        return to_string(self.board)

def main():
    piece = "X"
    board = '.'*27 + 'OX......XO'+'.'*27
    moves = [19, 31, 41]


if __name__ == "__main__":
    print(main())