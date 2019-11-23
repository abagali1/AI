#!/usr/bin/env python3
from sys import argv
from time import process_time as time


size, dim, sub_pzl_row, sub_pzl_col = 81, 9, 3, 3  # global variables describing puzzle physical structure
constraint_table = {0: (0, 0, 0), 1: (0, 1, 0), 2: (0, 2, 0), 3: (0, 3, 1), 4: (0, 4, 1), 5: (0, 5, 1), 6: (0, 6, 2),
                    7: (0, 7, 2), 8: (0, 8, 2), 9: (1, 0, 0), 10: (1, 1, 0), 11: (1, 2, 0), 12: (1, 3, 1),
                    13: (1, 4, 1), 14: (1, 5, 1), 15: (1, 6, 2), 16: (1, 7, 2), 17: (1, 8, 2), 18: (2, 0, 0),
                    19: (2, 1, 0), 20: (2, 2, 0), 21: (2, 3, 1), 22: (2, 4, 1), 23: (2, 5, 1), 24: (2, 6, 2),
                    25: (2, 7, 2), 26: (2, 8, 2), 27: (3, 0, 3), 28: (3, 1, 3), 29: (3, 2, 3), 30: (3, 3, 4),
                    31: (3, 4, 4), 32: (3, 5, 4), 33: (3, 6, 5), 34: (3, 7, 5), 35: (3, 8, 5), 36: (4, 0, 3),
                    37: (4, 1, 3), 38: (4, 2, 3), 39: (4, 3, 4), 40: (4, 4, 4), 41: (4, 5, 4), 42: (4, 6, 5),
                    43: (4, 7, 5), 44: (4, 8, 5), 45: (5, 0, 3), 46: (5, 1, 3), 47: (5, 2, 3), 48: (5, 3, 4),
                    49: (5, 4, 4), 50: (5, 5, 4), 51: (5, 6, 5), 52: (5, 7, 5), 53: (5, 8, 5), 54: (6, 0, 6),
                    55: (6, 1, 6), 56: (6, 2, 6), 57: (6, 3, 7), 58: (6, 4, 7), 59: (6, 5, 7), 60: (6, 6, 8),
                    61: (6, 7, 8), 62: (6, 8, 8), 63: (7, 0, 6), 64: (7, 1, 6), 65: (7, 2, 6), 66: (7, 3, 7),
                    67: (7, 4, 7), 68: (7, 5, 7), 69: (7, 6, 8), 70: (7, 7, 8), 71: (7, 8, 8), 72: (8, 0, 6),
                    73: (8, 1, 6), 74: (8, 2, 6), 75: (8, 3, 7), 76: (8, 4, 7), 77: (8, 5, 7), 78: (8, 6, 8),
                    79: (8, 7, 8), 80: (8, 8, 8)}
rows = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16, 17], [18, 19, 20, 21, 22, 23, 24, 25, 26],
        [27, 28, 29, 30, 31, 32, 33, 34, 35], [36, 37, 38, 39, 40, 41, 42, 43, 44],
        [45, 46, 47, 48, 49, 50, 51, 52, 53], [54, 55, 56, 57, 58, 59, 60, 61, 62],
        [63, 64, 65, 66, 67, 68, 69, 70, 71], [72, 73, 74, 75, 76, 77, 78, 79, 80]]
cols = [[0, 9, 18, 27, 36, 45, 54, 63, 72], [1, 10, 19, 28, 37, 46, 55, 64, 73], [2, 11, 20, 29, 38, 47, 56, 65, 74],
        [3, 12, 21, 30, 39, 48, 57, 66, 75], [4, 13, 22, 31, 40, 49, 58, 67, 76], [5, 14, 23, 32, 41, 50, 59, 68, 77],
        [6, 15, 24, 33, 42, 51, 60, 69, 78], [7, 16, 25, 34, 43, 52, 61, 70, 79], [8, 17, 26, 35, 44, 53, 62, 71, 80]]
sub_pzls = [[0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23], [6, 7, 8, 15, 16, 17, 24, 25, 26],
            [27, 28, 29, 36, 37, 38, 45, 46, 47], [30, 31, 32, 39, 40, 41, 48, 49, 50],
            [33, 34, 35, 42, 43, 44, 51, 52, 53], [54, 55, 56, 63, 64, 65, 72, 73, 74],
            [57, 58, 59, 66, 67, 68, 75, 76, 77], [60, 61, 62, 69, 70, 71, 78, 79, 80]]
