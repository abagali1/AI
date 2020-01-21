# AI Notes 9/5/19

### Depth First Search

Go all the way down the graph (up to the bottom)

If you don't find it at the leaf, then move up and look down the other side.

May give u a very long path to the node

![Example image](https://he-s3.s3.amazonaws.com/media/uploads/9fa1119.jpg)

### Breadth First Search

Look across each level at a time to find something. 

Mostly working with Breadth First Search in AI

Will give u shortest path to the node

![Example image](https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Breadth-first-tree.svg/1200px-Breadth-first-tree.svg.png)

Implementation Psuedo Code:
    
    # Based on slider puzzle
    
    # 1 2 3
    # 4 5 6      ==== represented as ====>   "12345678_"
    # 7 8 _
    
    def solve(puzzle, goal)
        if puzzle is goal
            finish up + exit
        
        parse_me = [puzzle]
        
        seen_items = {
            puzzle[0]: '' # <<< should point to the parent
        }
        
        while parse_me
            puzzle = next item from parse_me
            
            for all unseen neighbors (that is neighbos we haven't already analyzed) of puzzle
                if its the goal
                    finish up + exit
                
                add puzzle to seen_items
                
        report failure as puzzle is not solvable