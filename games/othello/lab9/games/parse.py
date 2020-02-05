#!/usr/bin/env python3
from sys import argv

book = {}
GRADER_MOVES = {11: 0, 12: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6, 18: 7, 21: 8, 22: 9, 23: 10, 24: 11, 25: 12, 26: 13, 27: 14, 28: 15, 31: 16, 32: 17, 33: 18, 34: 19, 35: 20, 36: 21, 37: 22, 38: 23, 41: 24, 42: 25, 43: 26, 44: 27, 45: 28, 46: 29, 47: 30, 48: 31, 51: 32, 52: 33, 53: 34, 54: 35, 55: 36, 56: 37, 57: 38, 58: 39, 61: 40, 62: 41, 63: 42, 64: 43, 65: 44, 66: 45, 67: 46, 68: 47, 71: 48, 72: 49, 73: 50, 74: 51, 75: 52, 76: 53, 77: 54, 78: 55, 81: 56, 82: 57, 83: 58, 84: 59, 85: 60, 86: 61, 87: 62, 88: 63}

PIECES = {
'@':1,
'O':0,
'o':0
}


def string_to_bitboard(board):
  b = board.replace("?","").replace(".","0").upper()
  return (hex(int(b.replace("O","1").replace("@","0"),2)), hex(int(b.replace("O","0").replace("@","1"),2)))


def parse(game, piece):
  for pos, line in enumerate(game):
    parts = line.split(" ")
    token = parts[1]
    if token != piece:
      continue
    board = string_to_bitboard(parts[0])
    move = game[pos+1].split(" ")[-1]
    if move == '-':
      break
    book[(*board, PIECES[piece])] = GRADER_MOVES[int(move)]



game = open("games/black.txt").read().splitlines()
parse(game, '@')
game = open("games/white.txt").read().splitlines()
parse(game, 'o')


print(book)
