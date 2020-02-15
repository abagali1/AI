#!/usr/bin/env python3
EMPTY = '-'
PROTECTED = '$'
BLOCK = '#'
HEIGHT = WIDTH = 13
AREA = HEIGHT * WIDTH
CENTER = AREA // 2
NEIGHBORS = {}


def bfs(board, starting_index, blocking_token=BLOCK):
    visited = {starting_index}
    queue = [starting_index]

    for index in queue:
        for neighbor in NEIGHBORS[index]:
            if board[neighbor] != blocking_token and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return visited


def connected_components(board):
    visited, components = set(), []
    for pos, elem in enumerate(board):
        if elem == BLOCK or pos in visited:
            continue
        tmp = bfs(board, pos)
        visited |= tmp
        components.append(tmp)
    return components


def gen_neighbors():
    for index in range(0, AREA):
        row = index // WIDTH
        neighbors = [i for i in [index + WIDTH, index - WIDTH] if 0 <= i < AREA]
        if (index + 1) // WIDTH == row and index + 1 < AREA:
            neighbors.append(index + 1)
        if (index - 1) // WIDTH == row and index - 1 >= 0:
            neighbors.append(index - 1)
        NEIGHBORS[index] = neighbors


board = ['$', '$', '$', '#', '$', '$', '$', '$', '#', '$', '$', '$', '$', '$', '$', '$', '#', '$', '$', '$', '$', '#', '$', '$', '$', '$', '$', '$', '$', '#', '$', '$', '$', '$', '#', '$', '$', '$', '$', '$', '$', '$', '#', '#', '#', '#', '-', '-', '-', '-', '-', '$', '$', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '-', '$', '-', '-', '-', '-', '$', '#', '$', '-', '-', '-', '-', '-', '-', '-', '-', '-', '$', '$', '#', '$', '$', '-', '-', '-', '-', '-', '-', '-', '-', '-', '$', '#', '$', '-', '-', '-', '-', '$', '-', '-', '-', '-', '-', '-', '#', '-', '-', '-', '-', '-', '$', '$', '-', '-', '-', '-', '-', '#', '#', '#', '#', '$', '$', '$', '$', '$', '$', '$', '#', '$', '$', '$', '$', '#', '$', '$', '$', '$', '$', '$', '$', '#', '$', '$', '$', '$', '#', '$', '$', '$', '$', '$', '$', '$', '#', '$', '$', '$', '$', '#', '$', '$', '$']
gen_neighbors()
print(board)
cc = connected_components(board)
print(cc)
print(len(cc))

