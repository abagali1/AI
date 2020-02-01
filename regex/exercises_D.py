from sys import argv


expressions = [
    r"/^(0(?!10)|1)*$/",
    r"/^((?!101|010)[01])*$/",
    r"/^(0|1)([01]*\1)?$/", 
    r"/\b(?!(\w)+\w*\1\b)\w+/i" 
]

if __name__ == '__main__':
    print(expressions[int(argv[1])-60])