NEIGHBORS = {0: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 72, 18, 19, 20, 27, 36, 45, 54, 63},
             1: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 64, 73, 18, 19, 20, 28, 37, 46, 55},
             2: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 65, 74, 18, 19, 20, 29, 38, 47, 56},
             3: {0, 1, 2, 3, 4, 5, 6, 7, 8, 66, 75, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57},
             4: {0, 1, 2, 3, 4, 5, 6, 7, 8, 67, 12, 13, 14, 76, 21, 22, 23, 31, 40, 49, 58},
             5: {0, 1, 2, 3, 4, 5, 6, 7, 8, 68, 12, 13, 14, 77, 21, 22, 23, 32, 41, 50, 59},
             6: {0, 1, 2, 3, 4, 5, 6, 7, 8, 69, 78, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60},
             7: {0, 1, 2, 3, 4, 5, 6, 7, 8, 70, 15, 16, 17, 79, 24, 25, 26, 34, 43, 52, 61},
             8: {0, 1, 2, 3, 4, 5, 6, 7, 8, 71, 15, 16, 17, 80, 24, 25, 26, 35, 44, 53, 62},
             9: {0, 1, 2, 72, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 36, 45, 54, 63},
             10: {0, 1, 2, 64, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28, 37, 46, 73, 55},
             11: {0, 1, 2, 65, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 38, 47, 74, 56},
             12: {66, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 75, 21, 22, 23, 30, 39, 48, 57},
             13: {3, 4, 5, 67, 9, 10, 11, 12, 13, 14, 15, 16, 17, 76, 21, 22, 23, 31, 40, 49, 58},
             14: {3, 4, 5, 68, 9, 10, 11, 12, 13, 14, 15, 16, 17, 77, 21, 22, 23, 32, 41, 50, 59},
             15: {69, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 78, 24, 25, 26, 33, 42, 51, 60},
             16: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 79, 24, 25, 26, 70, 34, 43, 52, 61},
             17: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 80, 24, 25, 26, 35, 71, 44, 53, 62},
             18: {0, 1, 2, 72, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 45, 54, 63},
             19: {0, 1, 2, 64, 9, 10, 11, 73, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 37, 46, 55},
             20: {0, 1, 2, 65, 9, 10, 11, 74, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29, 38, 47, 56},
             21: {66, 3, 4, 5, 75, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 39, 48, 57},
             22: {3, 4, 5, 67, 12, 13, 14, 76, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 40, 49, 58},
             23: {3, 4, 5, 68, 12, 13, 14, 77, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 41, 50, 59},
             24: {69, 6, 7, 8, 78, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 33, 42, 51, 60},
             25: {6, 7, 8, 70, 79, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 34, 43, 52, 61},
             26: {6, 7, 8, 71, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 80, 35, 44, 53, 62},
             27: {0, 72, 9, 18, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 63},
             28: {64, 1, 73, 10, 19, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55},
             29: {65, 2, 74, 11, 20, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56},
             30: {66, 3, 75, 12, 21, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 57},
             31: {67, 4, 76, 13, 22, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 58},
             32: {68, 5, 77, 14, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 59},
             33: {69, 6, 78, 15, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 60},
             34: {70, 7, 79, 16, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 61},
             35: {71, 8, 80, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 62},
             36: {0, 72, 9, 18, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 54, 63},
             37: {64, 1, 73, 10, 19, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 55},
             38: {65, 2, 74, 11, 20, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 56},
             39: {66, 3, 75, 12, 21, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 57},
             40: {67, 4, 76, 13, 22, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 58},
             41: {68, 5, 77, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 59},
             42: {69, 6, 78, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 60},
             43: {70, 7, 79, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 61},
             44: {71, 8, 80, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 62},
             45: {0, 72, 9, 18, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 63},
             46: {64, 1, 73, 10, 19, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55},
             47: {65, 2, 74, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56},
             48: {66, 3, 75, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 57},
             49: {67, 4, 76, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 58},
             50: {68, 5, 77, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59},
             51: {69, 6, 78, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 60},
             52: {70, 7, 79, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 61},
             53: {71, 8, 80, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 62},
             54: {0, 64, 65, 72, 9, 73, 74, 18, 27, 36, 45, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63},
             55: {64, 1, 65, 72, 73, 10, 74, 19, 28, 37, 46, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63},
             56: {64, 65, 2, 72, 73, 74, 11, 20, 29, 38, 47, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63},
             57: {66, 3, 67, 68, 75, 12, 76, 77, 21, 30, 39, 48, 54, 55, 56, 57, 58, 59, 60, 61, 62},
             58: {66, 67, 4, 68, 75, 76, 13, 77, 22, 31, 40, 49, 54, 55, 56, 57, 58, 59, 60, 61, 62},
             59: {66, 67, 68, 5, 75, 76, 77, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 59, 60, 61, 62},
             60: {69, 6, 70, 71, 78, 15, 79, 80, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 60, 61, 62},
             61: {69, 70, 7, 71, 78, 79, 16, 80, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62},
             62: {69, 70, 71, 8, 78, 79, 80, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62},
             63: {0, 64, 65, 66, 67, 68, 69, 70, 71, 9, 72, 73, 74, 18, 27, 36, 45, 54, 55, 56, 63},
             64: {64, 1, 65, 66, 67, 68, 69, 70, 71, 72, 10, 73, 74, 19, 28, 37, 46, 54, 55, 56, 63},
             65: {64, 65, 2, 66, 67, 68, 69, 70, 71, 72, 73, 11, 74, 20, 29, 38, 47, 54, 55, 56, 63},
             66: {64, 65, 66, 3, 67, 68, 69, 70, 71, 75, 12, 76, 77, 21, 30, 39, 48, 57, 58, 59, 63},
             67: {64, 65, 66, 67, 4, 68, 69, 70, 71, 75, 76, 13, 77, 22, 31, 40, 49, 57, 58, 59, 63},
             68: {64, 65, 66, 67, 68, 5, 69, 70, 71, 75, 76, 77, 14, 23, 32, 41, 50, 57, 58, 59, 63},
             69: {64, 65, 66, 67, 68, 69, 6, 70, 71, 78, 15, 79, 80, 24, 33, 42, 51, 60, 61, 62, 63},
             70: {64, 65, 66, 67, 68, 69, 70, 7, 71, 78, 79, 16, 80, 25, 34, 43, 52, 60, 61, 62, 63},
             71: {64, 65, 66, 67, 68, 69, 70, 71, 8, 78, 79, 80, 17, 26, 35, 44, 53, 60, 61, 62, 63},
             72: {0, 64, 65, 72, 9, 73, 74, 75, 76, 77, 78, 79, 80, 18, 27, 36, 45, 54, 55, 56, 63},
             73: {64, 1, 65, 72, 73, 10, 74, 75, 76, 77, 78, 79, 80, 19, 28, 37, 46, 54, 55, 56, 63},
             74: {64, 65, 2, 72, 73, 74, 11, 75, 76, 77, 78, 79, 80, 20, 29, 38, 47, 54, 55, 56, 63},
             75: {66, 3, 67, 68, 72, 73, 74, 75, 12, 76, 77, 78, 79, 80, 21, 30, 39, 48, 57, 58, 59},
             76: {66, 67, 4, 68, 72, 73, 74, 75, 76, 13, 77, 78, 79, 80, 22, 31, 40, 49, 57, 58, 59},
             77: {66, 67, 68, 5, 72, 73, 74, 75, 76, 77, 14, 78, 79, 80, 23, 32, 41, 50, 57, 58, 59},
             78: {69, 6, 70, 71, 72, 73, 74, 75, 76, 77, 15, 78, 79, 80, 24, 33, 42, 51, 60, 61, 62},
             79: {69, 70, 7, 71, 72, 73, 74, 75, 76, 77, 78, 16, 79, 80, 25, 34, 43, 52, 60, 61, 62},
             80: {69, 70, 71, 8, 72, 73, 74, 75, 76, 77, 78, 79, 17, 80, 26, 35, 44, 53, 60, 61, 62}}
