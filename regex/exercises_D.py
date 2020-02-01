from sys import argv


expressions = [
    r"/^(0(?!10)|1)*$/", # 16 BEST: 14
    r"/^((?!101|010)[01])*$/", #22 BEST: 20
    r"/^(0|1)([01]*\1)?$/", # 18 BEST: 14
    r"/\b(?!(\w)+\w*\1\b)\w+/i" # finished 
]

if __name__ == '__main__':
    print(expressions[int(argv[1])-60])