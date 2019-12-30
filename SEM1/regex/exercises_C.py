from sys import argv


expressions = [
    r"/(\w)+\w*\1\w*/",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//",
    r"//"
]

if __name__ == '__main__':
    print(expressions[int(argv[1])-50])