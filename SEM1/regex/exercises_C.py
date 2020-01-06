from sys import argv


expressions = [
    r"/(\w)+\w*\1\w*/i",
    r"/(\w)+(\w*\1){3}\w*/i",
    r"/^(0|1)([01]*\1)?$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*ing)(?=\w*bri)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i",
    r"//",
    r"/^(?!10011)[01]*$/",
    r"//",
    r"//"
]

if __name__ == '__main__':
    print(expressions[int(argv[1])-50])