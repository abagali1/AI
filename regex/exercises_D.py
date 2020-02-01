from sys import argv


expressions = [
    r"/^((?!010)[01])*$/", # BEST: 14 CURRENT: 16
    r"/^((?!101|010)[01])*$/", # finished 
    r"/^([01])[01]*\1$|^[01]$/", # BEST: 14 CURRENT: 21
    r"/^(?!\1).*(.)$/" # BEST: 21
]

if __name__ == '__main__':
    print(expressions[int(argv[1])-60])