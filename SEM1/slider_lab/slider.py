import sys


def solve(puzzle, goal="12345678_"):
	if puzzle == goal:
		print(puzzle)
		return backtrack({}, goal)

	parent = [puzzle]

	visited = {parent[0]: ''}

	while parent:
		elem = parent.pop(0)
		neighbors = get_children([list(elem[0:3]), list(elem[3:6]), list(elem[6:9])])
		for n in neighbors:
			if n == goal:
				return backtrack(visited, goal)
			else:
				visited[''.join(str(item) for i in n for item in i)] = elem
				parent.extend(neighbors)


def backtrack(visited_nodes, goal):
	path = [visited_nodes[goal]]
	path.extend(visited_nodes[i] for i in path if i in visited_nodes.keys())
	return path[::-1], len(path)


def get_children(parent):
	print(parent)
	index = [(index, row.index('_')) for index, row in enumerate(parent) if '_' in row][0]
	neighbors = [(x, y) for x, y in [(index[0], index[1] - 1), (index[0], index[1] + 1), (index[0] + 1, index[1]), (index[0] - 1, index[1])] if
			0 <= x < len(parent) and 0 <= y < len(parent[0])]
	return gen_swaps(parent, neighbors, index)


def gen_swaps(p, n, i):
	true_neighbors = []
	for neighbor in n:
		temp = p.copy()
		temp[i[0]][i[1]], temp[neighbor[0]][neighbor[1]] = temp[neighbor[0]][neighbor[1]], temp[i[0]][i[1]]
		true_neighbors.append(temp)
	return true_neighbors



def main():
	try:
		puzzle = sys.argv[1]
	except IndexError:
		print("Usage: \"python3 slider.py <puzzle> <goal(optional)>\"")
		print("Missing Puzzle Parameter")
		return

	try:
		goal = sys.argv[2]
	except IndexError:
		goal = None

	print(f"Steps: {solve(puzzle, goal)}")


if __name__ == '__main__':
	main()
