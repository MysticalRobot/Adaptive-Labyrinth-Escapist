import sys
import random as r
from collections import deque
from typing import Tuple, List

class Graph:

    # Let us be schizophrenic
    # Graph = G
    # S = G.vertices
    # Current vertex = s
    # Cost of path between vertices = c(v1, v2). Infinity cost represents path to wall.
    # List of predecessor and successor vertices = G.Adjacent(s)
    # Start/Amongus/Sussy/Baka = g.start
    # End/Vent = g.end
    # Estimated cost from start to current = g(s)
    
    # edges are at odd row or col indices

    # constants for differentiating spots on the maze 
    # (all positive value so they print nicely)
    EMPTY_OR_EDGE = 0
    ENDPOINT = 1 # (start or goal vertices)
    NEW_EDGE = 2 # (newly removed wall)
    NO_EDGE = 3 # (wall)
    REMOVED_EDGE = 4 # (newly added wall)

    # n = number of rows and columns (nxn maze)
    # precondition: n > 1
    def __init__(self, n : int, allow_diagonal_movement : bool):
        self.old_n = n 
        self.n = self.old_n + self.old_n - 1
        self.allow_diagonal_movement = allow_diagonal_movement
        self.maze = []
        # place walls at odd indices
        for row in range(self.n):
            if row & 1:
                self.maze.append([self.NO_EDGE] * self.n)
            else:
                self.maze.append([self.NO_EDGE if col & 1 else self.EMPTY_OR_EDGE for col in range(self.n)])
        # seed random number generator
        r.seed()
        # vertices are only at even indices
        vertex_indices = list(range(0, self.n, 2))
        # generate start and goal vertices
        self.start = (r.choice(vertex_indices), r.choice(vertex_indices))
        self.goal = (r.choice(vertex_indices), r.choice(vertex_indices))
        # mark start and end
        self.maze[self.start[0]][self.start[1]] = self.ENDPOINT
        self.maze[self.goal[0]][self.goal[1]] = self.ENDPOINT
        # knock down walls until the graph is connected
        visited = [[False] * self.n for _ in range(self.n)] 
        # (cheekily) increase the recursion limit to allow for larger maze generation
        sys.setrecursionlimit(10000) 
        self.GenerateWalls(self.start, visited)

    # returns string representation of maze
    def __str__(self) -> str:
        rows = [''.join([str(s) for s in row]) for row in self.maze]
        return '\n'.join(rows)

    # tries to remove walls near self.start by adding the edges that it returns
    def AddEdges(self) -> List[Tuple[int, int]]:
        # 9 because that is the size of the smallest maze being generated (2x2)
        new_edges = self.UpToKSomeWhatCloseEdges(5, edge_exists=False)
        # remove walls 
        for e in new_edges:
            self.maze[e[0]][e[1]] = self.NEW_EDGE
        return new_edges

    # tries to add walls near self.start by removing the edges that it returns
    def RemoveEdges(self) -> List[Tuple[int, int]]:
        removed_edges = []
        # 9 because that is the size of the smallest maze being generated (2x2)
        for e in self.UpToKSomeWhatCloseEdges(5, edge_exists=True):
            prev_value = self.maze[e[0]][e[1]]
            # try removing edge
            self.maze[e[0]][e[1]] = self.REMOVED_EDGE
            # if removing it disconnected the endpoints, restore the edge
            if not self.FindPath()[0]:
                self.maze[e[0]][e[1]] = prev_value
            # otherwise, keep it removed
            else:
                removed_edges.append(e)
        return removed_edges
    
    # returns up to k edges around self.start that may or may not exist
    def UpToKSomeWhatCloseEdges(self, k : int, edge_exists : bool) -> List[Tuple[int, int]]:
        edges = []
        # gather edges from a window surrounding self.start
        half_window_size = self.n // 2
        row_lo, row_hi = max(0, self.start[0] - half_window_size), min(self.n, self.start[0] + half_window_size)
        col_lo, col_hi = max(0, self.start[1] - half_window_size), min(self.n, self.start[1] + half_window_size)
        for row in range(row_lo, row_hi):
            for col in range(col_lo, col_hi):
                # skip vertices
                if not ((row & 1) + (col & 1)): 
                    continue
                # disregard diagonal edges if diagonal movement is disallowed
                if not self.allow_diagonal_movement and not ((row & 1) ^ (col & 1)):
                    continue
                # at one time, consider only either edges that do not exist (i.e. walls), or edges that do exist
                if ((self.maze[row][col] == self.NO_EDGE or self.maze[row][col] == self.REMOVED_EDGE) and not edge_exists) or \
                ((self.maze[row][col] == self.EMPTY_OR_EDGE or self.maze[row][col] == self.NEW_EDGE) and edge_exists):
                    edges.append((row, col))
        # randomize the result
        r.shuffle(edges)
        return edges[:min(k, len(edges))]

    # returns a bool indicating whether a path from the start to the goal was found and the path itself
    # finds the path using BFS
    def FindPath(self) -> Tuple[bool, List[Tuple[int, int]]]:
        path = []
        # consider edge case (common with small mazes)
        if self.start == self.goal:
            return (True, path) 
        # track visited vertices
        parent = [[(-1, -1)] * self.n for _ in range(self.n)] 
        # set the parent tree's root to be its own parent
        parent[self.goal[0]][self.goal[1]] = self.goal
        # fringe stored with queue
        q = deque([self.goal])
        while q:
            s = q.popleft()
            # consider the adjacent vertices
            for u in self.Adjacent(s):
                e = self.Edge(s, u)
                # disregard visited or unreachable vertices
                if parent[u[0]][u[1]] != (-1, -1) or self.maze[e[0]][e[1]] == self.NO_EDGE or \
                    self.maze[e[0]][e[1]] == self.REMOVED_EDGE:
                    continue 
                # add unprocessed vertices to the fringe and set their parent
                else:
                    q.append(u)
                    parent[u[0]][u[1]] = s
        # no path was found
        if parent[self.start[0]][self.start[1]] == (-1, -1):
            return (False, path)
        # reconstruct path from parent tree
        s = parent[self.start[0]][self.start[1]]
        while True:
            path.append(s)
            if parent[s[0]][s[1]] == s:
                break 
            s = parent[s[0]][s[1]] 
        return (True, path)
    
    # moves the start to the provided location
    def MoveStart(self, new_start : Tuple[int, int]) -> None:
        self.maze[self.start[0]][self.start[1]] = self.EMPTY_OR_EDGE
        self.start = new_start
        self.maze[self.start[0]][self.start[1]] = self.ENDPOINT

    # returns the edge the two adjacent vertices
    def Edge(self, s : Tuple[int, int], u : Tuple[int, int]) -> Tuple[int, int]:
        return ((s[0] + u[0]) // 2, (s[1] + u[1]) // 2)

    # does DFS to remove walls until the graph is connected
    def GenerateWalls(self, s : Tuple[int, int], visited : List[List[bool]]) -> None:
        # mark current as visited
        visited[s[0]][s[1]] = True 
        # consider adjacent vertices in random order
        adjacent = self.Adjacent(s)
        r.shuffle(adjacent)
        for u in adjacent:
            # skip visited adjacent vertices
            if visited[u[0]][u[1]]:
                continue
            # remove wall (add edge) if not visited
            e = self.Edge(s, u)
            self.maze[e[0]][e[1]] = self.EMPTY_OR_EDGE
            # continue DFS
            self.GenerateWalls(u, visited)
    
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
        # consider up to 4 adjacent vertices by default
        choices = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        # additionally consider 4 diagonal vertices
        if self.allow_diagonal_movement:
            choices += [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for i, j in choices:
            u = (s[0] + i, s[1] + j) 
            # ensure index validity
            if u[0] >= 0 and u[0] < self.n and u[1] >= 0 and u[1] < self.n:
                adjacent.append(u)
        return adjacent

    # returns the edge cost between s and u
    def Cost(self, s : Tuple[int, int], u : Tuple[int, int]) -> float:
        e = self.Edge(s, u)
        # there is a wall between s and u (no edge between them)
        if self.maze[e[0]][e[1]] == self.NO_EDGE or self.maze[e[0]][e[1]] == self.REMOVED_EDGE:
            return float('inf')
        # same vertex
        elif s == u:
            return 0
        # there is an edge between s and u (no wall)
        else:
            return 1