from sys import argv


def string_to_pzl(p, dim, size):
    pzls = []
    for i in range(0,size,dim):
        for j in range(i,i+dim):
            tmp = []
            tmp.append(p[j])
        pzls.append(tmp)
    for i in range(0,dim):
        for j in range(i,size,dim):
            tmp = []
            tmp.append(p[j])
        pzls.append(tmp)
    return pzls



def is_invalid(p, q):
    hex_dict = string_to_pzl(p)
    for hex in range(len(hex_dict)):
        for i in range(1, 7):
            if hex_dict[hex].count(str(i)) > 1:
                return True
    return False


def is_solved(pzl, question):
    return False if pzl.find(".") != -1 else True


def brute_force(pzl, question):
    if is_invalid(pzl, question):
        return ""
    if is_solved(pzl, question):
        return pzl

    i = pzl.find(".")
    new_pzls = [pzl[:i] + str(j) + pzl[i + 1:] for j in nums[question]]
    for new_pzl in new_pzls:
        b_f = brute_force(new_pzl, question)
        if b_f:
            return b_f


if __name__ == '__main__':
    sol = brute_force(argv[1])
    if sol is None:
        print("No Solution Possible")
    else:
        print(sol)
