from sys import argv

expressions = [
    "/^[.ox]{64}$/i", #40
    "/^[ox]*\.[ox]*$/i", #41
    "", #42
    "/^.(..)*$/s", #43
    "/^0.(..)*$|^1.(.)*$/s" # 44


]

if __name__ == '__main__':
    print(expressions[int(argv[1])-40])