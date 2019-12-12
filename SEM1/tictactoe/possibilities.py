#!/usr/bin/env python3
from sys import argv
WIN, HEIGHT, WIDTH = 0, 0, 0
X = 'X'
O = 'O'
SPACE = '.'


def finished(pzl):
    if pzl.find(SPACE) == -1:
        return True
    for i in range(HEIGHT):
        row = pzl[i*WIDTH:i*WIDTH+WIDTH]
        if row.count(X) == WIN or row.count(O) == WIN:
            print("ROW")
            return True

    if [y.count(X) for y in[[pzl[x], pzl[x+3], pzl[x+6]] for x in range(WIDTH)]].count(WIN) >= 1:
        return True
    if [y.count(O) for y in[[pzl[x], pzl[x+3], pzl[x+6]] for x in range(WIDTH)]].count(WIN) >= 1:
        return True
         
    if (pzl[0] == X and pzl[4] == X and pzl[8] == X) or (pzl[2] == X and pzl[4] == X and pzl[6] == X):
        print("L-R DIAG")
        return True
    if (pzl[0] == O and pzl[4] == O and pzl[8] == O) or (pzl[2] == O and pzl[4] == O and pzl[6] == O):
        print("R-L DIAG")
        return True
    return False


def possibilities(pzl, board, move):
    if finished(pzl):
        print(f"adding {pzl}")
        board.add(pzl)
        return ""
    

    set_of_choices = [pos for pos,elem in enumerate(pzl) if elem == '.']
    
    for index in set_of_choices:
        new_pzl = pzl[:index] + move + pzl[index+1:]
        print(f"recurring on {new_pzl}")
        p = possibilities(new_pzl, board, X if move == O else O)
        if p:
            return ""
    return board


def main():
    global HEIGHT, WIDTH, WIN
    WIN, HEIGHT, WIDTH = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) == 4 else (3, int(argv[1]), int(argv[2]))
    pzl = '.'*HEIGHT*WIDTH

    return len(possibilities(pzl,set(),X).union(possibilities(pzl,set(),O)))


if __name__ == "__main__":
    print(main())
