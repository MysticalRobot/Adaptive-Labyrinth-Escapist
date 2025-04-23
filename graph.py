import sys
import random as r
from typing import Tuple, List

class Graph:

    # Let us be schizophrenic
    # Graph = G
    # S = G.vertices
    # Current vertex = s
    # Cost of path between vertices = c(v1, v2). Infinity cost represents path to wall.
    # List of predecessor and successor vertices = G.Adjacent(s)
    # Start = g.start
    # End/Vent = g.end
    # Estimated cost from start to current = g(s)
    # start/goal are represented by 2 in the maze
    # vertices are 0 are at even row and col indices
    # edges are at odd row or col indices
    # edges with value 1 do no exist (walls)

    # n = number of rows and columns (nxn maze)
    # precondition: n > 1
    def __init__(self, n : int):
        self.old_n = n 
        self.n = self.old_n + self.old_n - 1
        self.maze = []
        # place walls at odd indices
        for row in range(self.n):
            if row & 1:
                self.maze.append([1] * self.n)
            else:
                self.maze.append([col & 1 for col in range(self.n)])
        # seed random number generator
        r.seed()
        # vertices are only at even indices
        vertex_indices = list(range(0, self.n, 2))
        # generate start and goal vertices
        self.start = (r.choice(vertex_indices), r.choice(vertex_indices))
        self.goal = (r.choice(vertex_indices), r.choice(vertex_indices))
        # mark start and end
        self.maze[self.start[0]][self.start[1]] = 2
        self.maze[self.goal[0]][self.goal[1]] = 2
        # knock down walls until the graph is connected
        visited = [[False] * self.n for _ in range(self.n)] 
        # (cheekily) increase the recursion limit to allow for larger maze generation
        sys.setrecursionlimit(10000) 
        self.RemoveEdges(self.start, visited)

    # returns string representation of maze
    def __str__(self) -> str:
        rows = [''.join([str(s) for s in row]) for row in self.maze]
        return '\n'.join(rows)

    # TODO knocks some walls down and returns the list of those edges
    # maybe mark new edges with value 3 or something for visualization
    def NewEdges(self) -> List[Tuple[int, int]]:
        raise NotImplementedError()
    
    # TODO raises some walls and returns the list of those edges
    # maybe mark removed edges with value 4 or something for visualization
    def RemovedEdges(self) -> List[Tuple[int, int]]:
        raise NotImplementedError()
    
    # moves the start to the provided location
    def MoveStart(self, new_start : Tuple[int, int]) -> None:
        self.maze[self.start[0]][self.start[1]] = 0
        self.start = new_start
        self.maze[self.start[0]][self.start[1]] = 2

    # returns the edge the two adjacent vertices
    def Edge(self, s : Tuple[int, int], u : Tuple[int, int]) -> Tuple[int, int]:
        return ((s[0] + u[0]) // 2, (s[1] + u[1]) // 2)

    # does DFS to remove walls until the graph is connected
    def RemoveEdges(self, s : Tuple[int, int], visited : List[List[bool]]) -> None:
        # mark current as visited
        visited[s[0]][s[1]] = True 
        # consider 4 adjacent vertices in random order
        choices = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        r.shuffle(choices)
        for i, j in choices:
            u = (s[0] + i, s[1] + j)
            # ensure index validity
            if u[0] < 0 or u[0] >= self.n or u[1] < 0 or u[1] >= self.n:
                continue
            # skip visited adjacent vertices
            if visited[u[0]][u[1]]:
                continue
            # remove wall if not visited
            row, col = self.Edge(s, u)
            self.maze[row][col] = 0
            # continue DFS
            self.RemoveEdges(u, visited)
    
    def Vertices(self) -> List[Tuple[int, int]]:
        vertices = []
        # only include even indices
        for i in range(0, self.n, 2):
            for j in range(0, self.n, 2):
                vertices.append((i, j))
        return vertices

    # returns a list of all the valid adjacent vertices
    def Adjacent(self, s : Tuple[int, int]) -> List[Tuple[int, int]]:
        adjacent = []
        # consider up to 8 adjacent vertices
        for i in -2, 0, 2:
            for j in -2, 0, 2:
                # skip over the current vertex
                if i == 0 and j == 0:
                    continue
                u = (s[0] + i, s[1] + j) 
                # ensure index validity
                if u[0] >= 0 and u[0] < self.n and u[1] >= 0 and u[1] < self.n:
                    adjacent.append(u)
        return adjacent

    # returns the edge cost between s and u
    def Cost(self, s : Tuple[int, int], u : Tuple[int, int]) -> float:
        row, col = self.Edge(s, u)
        # there is a wall between s and u (no edge between them)
        if self.maze[row][col] == 1:
            return float('inf')
        # same vertex
        elif s == u:
            return 0
        # there is an edge between s and u (no wall)
        else:
            return 1