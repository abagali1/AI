#!/usr/bin/env python3
from sys import argv


def clean_args(args):
    pzl = (int(args[0][:args[0].find('x')]), int(args[0][args[0].find('x')+1:])) if 'x' in args[0] else (int(args[0]), int(args[1]))
    blocks = []
    start = 1 if 'x' in args[0] else 2
    print(args[start:])

    for i in args[start:]:
        if 'x' in i:
            blocks.append((int(i.split('x')[0]), int(i.split('x')[1])))
            args.remove(i)
    
    blocks += [(int(args[i]), int(args[i+1])) for i in range(start, len(args), 2)]
        

    return '.'*(pzl[0]*pzl[1]), blocks



def brute_force(pzl, blocks):
    if is_invalid(pzl):
        return ""
    if not blocks:
        return pzl




def main():
    pzl, blocks = clean_args(argv[1:])
    sol = brute_force(pzl, blocks)






if __name__ == "__main__":
    main()