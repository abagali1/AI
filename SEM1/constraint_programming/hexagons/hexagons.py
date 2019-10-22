from sys import argv

nums = {'A': ['1', '2', '3', '4', '5', '6'], 'B': ['1', '2', '3', '4', '5', '6', '7']}
hexagons, rows = [], []


def pzl_to_hexagons(p):
    return [
        [p[0], p[1], p[2], p[6], p[7], p[8]],
        [p[2], p[3], p[4], p[8], p[9], p[10]],
        [p[5], p[6], p[7], p[12], p[13], p[14]],
        [p[7], p[8], p[9], p[14], p[15], p[16]],
        [p[9], p[10], p[11], p[16], p[17], p[18]],
        [p[13], p[14], p[15], p[19], p[20], p[21]],
        [p[15], p[16], p[17], p[21], p[22], p[23]]
    ]


def is_invalid(p, q):
    hex_dict = pzl_to_hexagons(p)
    for hex in range(len(hex_dict)):
        for i in range(1,7):
            if hex_dict[hex].count(str(i)) >1:
                return True
    return False


def is_solved(pzl, question):
    global hexagons, rows
    return False if pzl.find(".") != -1 else True


def brute_force(pzl, question):
    if question == 'B':
        return None
    if is_invalid(pzl, question):
        return ""
    if is_solved(pzl, question):
        return pzl

    i = pzl.find(".")
    for j in range(1,7):
        new_pzl = pzl[:i] + str(j) + pzl[i+1:]
        b_f = brute_force(new_pzl, question)
        if b_f:
            return b_f
    

if __name__ == '__main__':
    sol = brute_force(argv[2], argv[1])
    if sol is None:
        print("No Solution Possible")
    else:
        print(sol)
        print(" ", end="")
        for i in range(0,5):
            print(sol[i], end="")
        print("")
        for i in range(6,6+7):
            print(sol[i], end="")
        print("")
        for i in range(6+7,13+7):
            print(sol[i], end="")
        print("")
        print(" ", end="")
        for i in range(20,24):
            print(sol[i], end="")
        print("")