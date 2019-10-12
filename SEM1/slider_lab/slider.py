from sys import argv
from time import time
from math import sqrt

# character representing empty space and time limit are constants
SPACE, TIME_LIMIT = "_", 90
# Lookup table for all possible manhattan distances (puzzle_dim: {(x,y): manhattan_distance})
MANHATTAN_TABLE = {
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
# Lookup table storing maximum length of path for puzzle (puzzle_dim: max_path)
LENGTH_TABLE = {3: 31, 4: 82}
# Lookup table storing the letter: position of the goal puzzle (letter: index_of_letter)
GOAL_TABLE = {}
# Lookup table storing all possible neighbors at a given index (index: [index1,index2...])
NEIGHBOR_TABLE = {}

"""
Generates neighbors for a specific puzzle
@:param parent (puzzle, position of space in puzzle)
"""


def get_children(parent):
    true_neighbors = []  # list to store final neighbors

    # iterate through all indices of possible neighbors
    for neighbor in NEIGHBOR_TABLE[parent[1]]:
        temp = list(parent[0][:])  # copy string into temp list
        temp[parent[1]], temp[neighbor] = temp[neighbor], temp[parent[1]]  # swap space and neighboring characters
        true_neighbors.append((''.join(temp), neighbor))  # join swapped list back into string
    return true_neighbors


"""
Generates the manhattan puzzle for a puzzle assuming the goal state is the default end state
@:param puzzle (puzzle, position of space in puzzle)
@:param dim dimensions of puzzle
"""


def manhattan_distance(puzzle, dim):
    return sum([MANHATTAN_TABLE[dim][(i, GOAL_TABLE[j])] for i, j in enumerate(puzzle) if puzzle[i] != SPACE])


"""
Uses the A* algorithm to determine the optimal solve path for a given puzzle to a goal state
@:param puzzle starting puzzle
@:param goal desired end state
@:param size total length of puzzle string
@:param dimensions of the given puzzle
"""


def solve(puzzle, goal, size, dim):
    start = time()  # record starting time
    if puzzle == goal:  # already at goal state
        return 0, time() - start
    if not solveable(puzzle, size, dim):  # goal state unreachable
        return -1, time() - start

    bucket = [[] for _ in range(LENGTH_TABLE[dim])]  # list of open_sets indexed by F value (g+h)
    closed_set = set()  # set of all visited nodes
    bucket[manhattan_distance(puzzle, dim)].append(
        [(puzzle, puzzle.find(SPACE)), 0])  # append starting puzzle to appropriate index

    for pos, open_set in enumerate(bucket):  # iterate through buckets
        while open_set:  # while current open_set is not empty
            elem = open_set.pop(-1)  # pop from end of open_set(eliminates manual indexing and expensive reindexing)
            if elem[0] in closed_set:  # continue if already visited
                continue
            closed_set.add(elem[0])  # add to visited
            for nbr in get_children(elem[0]):  # iterate through neighbors of current puzzle
                if nbr[0] == goal:  # goal state has been reached
                    closed_set.add(nbr)
                    return elem[1] + 1, time() - start
                bucket[manhattan_distance(
                    nbr[0], dim) + (elem[1] + 1)].append([nbr, elem[1] + 1])  # add new puzzle to appropriate bucket


"""
Uses inversion counts to determine if a puzzle is able to reach its default goal state
@:param puzzle puzzle string
@:param size total length of the puzzle string
@:param dim dimensions of puzzle 
"""


def solveable(puzzle, size, dim):
    pzl = puzzle.replace(SPACE, "")  # space value does not contribute to inversion counts
    inversion_count = len([i for i in range(size - 1)
                           for j in range(i + 1, size - 1) if pzl[i] > pzl[j]])  # determine inversion counts
    pos = size - (puzzle.find(SPACE) // dim)  # determine position of space character relative to bottom of puzzle
    return not (inversion_count % 2) if size % 2 == 1 else not (inversion_count % 2) if pos % 2 == 1 else bool(
        inversion_count % 2)  # if the puzzle size is odd, puzzle is solveable if inversion count is even
    # if the puzzle size is even, puzzle is solveable if inversion count is even and position is odd or vice versa


def main():
    if len(argv) == 2:
        start_time = time()
        puzzles = open(argv[1]).read().splitlines()
        impossible_count, count, lengths, goal = 0, 0, 0, puzzles[0]  # statistical variables and constants
        s = len(goal)  # length of puzzle string
        d = int(sqrt(s))  # dimensions of puzzle

        # start initializing lookup tables
        for x, y in enumerate(goal):  # indexes goal state
            GOAL_TABLE[y] = x
        for index in range(0, s):  # saves all possible neighbors for all indices
            row = index // d
            neighbors = [i for i in [index + d, index - d] if 0 <= i < s]
            if (index + 1) // d == row and index + 1 < s:
                neighbors.append(index + 1)
            if (index - 1) // d == row and index - 1 >= 0:
                neighbors.append(index - 1)
            NEIGHBOR_TABLE[index] = neighbors
            # end initializing lookup tables

        for i in range(len(puzzles)):
            if time() - start_time >= TIME_LIMIT:  # watch out for time limit
                break
            solved = solve(puzzles[i], goal, s, d)  # get solved puzzle and time to solve
            if solved[0] == -1:  # puzzle was unsolvable
                impossible_count += 1  # record puzzle as impossible
                print("Pzl {0}: {1} => unsolvable\tin %.2lfs".format(
                    i, puzzles[i]) % solved[1])  # output acknowledgement of impossible state
            else:  # puzzle was solveable
                lengths += len(puzzles[i])  # statistical
                print("Pzl {0}: {1} => {2} steps\tin %.2lfs".format(
                    i, puzzles[i], solved[0]) % solved[1])  # output acknowledgement of solvable puzzle and time used
            count += 1  # increment amount of puzzles finished
        # statistical outputs
        print("Impossible count: {0}".format(impossible_count))
        print("Avg len for possibles: {0}".format(
            lengths / count - impossible_count))
        print("Solved {0} puzzles in %.2lfs".format(count) %
              (time() - start_time))
    elif len(argv) == 3:
        start_time = time()
        puzzle = argv[1]
        goal = argv[2]
        s = len(goal)  # length of puzzle string
        d = int(sqrt(s))  # dimensions of puzzle

        # start initializing lookup tables
        for x, y in enumerate(goal):  # indexes goal state
            GOAL_TABLE[y] = x
        for index in range(0, s):  # saves all possible neighbors for all indices
            row = index // d
            neighbors = [i for i in [index + d, index - d] if 0 <= i < s]
            if (index + 1) // d == row and index + 1 < s:
                neighbors.append(index + 1)
            if (index - 1) // d == row and index - 1 >= 0:
                neighbors.append(index - 1)
            NEIGHBOR_TABLE[index] = neighbors
            # end initializing lookup tables
        solved = solve(puzzle, goal, s, d)  # get solved puzzle and time to solve
        if solved[0] == -1:  # puzzle was unsolvable
            print("Pzl {0} => unsolvable\tin %.2lfs".format(
                puzzle) % solved[1])  # output acknowledgement of impossible state
        else:  # puzzle was solveable
            print("Pzl {0} => {1} steps\tin %.2lfs".format(
                puzzle, solved[0]) % solved[1])  # output acknowledgement of solvable puzzle and time used
        print("Time used: %.2lfs" % (time()-start_time))
    else:
        print("Error: {0} arguments".format("Too many" if len(argv) > 2 else "Missing"))
        print("Usage: python slider.py <puzzle> <goal>")
        print("Usage: python slider.py <filename>")


if __name__ == '__main__':
    main()
