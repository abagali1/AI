#!/usr/bin/env python3
from sys import argv

expressions = {
    31: r"^0$|^100$|^101$",
    32: r"^[0-1]*$",
    33: r"^[0-1]*0$",
    34: r"\b(?:\w*[aeiou]\w*){2,}\b",
    35: r"^[0-1]*0$",
    36: r"^[0-1]*?110[0-1]*?$",
    37: r"^.{2,4}$",
    38: r"^[0-9]{3} *?-? *?[0-9]{2} *?-? *?[0-9]{4}$",
    39: r".*?d",
    40: None,
}


if __name__ == "__main__":
    print(expressions[argv[1]])