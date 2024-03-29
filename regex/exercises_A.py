#!/usr/bin/env python3
from sys import argv

expressions = [
    r"/^10[01]$|^0$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/s",
    r"/^\d{3} *-? *\d\d *-? *\d{4}$/",
    r"/^.*?d\w*/mi",
    r"/^0[01]*0$|^1[01]*1$|^[01]?$/"
    ]

if __name__ == "__main__":
    print(expressions[int(argv[1])-30])