ALL_CONSTRAINTS = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16, 17],
                   [18, 19, 20, 21, 22, 23, 24, 25, 26], [27, 28, 29, 30, 31, 32, 33, 34, 35],
                   [36, 37, 38, 39, 40, 41, 42, 43, 44], [45, 46, 47, 48, 49, 50, 51, 52, 53],
                   [54, 55, 56, 57, 58, 59, 60, 61, 62], [63, 64, 65, 66, 67, 68, 69, 70, 71],
                   [72, 73, 74, 75, 76, 77, 78, 79, 80], [0, 9, 18, 27, 36, 45, 54, 63, 72],
                   [1, 10, 19, 28, 37, 46, 55, 64, 73], [2, 11, 20, 29, 38, 47, 56, 65, 74],
                   [3, 12, 21, 30, 39, 48, 57, 66, 75], [4, 13, 22, 31, 40, 49, 58, 67, 76],
                   [5, 14, 23, 32, 41, 50, 59, 68, 77], [6, 15, 24, 33, 42, 51, 60, 69, 78],
                   [7, 16, 25, 34, 43, 52, 61, 70, 79], [8, 17, 26, 35, 44, 53, 62, 71, 80],
                   [0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23],
                   [6, 7, 8, 15, 16, 17, 24, 25, 26], [27, 28, 29, 36, 37, 38, 45, 46, 47],
                   [30, 31, 32, 39, 40, 41, 48, 49, 50], [33, 34, 35, 42, 43, 44, 51, 52, 53],
                   [54, 55, 56, 63, 64, 65, 72, 73, 74], [57, 58, 59, 66, 67, 68, 75, 76, 77],
                   [60, 61, 62, 69, 70, 71, 78, 79, 80]]
