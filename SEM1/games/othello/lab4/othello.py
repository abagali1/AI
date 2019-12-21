#!/usr/bin/env python3
from sys import argv
from re import compile, IGNORECASE, finditer

INDICES_2D = {(i,j):i*8 +j for i in range(8) for j in range(8)}
INDICES = {i: (i//8, i%8) for i in range(0,64)}
LETTERS = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7, 'A1': 0, 'B1': 1, 'C1': 2, 'D1': 3, 'E1': 4, 'F1': 5, 'G1': 6, 'H1': 7, 'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15, 'A2': 8, 'B2': 9, 'C2': 10, 'D2': 11, 'E2': 12, 'F2': 13, 'G2': 14, 'H2': 15, 'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23, 'A3': 16, 'B3': 17, 'C3': 18, 'D3': 19, 'E3': 20, 'F3': 21, 'G3': 22, 'H3': 23, 'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31, 'A4': 24, 'B4': 25, 'C4': 26, 'D4': 27, 'E4': 28, 'F4': 29, 'G4': 30, 'H4': 31, 'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39, 'A5': 32, 'B5': 33, 'C5': 34, 'D5': 35, 'E5': 36, 'F5': 37, 'G5': 38, 'H5': 39, 'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47, 'A6': 40, 'B6': 41, 'C6': 42, 'D6': 43, 'E6': 44, 'F6': 45, 'G6': 46, 'H6': 47, 'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55, 'A7': 48, 'B7': 49, 'C7': 50, 'D7': 51, 'E7': 52, 'F7': 53, 'G7': 54, 'H7': 55, 'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63, 'A8': 56, 'B8': 57, 'C8': 58, 'D8': 59, 'E8': 60, 'F8': 61, 'G8': 62, 'H8': 63, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '21': 21, '22': 22, '23': 23, '24': 24, '25': 25, '26': 26, '27': 27, '28': 28, '29': 29, '30': 30, '31': 31, '32': 32, '33': 33, '34': 34, '35': 35, '36': 36, '37': 37, '38': 38, '39': 39, '40': 40, '41': 41, '42': 42, '43': 43, '44': 44, '45': 45, '46': 46, '47': 47, '48': 48, '49': 49, '50': 50, '51': 51, '52': 52, '53': 53, '54': 54, '55': 55, '56': 56, '57': 57, '58': 58, '59': 59, '60': 60, '61': 61, '62': 62, '63': 63}
REGEX = {
    "X": {
        0: compile(r"xo+\.", IGNORECASE),
        1: compile(r"\.o+x", IGNORECASE)
    },
    "O": {
        0: compile(r"ox+\.", IGNORECASE),
        1: compile(r"\.x+o", IGNORECASE)
    }
}
CONSTRAINTS = {0: ([0, 1, 2, 3, 4, 5, 6, 7], [0, 8, 16, 24, 32, 40, 48, 56], [0, 9, 18, 27, 36, 45, 54, 63], [0]), 1: ([0, 1, 2, 3, 4, 5, 6, 7], [1, 9, 17, 25, 33, 41, 49, 57], [1, 10, 19, 28, 37, 46, 55], [1, 8]), 2: ([0, 1, 2, 3, 4, 5, 6, 7], [2, 10, 18, 26, 34, 42, 50, 58], [2, 11, 20, 29, 38, 47], [2, 9, 16]), 3: ([0, 1, 2, 3, 4, 5, 6, 7], [3, 11, 19, 27, 35, 43, 51, 59], [3, 12, 21, 30, 39], [3, 10, 17, 24]), 4: ([0, 1, 2, 3, 4, 5, 6, 7], [4, 12, 20, 28, 36, 44, 52, 60], [4, 13, 22, 31], [4, 11, 18, 25, 32]), 5: ([0, 1, 2, 3, 4, 5, 6, 7], [5, 13, 21, 29, 37, 45, 53, 61], [5, 14, 23], [5, 12, 19, 26, 33, 40]), 6: ([0, 1, 2, 3, 4, 5, 6, 7], [6, 14, 22, 30, 38, 46, 54, 62], [6, 15], [6, 13, 20, 27, 34, 41, 48]), 7: ([0, 1, 2, 3, 4, 5, 6, 7], [7, 15, 23, 31, 39, 47, 55, 63], [7], [7, 14, 21, 28, 35, 42, 49, 56]), 8: ([8, 9, 10, 11, 12, 13, 14, 15], [0, 8, 16, 24, 32, 40, 48, 56], [8, 17, 26, 35, 44, 53, 62], [1, 8]), 9: ([8, 9, 10, 11, 12, 13, 14, 15], [1, 9, 17, 25, 33, 41, 49, 57], [0, 9, 18, 27, 36, 45, 54, 63], [2, 9, 16]), 10: ([8, 9, 10, 11, 12, 13, 14, 15], [2, 10, 18, 26, 34, 42, 50, 58], [1, 10, 19, 28, 37, 46, 55], [3, 10, 17, 24]), 11: ([8, 9, 10, 11, 12, 13, 14, 15], [3, 11, 19, 27, 35, 43, 51, 59], [2, 11, 20, 29, 38, 47], [4, 11, 18, 25, 32]), 12: ([8, 9, 10, 11, 12, 13, 14, 15], [4, 12, 20, 28, 36, 44, 52, 60], [3, 12, 21, 30, 39], [5, 12, 19, 26, 33, 40]), 13: ([8, 9, 10, 11, 12, 13, 14, 15], [5, 13, 21, 29, 37, 45, 53, 61], [4, 13, 22, 31], [6, 13, 20, 27, 34, 41, 48]), 14: ([8, 9, 10, 11, 12, 13, 14, 15], [6, 14, 22, 30, 38, 46, 54, 62], [5, 14, 23], [7, 14, 21, 28, 35, 42, 49, 56]), 15: ([8, 9, 10, 11, 12, 13, 14, 15], [7, 15, 23, 31, 39, 47, 55, 63], [6, 15], [15, 22, 29, 36, 43, 50, 57]), 16: ([16, 17, 18, 19, 20, 21, 22, 23], [0, 8, 16, 24, 32, 40, 48, 56], [16, 25, 34, 43, 52, 61], [2, 9, 16]), 17: ([16, 17, 18, 19, 20, 21, 22, 23], [1, 9, 17, 25, 33, 41, 49, 57], [8, 17, 26, 35, 44, 53, 62], [3, 10, 17, 24]), 18: ([16, 17, 18, 19, 20, 21, 22, 23], [2, 10, 18, 26, 34, 42, 50, 58], [0, 9, 18, 27, 36, 45, 54, 63], [4, 11, 18, 25, 32]), 19: ([16, 17, 18, 19, 20, 21, 22, 23], [3, 11, 19, 27, 35, 43, 51, 59], [1, 10, 19, 28, 37, 46, 55], [5, 12, 19, 26, 33, 40]), 20: ([16, 17, 18, 19, 20, 21, 22, 23], [4, 12, 20, 28, 36, 44, 52, 60], [2, 11, 20, 29, 38, 47], [6, 13, 20, 27, 34, 41, 48]), 21: ([16, 17, 18, 19, 20, 21, 22, 23], [5, 13, 21, 29, 37, 45, 53, 61], [3, 12, 21, 30, 39], [7, 14, 21, 28, 35, 42, 49, 56]), 22: ([16, 17, 18, 19, 20, 21, 22, 23], [6, 14, 22, 30, 38, 46, 54, 62], [4, 13, 22, 31], [15, 22, 29, 36, 43, 50, 57]), 23: ([16, 17, 18, 19, 20, 21, 22, 23], [7, 15, 23, 31, 39, 47, 55, 63], [5, 14, 23], [23, 30, 37, 44, 51, 58]), 24: ([24, 25, 26, 27, 28, 29, 30, 31], [0, 8, 16, 24, 32, 40, 48, 56], [24, 33, 42, 51, 60], [3, 10, 17, 24]), 25: ([24, 25, 26, 27, 28, 29, 30, 31], [1, 9, 17, 25, 33, 41, 49, 57], [16, 25, 34, 43, 52, 61], [4, 11, 18, 25, 32]), 26: ([24, 25, 26, 27, 28, 29, 30, 31], [2, 10, 18, 26, 34, 42, 50, 58], [8, 17, 26, 35, 44, 53, 62], [5, 12, 19, 26, 33, 40]), 27: ([24, 25, 26, 27, 28, 29, 30, 31], [3, 11, 19, 27, 35, 43, 51, 59], [0, 9, 18, 27, 36, 45, 54, 63], [6, 13, 20, 27, 34, 41, 48]), 28: ([24, 25, 26, 27, 28, 29, 30, 31], [4, 12, 20, 28, 36, 44, 52, 60], [1, 10, 19, 28, 37, 46, 55], [7, 14, 21, 28, 35, 42, 49, 56]), 29: ([24, 25, 26, 27, 28, 29, 30, 31], [5, 13, 21, 29, 37, 45, 53, 61], [2, 11, 20, 29, 38, 47], [15, 22, 29, 36, 43, 50, 57]), 30: ([24, 25, 26, 27, 28, 29, 30, 31], [6, 14, 22, 30, 38, 46, 54, 62], [3, 12, 21, 30, 39], [23, 30, 37, 44, 51, 58]), 31: ([24, 25, 26, 27, 28, 29, 30, 31], [7, 15, 23, 31, 39, 47, 55, 63], [4, 13, 22, 31], [31, 38, 45, 52, 59]), 32: ([32, 33, 34, 35, 36, 37, 38, 39], [0, 8, 16, 24, 32, 40, 48, 56], [32, 41, 50, 59], [4, 11, 18, 25, 32]), 33: ([32, 33, 34, 35, 36, 37, 38, 39], [1, 9, 17, 25, 33, 41, 49, 57], [24, 33, 42, 51, 60], [5, 12, 19, 26, 33, 40]), 34: ([32, 33, 34, 35, 36, 37, 38, 39], [2, 10, 18, 26, 34, 42, 50, 58], [16, 25, 34, 43, 52, 61], [6, 13, 20, 27, 34, 41, 48]), 35: ([32, 33, 34, 35, 36, 37, 38, 39], [3, 11, 19, 27, 35, 43, 51, 59], [8, 17, 26, 35, 44, 53, 62], [7, 14, 21, 28, 35, 42, 49, 56]), 36: ([32, 33, 34, 35, 36, 37, 38, 39], [4, 12, 20, 28, 36, 44, 52, 60], [0, 9, 18, 27, 36, 45, 54, 63], [15, 22, 29, 36, 43, 50, 57]), 37: ([32, 33, 34, 35, 36, 37, 38, 39], [5, 13, 21, 29, 37, 45, 53, 61], [1, 10, 19, 28, 37, 46, 55], [23, 30, 37, 44, 51, 58]), 38: ([32, 33, 34, 35, 36, 37, 38, 39], [6, 14, 22, 30, 38, 46, 54, 62], [2, 11, 20, 29, 38, 47], [31, 38, 45, 52, 59]), 39: ([32, 33, 34, 35, 36, 37, 38, 39], [7, 15, 23, 31, 39, 47, 55, 63], [3, 12, 21, 30, 39], [39, 46, 53, 60]), 40: ([40, 41, 42, 43, 44, 45, 46, 47], [0, 8, 16, 24, 32, 40, 48, 56], [40, 49, 58], [5, 12, 19, 26, 33, 40]), 41: ([40, 41, 42, 43, 44, 45, 46, 47], [1, 9, 17, 25, 33, 41, 49, 57], [32, 41, 50, 59], [6, 13, 20, 27, 34, 41, 48]), 42: ([40, 41, 42, 43, 44, 45, 46, 47], [2, 10, 18, 26, 34, 42, 50, 58], [24, 33, 42, 51, 60], [7, 14, 21, 28, 35, 42, 49, 56]), 43: ([40, 41, 42, 43, 44, 45, 46, 47], [3, 11, 19, 27, 35, 43, 51, 59], [16, 25, 34, 43, 52, 61], [15, 22, 29, 36, 43, 50, 57]), 44: ([40, 41, 42, 43, 44, 45, 46, 47], [4, 12, 20, 28, 36, 44, 52, 60], [8, 17, 26, 35, 44, 53, 62], [23, 30, 37, 44, 51, 58]), 45: ([40, 41, 42, 43, 44, 45, 46, 47], [5, 13, 21, 29, 37, 45, 53, 61], [0, 9, 18, 27, 36, 45, 54, 63], [31, 38, 45, 52, 59]), 46: ([40, 41, 42, 43, 44, 45, 46, 47], [6, 14, 22, 30, 38, 46, 54, 62], [1, 10, 19, 28, 37, 46, 55], [39, 46, 53, 60]), 47: ([40, 41, 42, 43, 44, 45, 46, 47], [7, 15, 23, 31, 39, 47, 55, 63], [2, 11, 20, 29, 38, 47], [47, 54, 61]), 48: ([48, 49, 50, 51, 52, 53, 54, 55], [0, 8, 16, 24, 32, 40, 48, 56], [48, 57], [6, 13, 20, 27, 34, 41, 48]), 49: ([48, 49, 50, 51, 52, 53, 54, 55], [1, 9, 17, 25, 33, 41, 49, 57], [40, 49, 58], [7, 14, 21, 28, 35, 42, 49, 56]), 50: ([48, 49, 50, 51, 52, 53, 54, 55], [2, 10, 18, 26, 34, 42, 50, 58], [32, 41, 50, 59], [15, 22, 29, 36, 43, 50, 57]), 51: ([48, 49, 50, 51, 52, 53, 54, 55], [3, 11, 19, 27, 35, 43, 51, 59], [24, 33, 42, 51, 60], [23, 30, 37, 44, 51, 58]), 52: ([48, 49, 50, 51, 52, 53, 54, 55], [4, 12, 20, 28, 36, 44, 52, 60], [16, 25, 34, 43, 52, 61], [31, 38, 45, 52, 59]), 53: ([48, 49, 50, 51, 52, 53, 54, 55], [5, 13, 21, 29, 37, 45, 53, 61], [8, 17, 26, 35, 44, 53, 62], [39, 46, 53, 60]), 54: ([48, 49, 50, 51, 52, 53, 54, 55], [6, 14, 22, 30, 38, 46, 54, 62], [0, 9, 18, 27, 36, 45, 54, 63], [47, 54, 61]), 55: ([48, 49, 50, 51, 52, 53, 54, 55], [7, 15, 23, 31, 39, 47, 55, 63], [1, 10, 19, 28, 37, 46, 55], [55, 62]), 56: ([56, 57, 58, 59, 60, 61, 62, 63], [0, 8, 16, 24, 32, 40, 48, 56], [56], [7, 14, 21, 28, 35, 42, 49, 56]), 57: ([56, 57, 58, 59, 60, 61, 62, 63], [1, 9, 17, 25, 33, 41, 49, 57], [48, 57], [15, 22, 29, 36, 43, 50, 57]), 58: ([56, 57, 58, 59, 60, 61, 62, 63], [2, 10, 18, 26, 34, 42, 50, 58], [40, 49, 58], [23, 30, 37, 44, 51, 58]), 59: ([56, 57, 58, 59, 60, 61, 62, 63], [3, 11, 19, 27, 35, 43, 51, 59], [32, 41, 50, 59], [31, 38, 45, 52, 59]), 60: ([56, 57, 58, 59, 60, 61, 62, 63], [4, 12, 20, 28, 36, 44, 52, 60], [24, 33, 42, 51, 60], [39, 46, 53, 60]), 61: ([56, 57, 58, 59, 60, 61, 62, 63], [5, 13, 21, 29, 37, 45, 53, 61], [16, 25, 34, 43, 52, 61], [47, 54, 61]), 62: ([56, 57, 58, 59, 60, 61, 62, 63], [6, 14, 22, 30, 38, 46, 54, 62], [8, 17, 26, 35, 44, 53, 62], [55, 62]), 63: ([56, 57, 58, 59, 60, 61, 62, 63], [7, 15, 23, 31, 39, 47, 55, 63], [0, 9, 18, 27, 36, 45, 54, 63], [63])}
ALL_CONSTRAINTS = [[0, 1, 2, 3, 4, 5, 6, 7], [0, 8, 16, 24, 32, 40, 48, 56], [0, 9, 18, 27, 36, 45, 54, 63], [0], [0, 1, 2, 3, 4, 5, 6, 7], [1, 9, 17, 25, 33, 41, 49, 57], [1, 10, 19, 28, 37, 46, 55], [1, 8], [0, 1, 2, 3, 4, 5, 6, 7], [2, 10, 18, 26, 34, 42, 50, 58], [2, 11, 20, 29, 38, 47], [2, 9, 16], [0, 1, 2, 3, 4, 5, 6, 7], [3, 11, 19, 27, 35, 43, 51, 59], [3, 12, 21, 30, 39], [3, 10, 17, 24], [0, 1, 2, 3, 4, 5, 6, 7], [4, 12, 20, 28, 36, 44, 52, 60], [4, 13, 22, 31], [4, 11, 18, 25, 32], [0, 1, 2, 3, 4, 5, 6, 7], [5, 13, 21, 29, 37, 45, 53, 61], [5, 14, 23], [5, 12, 19, 26, 33, 40], [0, 1, 2, 3, 4, 5, 6, 7], [6, 14, 22, 30, 38, 46, 54, 62], [6, 15], [6, 13, 20, 27, 34, 41, 48], [0, 1, 2, 3, 4, 5, 6, 7], [7, 15, 23, 31, 39, 47, 55, 63], [7], [7, 14, 21, 28, 35, 42, 49, 56], [8, 9, 10, 11, 12, 13, 14, 15], [0, 8, 16, 24, 32, 40, 48, 56], [8, 17, 26, 35, 44, 53, 62], [1, 8], [8, 9, 10, 11, 12, 13, 14, 15], [1, 9, 17, 25, 33, 41, 49, 57], [0, 9, 18, 27, 36, 45, 54, 63], [2, 9, 16], [8, 9, 10, 11, 12, 13, 14, 15], [2, 10, 18, 26, 34, 42, 50, 58], [1, 10, 19, 28, 37, 46, 55], [3, 10, 17, 24], [8, 9, 10, 11, 12, 13, 14, 15], [3, 11, 19, 27, 35, 43, 51, 59], [2, 11, 20, 29, 38, 47], [4, 11, 18, 25, 32], [8, 9, 10, 11, 12, 13, 14, 15], [4, 12, 20, 28, 36, 44, 52, 60], [3, 12, 21, 30, 39], [5, 12, 19, 26, 33, 40], [8, 9, 10, 11, 12, 13, 14, 15], [5, 13, 21, 29, 37, 45, 53, 61], [4, 13, 22, 31], [6, 13, 20, 27, 34, 41, 48], [8, 9, 10, 11, 12, 13, 14, 15], [6, 14, 22, 30, 38, 46, 54, 62], [5, 14, 23], [7, 14, 21, 28, 35, 42, 49, 56], [8, 9, 10, 11, 12, 13, 14, 15], [7, 15, 23, 31, 39, 47, 55, 63], [6, 15], [15, 22, 29, 36, 43, 50, 57], [16, 17, 18, 19, 20, 21, 22, 23], [0, 8, 16, 24, 32, 40, 48, 56], [16, 25, 34, 43, 52, 61], [2, 9, 16], [16, 17, 18, 19, 20, 21, 22, 23], [1, 9, 17, 25, 33, 41, 49, 57], [8, 17, 26, 35, 44, 53, 62], [3, 10, 17, 24], [16, 17, 18, 19, 20, 21, 22, 23], [2, 10, 18, 26, 34, 42, 50, 58], [0, 9, 18, 27, 36, 45, 54, 63], [4, 11, 18, 25, 32], [16, 17, 18, 19, 20, 21, 22, 23], [3, 11, 19, 27, 35, 43, 51, 59], [1, 10, 19, 28, 37, 46, 55], [5, 12, 19, 26, 33, 40], [16, 17, 18, 19, 20, 21, 22, 23], [4, 12, 20, 28, 36, 44, 52, 60], [2, 11, 20, 29, 38, 47], [6, 13, 20, 27, 34, 41, 48], [16, 17, 18, 19, 20, 21, 22, 23], [5, 13, 21, 29, 37, 45, 53, 61], [3, 12, 21, 30, 39], [7, 14, 21, 28, 35, 42, 49, 56], [16, 17, 18, 19, 20, 21, 22, 23], [6, 14, 22, 30, 38, 46, 54, 62], [4, 13, 22, 31], [15, 22, 29, 36, 43, 50, 57], [16, 17, 18, 19, 20, 21, 22, 23], [7, 15, 23, 31, 39, 47, 55, 63], [5, 14, 23], [23, 30, 37, 44, 51, 58], [24, 25, 26, 27, 28, 29, 30, 31], [0, 8, 16, 24, 32, 40, 48, 56], [24, 33, 42, 51, 60], [3, 10, 17, 24], [24, 25, 26, 27, 28, 29, 30, 31], [1, 9, 17, 25, 33, 41, 49, 57], [16, 25, 34, 43, 52, 61], [4, 11, 18, 25, 32], [24, 25, 26, 27, 28, 29, 30, 31], [2, 10, 18, 26, 34, 42, 50, 58], [8, 17, 26, 35, 44, 53, 62], [5, 12, 19, 26, 33, 40], [24, 25, 26, 27, 28, 29, 30, 31], [3, 11, 19, 27, 35, 43, 51, 59], [0, 9, 18, 27, 36, 45, 54, 63], [6, 13, 20, 27, 34, 41, 48], [24, 25, 26, 27, 28, 29, 30, 31], [4, 12, 20, 28, 36, 44, 52, 60], [1, 10, 19, 28, 37, 46, 55], [7, 14, 21, 28, 35, 42, 49, 56], [24, 25, 26, 27, 28, 29, 30, 31], [5, 13, 21, 29, 37, 45, 53, 61], [2, 11, 20, 29, 38, 47], [15, 22, 29, 36, 43, 50, 57], [24, 25, 26, 27, 28, 29, 30, 31], [6, 14, 22, 30, 38, 46, 54, 62], [3, 12, 21, 30, 39], [23, 30, 37, 44, 51, 58], [24, 25, 26, 27, 28, 29, 30, 31], [7, 15, 23, 31, 39, 47, 55, 63], [4, 13, 22, 31], [31, 38, 45, 52, 59], [32, 33, 34, 35, 36, 37, 38, 39], [0, 8, 16, 24, 32, 40, 48, 56], [32, 41, 50, 59], [4, 11, 18, 25, 32], [32, 33, 34, 35, 36, 37, 38, 39], [1, 9, 17, 25, 33, 41, 49, 57], [24, 33, 42, 51, 60], [5, 12, 19, 26, 33, 40], [32, 33, 34, 35, 36, 37, 38, 39], [2, 10, 18, 26, 34, 42, 50, 58], [16, 25, 34, 43, 52, 61], [6, 13, 20, 27, 34, 41, 48], [32, 33, 34, 35, 36, 37, 38, 39], [3, 11, 19, 27, 35, 43, 51, 59], [8, 17, 26, 35, 44, 53, 62], [7, 14, 21, 28, 35, 42, 49, 56], [32, 33, 34, 35, 36, 37, 38, 39], [4, 12, 20, 28, 36, 44, 52, 60], [0, 9, 18, 27, 36, 45, 54, 63], [15, 22, 29, 36, 43, 50, 57], [32, 33, 34, 35, 36, 37, 38, 39], [5, 13, 21, 29, 37, 45, 53, 61], [1, 10, 19, 28, 37, 46, 55], [23, 30, 37, 44, 51, 58], [32, 33, 34, 35, 36, 37, 38, 39], [6, 14, 22, 30, 38, 46, 54, 62], [2, 11, 20, 29, 38, 47], [31, 38, 45, 52, 59], [32, 33, 34, 35, 36, 37, 38, 39], [7, 15, 23, 31, 39, 47, 55, 63], [3, 12, 21, 30, 39], [39, 46, 53, 60], [40, 41, 42, 43, 44, 45, 46, 47], [0, 8, 16, 24, 32, 40, 48, 56], [40, 49, 58], [5, 12, 19, 26, 33, 40], [40, 41, 42, 43, 44, 45, 46, 47], [1, 9, 17, 25, 33, 41, 49, 57], [32, 41, 50, 59], [6, 13, 20, 27, 34, 41, 48], [40, 41, 42, 43, 44, 45, 46, 47], [2, 10, 18, 26, 34, 42, 50, 58], [24, 33, 42, 51, 60], [7, 14, 21, 28, 35, 42, 49, 56], [40, 41, 42, 43, 44, 45, 46, 47], [3, 11, 19, 27, 35, 43, 51, 59], [16, 25, 34, 43, 52, 61], [15, 22, 29, 36, 43, 50, 57], [40, 41, 42, 43, 44, 45, 46, 47], [4, 12, 20, 28, 36, 44, 52, 60], [8, 17, 26, 35, 44, 53, 62], [23, 30, 37, 44, 51, 58], [40, 41, 42, 43, 44, 45, 46, 47], [5, 13, 21, 29, 37, 45, 53, 61], [0, 9, 18, 27, 36, 45, 54, 63], [31, 38, 45, 52, 59], [40, 41, 42, 43, 44, 45, 46, 47], [6, 14, 22, 30, 38, 46, 54, 62], [1, 10, 19, 28, 37, 46, 55], [39, 46, 53, 60], [40, 41, 42, 43, 44, 45, 46, 47], [7, 15, 23, 31, 39, 47, 55, 63], [2, 11, 20, 29, 38, 47], [47, 54, 61], [48, 49, 50, 51, 52, 53, 54, 55], [0, 8, 16, 24, 32, 40, 48, 56], [48, 57], [6, 13, 20, 27, 34, 41, 48], [48, 49, 50, 51, 52, 53, 54, 55], [1, 9, 17, 25, 33, 41, 49, 57], [40, 49, 58], [7, 14, 21, 28, 35, 42, 49, 56], [48, 49, 50, 51, 52, 53, 54, 55], [2, 10, 18, 26, 34, 42, 50, 58], [32, 41, 50, 59], [15, 22, 29, 36, 43, 50, 57], [48, 49, 50, 51, 52, 53, 54, 55], [3, 11, 19, 27, 35, 43, 51, 59], [24, 33, 42, 51, 60], [23, 30, 37, 44, 51, 58], [48, 49, 50, 51, 52, 53, 54, 55], [4, 12, 20, 28, 36, 44, 52, 60], [16, 25, 34, 43, 52, 61], [31, 38, 45, 52, 59], [48, 49, 50, 51, 52, 53, 54, 55], [5, 13, 21, 29, 37, 45, 53, 61], [8, 17, 26, 35, 44, 53, 62], [39, 46, 53, 60], [48, 49, 50, 51, 52, 53, 54, 55], [6, 14, 22, 30, 38, 46, 54, 62], [0, 9, 18, 27, 36, 45, 54, 63], [47, 54, 61], [48, 49, 50, 51, 52, 53, 54, 55], [7, 15, 23, 31, 39, 47, 55, 63], [1, 10, 19, 28, 37, 46, 55], [55, 62], [56, 57, 58, 59, 60, 61, 62, 63], [0, 8, 16, 24, 32, 40, 48, 56], [56], [7, 14, 21, 28, 35, 42, 49, 56], [56, 57, 58, 59, 60, 61, 62, 63], [1, 9, 17, 25, 33, 41, 49, 57], [48, 57], [15, 22, 29, 36, 43, 50, 57], [56, 57, 58, 59, 60, 61, 62, 63], [2, 10, 18, 26, 34, 42, 50, 58], [40, 49, 58], [23, 30, 37, 44, 51, 58], [56, 57, 58, 59, 60, 61, 62, 63], [3, 11, 19, 27, 35, 43, 51, 59], [32, 41, 50, 59], [31, 38, 45, 52, 59], [56, 57, 58, 59, 60, 61, 62, 63], [4, 12, 20, 28, 36, 44, 52, 60], [24, 33, 42, 51, 60], [39, 46, 53, 60], [56, 57, 58, 59, 60, 61, 62, 63], [5, 13, 21, 29, 37, 45, 53, 61], [16, 25, 34, 43, 52, 61], [47, 54, 61], [56, 57, 58, 59, 60, 61, 62, 63], [6, 14, 22, 30, 38, 46, 54, 62], [8, 17, 26, 35, 44, 53, 62], [55, 62], [56, 57, 58, 59, 60, 61, 62, 63], [7, 15, 23, 31, 39, 47, 55, 63], [0, 9, 18, 27, 36, 45, 54, 63], [63]]
moves = []


def possible_moves(pzl, piece):
    possible = []
    p = {}
    for constraint in ALL_CONSTRAINTS:
        con = "".join(pzl[x] for x in constraint)
        if piece not in con:
            continue
        possible += [(constraint[x.end()-1],[constraint[i] for i in range(x.span()[0], x.span()[1])]) for x in finditer(REGEX[piece][0], con) if pzl[constraint[x.end()-1]] == '.']
        possible += [(constraint[x.start()],[constraint[i] for i in range(x.span()[0], x.span()[1])]) for x in finditer(REGEX[piece][1], con) if pzl[constraint[x.start()]] == '.']
    for i in possible:
        if i[0] in p:
            p[i[0]].update(i[1])
        else:
            p[i[0]] = {*i[1]}
    return p


def parse_args():
    global moves
    piece = ''
    board = [*'.'*27 + 'OX......XO'+'.'*27]
    if len(argv) != 1:
        for arg in argv[1:]:
            if len(arg) == 64:
                board = [*arg.upper()]
            elif arg.lower() == 'x' or arg.lower() == 'o':
                piece = arg.upper()
            else:
                moves.append(arg)
    if not piece:
        piece = "O" if board.count(".") % 2 != 0 else "X"
    moves = [LETTERS[x] if x in LETTERS else int(x) for x in moves]
    return piece,board


def to_string(pzl):
    return '\n'.join(
        [''.join([pzl[INDICES_2D[(i, j)]][0] for j in range(8)]) for i in range(8)]).strip().lower()


def place(pzl, piece, index):
    for i in index: 
        pzl[i] = piece
    return pzl

def main():
    piece, board = parse_args()

    print("{0} {1}/{2}\n".format("".join(board).lower(), board.count("X"), board.count("O")))
    possible = possible_moves(board, piece)
    
    if len(possible) == 0:
        piece = "X" if piece == "O" else "O"
        possible = possible_moves(board, piece)
    for i in possible:
        board[i] = '*'
    print(to_string(board))
    for i in possible:
        board[i] = '.'
    print("Possible moves for {0}: {1}\n".format(piece, ", ".join(list(map(str,[x for x in possible])))))

    for move in moves:
        if move < 0:
            continue
        print("{0} moves to {1}".format(piece, move))
        board = place(board, piece, possible[move])
        print("{0} {1}/{2}\n".format("".join(board).lower(), board.count("X"), board.count("O")))
        piece = "X" if piece == "O" else "O"
        possible = possible_moves(board, piece)
        if len(possible) != 0:
            for i in possible:
                board[i] = '*'
            print(to_string(board))
            for i in possible:
                board[i] = '.'
            print("Possible moves for {0}: {1}\n".format(piece, ", ".join(list(map(str,[x for x in possible])))))
        else:
            piece = "X" if piece == "O" else "O"
            possible = possible_moves(board, piece)
            for i in possible:
                board[i] = '*'
            print(to_string(board))
            for i in possible:
                board[i] = '.'
            print("Possible moves for {0}: {1}\n".format(piece, ", ".join(list(map(str,[x for x in possible])))))




if __name__ == "__main__":
    main()
