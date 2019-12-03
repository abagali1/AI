from sys import argv

expressions = [
    r"/^[.ox]{64}$/i", #40
    r"/^[ox]*\.[ox]*$/i", #41
    r"", #42
    r"/^.(..)*$/s", #43
    r"/^(0|10|11)([01]{2})*$/", # 44
    r"/^.*[aeiou][aeiou].*$/", # 45
    r"", # 46
    r"/^([bc])+?a?$/"


]

if __name__ == '__main__':
    print(expressions[int(argv[1])-40])