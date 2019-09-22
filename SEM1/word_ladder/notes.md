# AI Notes 9/12/19

# Graph Terms

A graph is a collection of vertices, some of which are linked by edges.

Vertex = Node

A node is an object

Edge = connection = link

If two nodes are connected they are adjacent

Path is a sequence of connected edges leading from one vertex to another (possibly the same vertex)

Path is a sequence of connected nodes

The distance between two vertices is the minimum number of edges between them

Neighbors of a vertex are all vertices that have a distance of one (NOT ITSELF)

Children are neighbors that are not parents

Degree of a vertex = number of neighbors a vertex has

Digraph = directed graph = a graph where the edges only go one way

A connected graph is a graph where you can get from one node to any other node

A connected component is a group of nodes connected by edges

A singleton is a vertex w/out any edges

Acyclic is a graph without any cycles
    ie. you can't start at a vertex and return to that vetex
    ie. no non-zero path from any vertex back to itself

A tree is an acyclic connected undirected graph
A tree's special vertex is the root
The root doesn't have parents

A complement of a graph is a graph where all the edges are replaced by no edges and all the no edges are replaced by edges
    A vertex connected to everyone becomes singleton
    A singleton becomes a vertex connected to everyone

N vertex graph could have at max n(n-1)÷2

# Next Lab

Given a list of words (1000s)
All have same length (five or six)
Read in a file
First arg is filename
A graph of with these words
Vertices are the words themselves

Two vertices are connected if the difference between the words is one letter

[Words list](https://academics.tjhsst.edu/compsci/ai/words.txt)

    # Tests and Testy are neighbors
               _
      0 1 2 3 | 4 |
              |   |
      T e s t | s |
      T e s t | y |
              |___|
      
      0 1 2          
      e a t
      a t e   <----- none are related
      t e a

The assignment:

First part
    
    just filename of words is argument
    report
        1) the number of words
        2) the number of edges
        3) the degree distribution list
            for ten vertexes, list size 10
            list[index] = number of vertices with index degrees
            only go up to highest non-zero
        4) Give an example word of 2nd highest degree
        5) Distribution of connected componenet sizes
            [# of singletons, connected components of size 2, ... of size 3, ...]
            only go up to highest non-zero
        
        
Second part

    filename of words and a word is an argument
    report