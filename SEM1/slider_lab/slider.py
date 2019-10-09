from sys import argv
from time import time
from math import sqrt

SPACE = "_"
minty_lookup_table = {
    3: {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 1, (0, 4): 2, (0, 5): 3, (0, 6): 2, (0, 7): 3, (0, 8): 4, (1, 0): 1,
        (1, 1): 0, (1, 2): 1, (1, 3): 2, (1, 4): 1, (1, 5): 2, (1, 6): 3, (1, 7): 2, (1, 8): 3, (2, 0): 2, (2, 1): 1,
        (2, 2): 0, (2, 3): 3, (2, 4): 2, (2, 5): 1, (2, 6): 4, (2, 7): 3, (2, 8): 2, (3, 0): 1, (3, 1): 2, (3, 2): 3,
        (3, 3): 0, (3, 4): 1, (3, 5): 2, (3, 6): 1, (3, 7): 2, (3, 8): 3, (4, 0): 2, (4, 1): 1, (4, 2): 2, (4, 3): 1,
        (4, 4): 0, (4, 5): 1, (4, 6): 2, (4, 7): 1, (4, 8): 2, (5, 0): 3, (5, 1): 2, (5, 2): 1, (5, 3): 2, (5, 4): 1,
        (5, 5): 0, (5, 6): 3, (5, 7): 2, (5, 8): 1, (6, 0): 2, (6, 1): 3, (6, 2): 4, (6, 3): 1, (6, 4): 2, (6, 5): 3,
        (6, 6): 0, (6, 7): 1, (6, 8): 2, (7, 0): 3, (7, 1): 2, (7, 2): 3, (7, 3): 2, (7, 4): 1, (7, 5): 2, (7, 6): 1,
        (7, 7): 0, (7, 8): 1, (8, 0): 4, (8, 1): 3, (8, 2): 2, (8, 3): 3, (8, 4): 2, (8, 5): 1, (8, 6): 2, (8, 7): 1,
        (8, 8): 0},
    4: {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (0, 4): 1, (0, 5): 2, (0, 6): 3, (0, 7): 4, (0, 8): 2, (0, 9): 3,
        (0, 10): 4, (0, 11): 5, (0, 12): 3, (0, 13): 4, (0, 14): 5, (0, 15): 6, (1, 0): 1, (1, 1): 0, (1, 2): 1,
        (1, 3): 2, (1, 4): 2, (1, 5): 1, (1, 6): 2, (1, 7): 3, (1, 8): 3, (1, 9): 2, (1, 10): 3, (1, 11): 4, (1, 12): 4,
        (1, 13): 3, (1, 14): 4, (1, 15): 5, (2, 0): 2, (2, 1): 1, (2, 2): 0, (2, 3): 1, (2, 4): 3, (2, 5): 2, (2, 6): 1,
        (2, 7): 2, (2, 8): 4, (2, 9): 3, (2, 10): 2, (2, 11): 3, (2, 12): 5, (2, 13): 4, (2, 14): 3, (2, 15): 4,
        (3, 0): 3, (3, 1): 2, (3, 2): 1, (3, 3): 0, (3, 4): 4, (3, 5): 3, (3, 6): 2, (3, 7): 1, (3, 8): 5, (3, 9): 4,
        (3, 10): 3, (3, 11): 2, (3, 12): 6, (3, 13): 5, (3, 14): 4, (3, 15): 3, (4, 0): 1, (4, 1): 2, (4, 2): 3,
        (4, 3): 4, (4, 4): 0, (4, 5): 1, (4, 6): 2, (4, 7): 3, (4, 8): 1, (4, 9): 2, (4, 10): 3, (4, 11): 4, (4, 12): 2,
        (4, 13): 3, (4, 14): 4, (4, 15): 5, (5, 0): 2, (5, 1): 1, (5, 2): 2, (5, 3): 3, (5, 4): 1, (5, 5): 0, (5, 6): 1,
        (5, 7): 2, (5, 8): 2, (5, 9): 1, (5, 10): 2, (5, 11): 3, (
            5, 12): 3, (5, 13): 2, (5, 14): 3, (5, 15): 4, (6, 0): 3, (6, 1): 2, (6, 2): 1, (6, 3): 2, (6, 4): 2,
        (6, 5): 1, (6, 6): 0, (6, 7): 1, (6, 8): 3, (6, 9): 2, (6, 10): 1, (6, 11): 2, (6, 12): 4, (6, 13): 3,
        (6, 14): 2, (6, 15): 3, (7, 0): 4, (7, 1): 3, (7, 2): 2, (7, 3): 1, (7, 4): 3, (7, 5): 2, (7, 6): 1, (7, 7): 0,
        (7, 8): 4, (7, 9): 3, (7, 10): 2, (7, 11): 1, (7, 12): 5, (7, 13): 4, (7, 14): 3, (7, 15): 2, (8, 0): 2,
        (8, 1): 3, (8, 2): 4, (8, 3): 5, (8, 4): 1, (8, 5): 2, (8, 6): 3, (8, 7): 4, (8, 8): 0, (8, 9): 1, (8, 10): 2,
        (8, 11): 3, (8, 12): 1, (8, 13): 2, (8, 14): 3, (8, 15): 4, (9, 0): 3, (9, 1): 2, (9, 2): 3, (9, 3): 4,
        (9, 4): 2, (9, 5): 1, (9, 6): 2, (9, 7): 3, (9, 8): 1, (9, 9): 0, (9, 10): 1, (9, 11): 2, (9, 12): 2,
        (9, 13): 1, (9, 14): 2, (9, 15): 3, (10, 0): 4, (10, 1): 3, (10, 2): 2, (10, 3): 3, (10, 4): 3, (10, 5): 2,
        (10, 6): 1, (10, 7): 2, (10, 8): 2, (10, 9): 1, (10, 10): 0, (10, 11): 1, (10, 12): 3, (10, 13): 2, (10, 14): 1,
        (10, 15): 2, (11, 0): 5, (11, 1): 4, (11, 2): 3, (11, 3): 2, (11, 4): 4, (11, 5): 3, (11, 6): 2, (11, 7): 1,
        (11, 8): 3, (11, 9): 2, (11, 10): 1, (11, 11): 0, (11, 12): 4, (11, 13): 3, (11, 14): 2, (11, 15): 1,
        (12, 0): 3, (12, 1): 4, (12, 2): 5, (12, 3): 6, (12, 4): 2, (12, 5): 3, (12, 6): 4, (12, 7): 5, (12, 8): 1,
        (12, 9): 2, (12, 10): 3, (12, 11): 4, (12, 12): 0, (12, 13): 1, (12, 14): 2, (12, 15): 3, (13, 0): 4,
        (13, 1): 3, (13, 2): 4, (13, 3): 5, (13, 4): 3, (13, 5): 2, (13, 6): 3, (13, 7): 4, (13, 8): 2, (13, 9): 1,
        (13, 10): 2, (13, 11): 3, (13, 12): 1, (13, 13): 0, (13, 14): 1, (13, 15): 2, (14, 0): 5, (14, 1): 4,
        (14, 2): 3, (14, 3): 4, (14, 4): 4, (14, 5): 3, (14, 6): 2, (14, 7): 3, (14, 8): 3, (14, 9): 2, (14, 10): 1,
        (14, 11): 2, (14, 12): 2, (14, 13): 1, (14, 14): 0, (14, 15): 1, (15, 0): 6, (15, 1): 5, (15, 2): 4, (15, 3): 3,
        (15, 4): 5, (15, 5): 4, (15, 6): 3, (15, 7): 2, (15, 8): 4, (15, 9): 3, (15, 10): 2, (15, 11): 1, (15, 12): 3,
        (15, 13): 2, (15, 14): 1, (15, 15): 0}}
