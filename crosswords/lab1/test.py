#!/usr/bin/env python3
EMPTY = '-'
PROTECTED = '$'
BLOCK = '#'
HEIGHT = 7
WIDTH = 7
AREA = HEIGHT * WIDTH
CENTER = AREA // 2
NEIGHBORS = {}

INDICES = {
    index: (index // WIDTH, (index % WIDTH)) for index in range(AREA)
}  # idx -> (row, col)
INDICES_2D = {
    (i, j): i * WIDTH + j for i in range(HEIGHT) for j in range(WIDTH)
}  # (row, col) -> idx

to_string = lambda pzl: "\n".join(
    ["".join([pzl[INDICES_2D[(i, j)]][0] for j in range(WIDTH)]) for i in range(HEIGHT)]
).strip()


def bfs(board, starting_index, blocking_token=BLOCK):
    visited = {starting_index}
    queue = [starting_index]
    count = 0

    for index in queue:
        for neighbor in NEIGHBORS[index]:
            if board[neighbor] != blocking_token and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                count += 1

    return count, visited


def connected_components(board):
    visited, components = set(), []
    for pos, elem in enumerate(board):
        if elem == BLOCK or pos in visited:
            continue
        tmp = bfs(board, pos)
        visited |= tmp[1]
        components.append(tmp)
    return sorted(components)


def gen_neighbors():
    for index in range(0, AREA):
        row = index // WIDTH
        neighbors = [i for i in [index + WIDTH, index - WIDTH] if 0 <= i < AREA]
        if (index + 1) // WIDTH == row and index + 1 < AREA:
            neighbors.append(index + 1)
        if (index - 1) // WIDTH == row and index - 1 >= 0:
            neighbors.append(index - 1)
        NEIGHBORS[index] = neighbors


board = [*"###---##----------------#----------------##---###"]
gen_neighbors()
print(to_string(board))
print()
cc = connected_components(board)
print(cc)
print(len(cc))
print(len(cc[0][1]))