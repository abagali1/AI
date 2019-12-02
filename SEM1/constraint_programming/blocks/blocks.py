# Anup Bagali Period 2
#!/usr/bin/env python3
from sys import argv


class Puzzle:

    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.size = h*w
        self.board = [[] for _ in range(h*w)]
    
    def __str__(self):
        return '\n'.join([''.join([self.board[i*self.width +j][0] for j in range(self.width)]) for i in range(self.height)]).strip()

    def add_block(self, block): # TODO: ADD BLOCKS TO BOARD
        """
        block: tuple(height, width, letter)
        return False here to get rid of is_invalid??
        """
        for position in range(self.size):
            if not self.board[position]:
                if self.add(position, block) or self.add(position, (block[1], block[0], block[2])):
                    return
                     

    def add(self, top_left_index, block):
        return True


    @property
    def decomposition(self): # TODO: RETURN PZL DECOMPOSITION
        return ""


ALPHABET = {i-ord('A'): chr(i) for i in range(ord('A'),ord('Z')+1)}
LETTERS = {}


def brute_force(pzl, blocks):
    if not blocks:
        return pzl

    
    while blocks:
        block = blocks.pop(0)

    



def main():
    global LETTERS

    args = ' '.join(argv[1:]).replace('x',' ').split(" ")  # standardize format(no more 'x')
    pzl, blocks = Puzzle(int(args[0]), int(args[1])), [(int(args[i]), int(args[i+1]), ALPHABET[pos]) for pos, i in enumerate(range(2, len(args), 2))] # extract blocks

    LETTERS = {i[2]: (i[0], i[1]) for i in blocks}


    sol = brute_force(pzl=pzl, blocks=blocks)
    if sol:
        print(pzl)
        print(pzl.decomposition)
    else:
        print("No solution")





if __name__ == "__main__":
    main()