DEL_TABLE= {('1'): {'5', '2', '3', '4', '6', '7', '8', '9'}, ('2', '1'): {'5', '3', '4', '6', '7', '8', '9'}, ('2', '1', '3'): {'5', '4', '6', '7', '8', '9'}, ('4', '2', '1', '3'): {'5', '6', '7', '8', '9'}, ('5', '2', '3', '1', '4'): {'6', '9', '8', '7'}, ('5', '2', '3', '1', '4', '6'): {'7', '9', '8'}, ('5', '2', '3', '1', '4', '6', '7'): {'9', '8'}, ('5', '2', '3', '1', '4', '6', '7', '8'): {'9'}}
{'1': {'5', '2', '3', '4', '6', '7', '8', '9'}, ('2', '1'): {'5', '3', '4', '6', '7', '8', '9'}, ('2', '1', '3'): {'5', '4', '6', '7', '8', '9'}, ('4', '2', '1', '3'): {'5', '6', '7', '8', '9'}, ('5', '2', '3', '1', '4'): {'6', '9', '8', '7'}, ('5', '2', '3', '1', '4', '6'): {'7', '9', '8'}, ('5', '2', '3', '1', '4', '6', '7'): {'9', '8'}, ('5', '2', '3', '1', '4', '6', '7', '8'): {'9'}}



def find_best_index(pzl: str) -> tuple:
    """
    Given a puzzle, find the index with the most amount of symbols able to be placed into that index
    @param: pzl Puzzle to find index for
    """
    max_pos = (-1, -1, set())
    for pos, elem in enumerate(pzl):
        if elem == '.':
            possibilities = set(pzl[j] for j in NEIGHBORS[pos] if pzl[j] != '.')
            length = len(possibilities)
            if length == 9:
                return None, None
            elif length == 8:
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
        for symbol in {'1', '2', '3', '4', '5', '6', '7', '8', '9'} - {pzl[i] for i in constraint if i != '.'}:
            valid_positions = {index for index in constraint if pzl[index] == '.' \
                               and symbol not in {pzl[i] for i in NEIGHBORS[index]}}
            length = len(valid_positions)
            if length == 0:
                return -1, -1
            elif length == 1 or length < len(possibilities):
                return symbol, valid_positions
    return None, None


def brute_force(pzl: str) -> str:
    """
    Given a puzzle, find its solution by judiciously placing symbols into every available position
    @param: pzl Puzzle to find solution for
    """
    if '.' not in pzl:
        return pzl  # This puzzle is solved

    index, c_s = find_best_index(pzl)  #
    if index is None:
        return ""
    set_of_choices = {'1', '2', '3', '4', '5', '6', '7', '8', '9'} - c_s  # If 2A is chosen
    symbol, positions = find_best_symbol(pzl, set_of_choices)  # 2B
    if symbol == -1 and positions == -1:
        return ""
        
    if symbol:
        set_of_choices = positions  # If 2B is chosen

    for choice in set_of_choices:
        b_f = brute_force(pzl[:choice] + symbol + pzl[choice + 1:] if symbol else pzl[:index] + choice + pzl[index + 1:])  # recur on new puzzle
        if b_f:
            return b_f  # return solution


if __name__ == '__main__':
    start = time()
    for pos, pzl in enumerate(open('puzzles.txt' if len(argv) <2 else argv[1]).read().splitlines()):
        sol = brute_force(pzl)
        print("Pzl {0}\n{1}\n{2}\n{3}".format(
            "{0}".format(pos + 1), pzl, sol, 405))
    print(f"{time()-start}")
