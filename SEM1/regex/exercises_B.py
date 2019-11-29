from sys import argv

expressions = [
    "/^[.ox]{64}$/i",
    "/^[ox]*\.[ox]*$/i",
    "",
    "/^.(..)*$/"


]

if __name__ == '__main__':
    print(expressions[int(argv[1])-40])