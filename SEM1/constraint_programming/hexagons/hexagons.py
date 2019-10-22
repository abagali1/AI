from sys import argv

nums = {'A': ['1', '2', '3', '4', '5', '6'], 'B': ['1', '2', '3', '4', '5', '6', '7']}


def is_invalid(p, q):
    hexagons = [
        [p[0], p[1], p[2], p[6], p[7], p[8]],
        [p[2], p[3], p[4], p[8], p[9], p[10]],
        [p[5], p[6], p[7], p[12], p[13], p[14]],
        [p[7], p[8], p[9], p[14], p[15], p[16]],
        [p[9], p[10], p[11], p[16], p[17], p[18]],
        [p[13], p[14], p[15], p[19], p[20], p[21]],
        [p[15], p[16], p[17], p[21], p[22], p[23]]
    ]

    for d in [x.count(i) for x in hexagons for i in nums[q]]:
        if d > 1:
            return True

    if q == 'B':
        rows = [
            [p[0], p[1], p[2], p[3], p[4]],
            [p[5], p[6], p[7], p[8], p[9], p[10], p[11]],
            [p[12], p[13], p[14], p[15], p[16], p[17], p[18]],
            [p[19], p[20], p[21], p[22], p[23]],
            [p[3], p[4], p[10], p[11], p[18]],
            [p[1], p[2], p[8], p[9], p[16], p[17], p[23]],
            [p[0], p[6], p[7], p[14], p[15], p[21]],
            [p[5], p[12], p[13], p[19], p[20]],
            [p[12], p[5], p[6], p[0], p[1]],
            [p[19], p[13], p[14], p[7], p[8], p[2], p[3]],
            [p[20], p[21], p[15], p[16], p[9], p[10], p[4]],
            [p[22], p[23], p[17], p[18], p[11]]
        ]
        for d in [x.count(i) for x in rows for i in nums[q]]:
            if d > 1:
                return True
    return False


def brute_force(pzl, question):
    if is_invalid(pzl, question):
        return ""
    if isSolved(pzl, question):
        return pzl


if __name__ == '__main__':
    print(brute_force(argv[2], argv[1]))
