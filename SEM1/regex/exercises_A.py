#!/usr/bin/env python3
from sys import argv

expressions = [
    r"/^0$|^10[01]$/",
    r"/^[0-1]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^1[0-1]*0$|^0$/",
    r"/^[0-1]*110[0-1]*$/",
    r"/^.{2,4}$/s",
    r"/^\d{3} *-? *\d{2} *-? *\d{4}$/",
    r"/^.*?d\w*/mi",
    r"/^[01]?$|^1[01]*1$|^0[01]*0$/"
    ]

if __name__ == "__main__":
    print(expressions[int(argv[1])-30])