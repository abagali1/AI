#!/usr/bin/env python3
from sys import argv

expressions = [
    r"/^0$|^100$|^101$/",
    r"/^[0-1]*$/",
    r"/^[0-1]*0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^1[0-1]*0$|^0$/",
    r"/^[0-1]*?110[0-1]*?$/",
    r"/^.{2,4}$/s",
    r"/^[0-9]{3} *?-? *?[0-9]{2} *?-? *?[0-9]{4}$/",
    r"/^.*?d/m", # FIXME
    None, # TODO
    ]

if __name__ == "__main__":
    print(expressions[int(argv[1])-30])