mintier_lookup_table = {3: 31, 4: 82}
find_table = {}
space_table = {
    3: {
        0: 2, 1: 3, 2: 2, 3: 3, 4: 4, 5: 3, 6: 2, 7: 3, 8: 2
    },
    4: {
        0: 2, 1: 3, 2: 3, 3: 2, 4: 3, 5: 4, 6: 4, 7: 3, 8: 3, 9: 4, 10: 4, 11: 3, 12: 2, 13: 3, 14: 3, 15: 2
    }
}


def get_children(parent, d):
    index = parent[1]
    row = index // d
    neighbors = [i for i in [index + d, index - d] if 0 <= i < len(parent[0])]
    if (index + 1) // d == row and index + 1 < len(parent[0]):
        neighbors.append(index + 1)
    if (index - 1) // d == row and index -1 >= 0:
        neighbors.append(index - 1)

    true_neighbors = []
    for neighbor in neighbors:
        temp = list(parent[0][:])
        temp[index], temp[neighbor] = temp[neighbor], temp[index]
        true_neighbors.append((''.join(temp), neighbor))
    return true_neighbors


def manhattan_distance(puzzle, dim):
    return sum([minty_lookup_table[dim][(i, find_table[j])] for i, j in enumerate(puzzle) if puzzle[i] != SPACE])


def solve(puzzle, goal):
    start = time()
    if puzzle == goal:
        return 0, time() - start
    size = len(puzzle)
    dim = int(sqrt(size))
    if not solveable(puzzle, size, dim):
        return -1, time() - start

    bucket, closed_set = [[] for _ in range(mintier_lookup_table[dim])], set()
    bucket[manhattan_distance(puzzle, dim)].append([(puzzle, puzzle.find(SPACE)), 0])

    for pos, open_set in enumerate(bucket):
        index = 0
        while index < len(open_set):
            elem, index = open_set[index], index + 1
            if elem[0] in closed_set:
                continue
            closed_set.add(elem[0])
            for nbr in get_children(elem[0], dim):
                if nbr[0] == goal:
                    closed_set.add(nbr)
                    return elem[1] + 1, time() - start
                bucket[manhattan_distance(
                    nbr[0], dim) + (elem[1] + 1)].append([nbr, elem[1] + 1])


def solveable(puzzle, size, dim):
    pzl = puzzle.replace(SPACE, "")
    inversion_count = len([i for i in range(size - 1)
                           for j in range(i + 1, size - 1) if pzl[i] > pzl[j]])
    pos = size - (puzzle.find(SPACE) // dim)
    return not (inversion_count % 2) if size % 2 == 1 else not (inversion_count % 2) if pos % 2 == 1 else bool(
        inversion_count % 2)


def main():
    start_time = time()
    puzzles = open(argv[1]).read().splitlines()
    impossible_count, count, lengths, goal = 0, 0, 0, puzzles[0]
    for x, y in enumerate(goal):
        find_table[y] = x
    for i in range(len(puzzles)):
        if time() - start_time >= 90:
            break
        p = puzzles[i]
        solved = solve(p, goal)
        if solved[0] == -1:
            impossible_count += 1
            print("Pzl {0}: {1} => unsolvable\tin %.2lfs".format(
                i, p) % solved[1])
        else:
            lengths += len(p)
            print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(
                i, p, solved[0]) % solved[1])
        count += 1
    print("Impossible count: {0}".format(impossible_count))
    print("Avg len for possibles: {0}".format(
        lengths / count - impossible_count))
    print("Solved {0} puzzles in %.2lfs".format(count) %
          (time() - start_time))


if __name__ == '__main__':
    main()
