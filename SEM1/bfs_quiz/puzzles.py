from sys import argv

BACKWARD_SYM = "\\"
FORWARD_SYM = "/"
HORIZONTAL_SYM = "-"
ROWS = {
    0: 0,
    1: 1,
    2: 1,
    3: 2,
    4: 2,
    5: 2,
    6: 3,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
    11: 4,
    12: 4,
    13: 4,
    14: 4
}  # DOES NOT CONTAIN NEIGHBOR POSITIONS.... NEIGHBOR POSITIONS ARE CALCED IN neighbors()
FORWARDS = {
    0: [(3, 1)],
    1: [(6, 3)],
    2: [(7, 4)],
    3: [(10, 6), (0, 1)],
    4: [(11, 7)],
    5: [(12, 8)],
    6: [(1, 3)],
    7: [(2, 4)],
    10: [(3, 6)],
    11: [(4, 7)],
    12: [(5, 8)],
} # KEY = '.' VALUE = (peg switching, intermediary)
NO_FORWARD_SWITCHES = [8,9,13,14] # THESE INDICES CANNOT HAVE FORWARD(/) SWITCHES
NO_BACKWARD_SWITCHES = [6,7,10,11] # THESE INDICES CANNOT HAVE BACKWARD(\) SWITCHES
BACKWARDS = {
    0: [(5,2)],
    1: [(8,4)],
    2: [(9,5)],
    3: [(12,7)],
    4: [(13,8)],
    5: [(14,9),(0,2)],
    8: [(1,4)],
    9: [(2,5)],
    12: [(3,7)],
    13: [(4,8)],
    14: [(5,9)]
} # KEY = '.' pos VALUE = (peg switching, intermediary)


def backtrack(visited_nodes, goal):
    if len(visited_nodes) == 0:
        return [goal], 0, d
    path = [visited_nodes[goal]]
    for i in path:
        if i in visited_nodes.keys() and visited_nodes[i] != '':
            tmp = visited_nodes[i]
            path.append(tmp)
    return path[::-1] + [goal], len(path)


def gen_swaps(pzl, start_pos, end_pos, type):
    swaps = []
    if type == HORIZONTAL_SYM:
        tmp = pzl[:]
        if tmp[end_pos] == '.' and tmp[start_pos] == '1' and (tmp[start_pos+1] == '1' or tmp[start_pos-1] == '1'):
            if start_pos < end_pos:
                tmp = tmp[:start_pos] + '..1' + pzl[end_pos+1:]
            elif start_pos > end_pos:
                tmp = tmp[:end_pos] + '1..' + pzl[start_pos+1:]
                swaps.append(tmp)
    elif type == FORWARD_SYM:
        for tup in start_pos:
            tmp = pzl[:]
            if tmp[end_pos] == '.' and tmp[tup[0]] == '1' and tmp[tup[1]] == '1':
                tmp = tmp[:tup[0]] + '.' + tmp[tup[0]+1:]
                tmp = tmp[:tup[1]] + '.' + tmp[tup[1]+1:]
                tmp = tmp[:end_pos] + '1' + tmp[end_pos+1:]
                swaps.append(tmp)
    elif type == BACKWARD_SYM:
        for tup in start_pos:
            tmp = pzl[:]
            if tmp[end_pos] == '.' and tmp[tup[0]] == '1' and tmp[tup[1]] == '1':
                tmp = tmp[:tup[0]] + '.' + tmp[tup[0]+1:]
                tmp = tmp[:tup[1]] + '.' + tmp[tup[1]+1:]
                tmp = tmp[:end_pos] + '1' + tmp[end_pos+1:]
                swaps.append(tmp)
    return swaps


def neighbors(pzl):
    neighbors = []
    for pos, elem in enumerate(pzl):
        if elem == '.':
            # horizontal switches
            if ROWS[pos] > 1:
                if pos-2 in ROWS:
                    if ROWS[pos-2] == ROWS[pos]:
                        neighbors.append(gen_swaps(pzl, pos-2, pos, HORIZONTAL_SYM))
                if pos+2 in ROWS:
                    if ROWS[pos+2] == ROWS[pos]:
                        neighbors.append(gen_swaps(pzl, pos+2, pos, HORIZONTAL_SYM))
            # '/' switches
            if pos not in NO_FORWARD_SWITCHES:
                neighbors.append(gen_swaps(pzl,FORWARDS[pos], pos, FORWARD_SYM))
            # '\' switches
            if pos not in NO_BACKWARD_SWITCHES:
                neighbors.append(gen_swaps(pzl,BACKWARDS[pos], pos, BACKWARD_SYM))

    tmp = []
    for i in neighbors:
        tmp.extend(i)
    return tmp


def at_goal_a(p, s_p):
    return p.find('1') == s_p and p.count('1') == 0

def at_goal_b(visited_set, s_p):
    return len([i for i in visited_set if i.find('1') == s_p and i.count('1') == 1]) == 0


def problem1(puzzle):
    parent = [puzzle]
    visited = {parent[0]: ''}
    starting_hole_pos = puzzle.find('.')

    while parent:
        elem = parent.pop(0)
        neigh = neighbors(elem)
        for n in neigh:
            if at_goal_a(n, starting_hole_pos):
                visited[n] = elem
                return visited
            elif n not in visited.keys():
                visited[n] = elem
                parent.append(n)
    return -1


def problem2(puzzle):
    parent = [puzzle]
    visited = {parent[0]: ''}
    starting_hole_pos = puzzle.find('.')

    for elem in parent:
        neigh = neighbors(elem)
        for n in neigh:
            if at_goal_b(n, starting_hole_pos):
                visited[n] = elem
                return backtrack(visited, n)
            elif n not in visited.keys():
                visited[n] = elem
                parent.append(n)
    return ['NULL'], -1


if __name__ == '__main__':
    pzl = "111111111111111"
    for i in range(len(pzl)):
        tmp = pzl[:]
        tmp = tmp[:i] + '.' + tmp[i+1:]
        print(tmp, problem1(tmp))


    #roblem2(start)





#  Find end puzzle where final peg is in same spot as starting hole
#  Find start puzzle where final peg CANNOT end in same spot as starting hole