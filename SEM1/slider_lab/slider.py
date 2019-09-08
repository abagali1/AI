import sys


class Graph
	
	def __init__():
		




def solve(puzzle, goal):
	if(puzzle == goal):
		return 0




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

	print(f"Steps: {solve(puzzle,goal)}")


if __name__ == '__main__':
	main()