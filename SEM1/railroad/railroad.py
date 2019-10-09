from sys import argv

names = {} # stores station code -> name
graph = {} # station code -> [ name, (lat,long), [neighbors] ]


def load_table():
    global names, graph
    names = {' '.join(x.split(" ")[1:]): x.split(" ")[0] for x in open('rrNodeCity.txt').read().splitlines()}
    for x in open('rrNodes.txt').read().splitlines():
        parts = x.split(" ")
        graph[int(parts[0])] = [(float(parts[1]), float(parts[2])), []]
    for x in open("rrEdges.txt").read().splitlines():
        parts = x.split(" ")
        graph[int(parts[0])][2].append(int(parts[1]))


def a_star(cities):
    global names, graph
    root, dest = '', ''
    tmp = ''
    for x in range(len(cities)):
        tmp += cities[x] + " "
        if tmp.strip() in names:
            if root == '':
                root = tmp.strip()
            elif dest == '':
                dest = tmp.strip()
            tmp = ''
    print(f"ROOT: {root}, DEST: {dest}")






def main():
    cities = argv[1:]
    load_table()
    a_star(cities)


if __name__ == '__main__':
    main()