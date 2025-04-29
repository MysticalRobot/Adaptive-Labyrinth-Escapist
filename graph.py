import sys
import random
from typing import Tuple, List, Optional

class Graph():
    
    # constants for differentiating spots on the maze 
    # (all positive value so they print nicely)
    EMPTY_OR_EDGE = 0 # (normal vertex or no wall)
    ENDPOINT = 1 # (start or goal vertex)
    NEW_EDGE = 2 # (newly removed wall)
    NO_EDGE = 3 # (wall)
    REMOVED_EDGE = 4 # (newly added wall)

    # n = number of rows and columns (nxn maze)
    # precondition: n > 1
    def __init__(self, n : int=2, allow_diagonal_movement : bool=False, maze_to_recreate : str='', random_seed : Optional[int]=None):
        # seed random number generator
        if random_seed:
            random.seed(random_seed)
        # randomly generate maze
        if not maze_to_recreate:
            self.old_n = n
            self.n = self.old_n + self.old_n - 1 # even the maze isn't safe from inflation
            self.allow_diagonal_movement = allow_diagonal_movement
            self.maze = []
            # place walls at odd indices
            for row in range(self.n):
                if self.IsHorizontalWall(row):
                    self.maze.append([self.NO_EDGE] * self.n)
                else:
                    self.maze.append([self.NO_EDGE if self.IsVerticalWall(col) else self.EMPTY_OR_EDGE for col in range(self.n)])
            # vertices are only at even indices
            vertex_indices = list(range(0, self.n, 2))
            # generate start and goal vertices
            self.start = (random.choice(vertex_indices), random.choice(vertex_indices))
            self.goal = (random.choice(vertex_indices), random.choice(vertex_indices))
            # mark start and end
            self.maze[self.start[0]][self.start[1]] = self.ENDPOINT
            self.maze[self.goal[0]][self.goal[1]] = self.ENDPOINT
            # (cheekily) increase the recursion limit to allow for larger maze generation
            sys.setrecursionlimit(10000) 
            # knock down walls until the graph is connected
            visited = [[False] * self.n for _ in range(self.n)] 
            self.GenerateWalls(self.start, visited)
        # recreate given maze
        else:
            with open(maze_to_recreate, 'r') as maze:
                self.old_n = int(maze.readline())
                self.n = int(maze.readline())
                self.allow_diagonal_movement = bool(maze.readline())
                self.start = tuple(int(index) for index in maze.readline().split())
                self.goal = tuple(int(index) for index in maze.readline().split())
                self.maze = [[int(val) for val in row.strip()] for row in maze.readlines()]

    # returns string representation of maze
    def __str__(self) -> str:
        rows = [''.join([str(s) for s in row]) for row in self.maze]
        return '\n'.join(rows)
    
    # return a string containing all the information needed to easily recreate a maze
    def GetRecreationInfo(self) -> str:
        return f'{self.old_n}\n{self.n}\n{self.allow_diagonal_movement}\n{self.start[0]} {self.start[1]}\n{self.goal[0]} {self.goal[1]}\n{self}'

    # tries to remove walls near self.start by adding the edges that it returns
    def AddEdges(self) -> List[Tuple[int, int]]:
        new_edges = self.UpToKSomeWhatCloseEdges(5, select_existing_edges=False)
        # remove walls 
        for e in new_edges:
            self.maze[e[0]][e[1]] = self.NEW_EDGE
        return new_edges

    # tries to add walls near self.start by removing the edges that it returns
    def RemoveEdges(self) -> List[Tuple[int, int]]:
        removed_edges = []
        for e in self.UpToKSomeWhatCloseEdges(5, select_existing_edges=True):
            prev_value = self.maze[e[0]][e[1]]
            # try removing edge
            self.maze[e[0]][e[1]] = self.REMOVED_EDGE
            # if removing it disconnected the endpoints, restore the edge
            if not self.PathExists():
                self.maze[e[0]][e[1]] = prev_value
            # otherwise, keep it removed
            else:
                removed_edges.append(e)
        return removed_edges
    
    # returns up to k edges around self.start that may or may not exist
    def UpToKSomeWhatCloseEdges(self, k : int, select_existing_edges : bool) -> List[Tuple[int, int]]:
        edges = []
        # gather edges from a window surrounding self.start
        half_window_size = self.n // 2
        row_lo, row_hi = max(0, self.start[0] - half_window_size), min(self.n, self.start[0] + half_window_size)
        col_lo, col_hi = max(0, self.start[1] - half_window_size), min(self.n, self.start[1] + half_window_size)
        for row in range(row_lo, row_hi):
            for col in range(col_lo, col_hi):
                # skip vertices
                if not self.IsEdge((row, col)): 
                    continue
                # disregard diagonal edges if diagonal movement is disallowed
                if not self.allow_diagonal_movement and self.IsDiagonalEdge((row, col)):
                    continue
                # at one time, consider only either edges that do not exist (i.e. walls), or edges that do exist
                edge_exists = self.EdgeExists((row, col))
                if (not edge_exists and not select_existing_edges) or (edge_exists and select_existing_edges):
                    edges.append((row, col))
        # randomize the result
        random.shuffle(edges)
        return edges[:min(k, len(edges))]

    # returns a bool indicating whether a path between the start and goal exists via an iterative DFS
    def PathExists(self) -> bool:
        # consider edge case (common with small mazes)
        if self.start == self.goal:
            return True
        # track visited vertices
        visited = [[False] * self.n for _ in range(self.n)] 
        visited[self.start[0]][self.start[1]] = True
        # fringe stored with queue
        stack = [self.start]
        while stack:
            s = stack.pop()
            # consider the reachable adjacent vertices
            for u in self.GetTraversableAdjacent(s):
                # disregard visited vertices
                if visited[u[0]][u[1]]:
                    continue 
                # no need to look further if the goal has been reached
                elif u == self.goal:
                    return True
                # add unprocessed vertices to the fringe and set their parent
                else:
                    stack.append(u)
                    visited[u[0]][u[1]] = True
        # the goal was never reached
        return False
    
    # moves the start to the provided location
    def MoveStart(self, new_start : Tuple[int, int]) -> None:
        self.maze[self.start[0]][self.start[1]] = self.EMPTY_OR_EDGE
        self.start = new_start
        self.maze[self.start[0]][self.start[1]] = self.ENDPOINT

    # returns the edge between two adjacent vertices
    def GetEdge(self, s : Tuple[int, int], u : Tuple[int, int]) -> Tuple[int, int]:
        return ((s[0] + u[0]) // 2, (s[1] + u[1]) // 2)
    
    # determines if the given coordinate is an edge
    def IsEdge(self, e : Tuple[int, int]) -> bool:
        return (e[0] & 1) or (e[1] & 1)

    # determines if the given coordinate is a diagonal edge
    def IsDiagonalEdge(self, e : Tuple[int, int]) -> bool:
        return (e[0] & 1) and (e[1] & 1)
    
    # determines if there is a horizontal wall at row 
    def IsHorizontalWall(self, row : int) -> bool:
        return True if row & 1 else False
    
    # determines if there is a vertical wall at col
    def IsVerticalWall(self, col : int) -> bool:
        return True if col & 1 else False
    
    # returns the vertices that are connected by the given edge
    def GetVerticesConnectedByEdge(self, e : Tuple[int, int]) -> List[Tuple[int, int]]:
        pairs_of_vertices = []
        if self.IsDiagonalEdge(e):
            choices = [((e[0] - 1, e[1] -1), (e[0] + 1, e[1] + 1)), ((e[0] - 1, e[1] + 1), (e[0] + 1, e[1] -1))]
        elif self.IsHorizontalWall(e[0]):
            choices = [((e[0] - 1, e[1]), (e[0] + 1, e[1]))]
        else: # self.IsVerticalWall(e[1])
            choices = [((e[0], e[1] - 1), (e[0], e[1] + 1))]
        for s, u in choices: 
            if self.HasValidIndices(s) and self.HasValidIndices(u):
                pairs_of_vertices.append((s, u))
        return pairs_of_vertices

    # does DFS to remove walls until the graph is connected
    def GenerateWalls(self, s : Tuple[int, int], visited : List[List[bool]]) -> None:
        # mark current as visited
        visited[s[0]][s[1]] = True 
        # consider adjacent vertices in random order
        adjacent = self.GetAdjacent(s)
        random.shuffle(adjacent)
        for u in adjacent:
            # skip visited adjacent vertices
            if visited[u[0]][u[1]]:
                continue
            # remove wall (add edge) if not visited
            e = self.GetEdge(s, u)
            self.maze[e[0]][e[1]] = self.EMPTY_OR_EDGE
            # continue DFS
            self.GenerateWalls(u, visited)
    
    # returns a list of all the vertices in the graph
    def GetVertices(self) -> List[Tuple[int, int]]:
        vertices = []
        # only include even indices
        for i in range(0, self.n, 2):
            for j in range(0, self.n, 2):
                vertices.append((i, j))
        return vertices
    
    # returns true if the indices of the given point fit on the maze
    def HasValidIndices(self, point : Tuple[int, int]) -> bool:
        return point[0] >= 0 and point[0] < self.n and point[1] >= 0 and point[1] < self.n
    
    # returns a list of all the valid adjacent vertices
    def GetAdjacent(self, s : Tuple[int, int]) -> List[Tuple[int, int]]:
        adjacent = []
        # consider up to 4 adjacent vertices by default
        choices = [(-2, 0), (0, -2), (2, 0), (0, 2)]
        # additionally consider 4 diagonal vertices
        if self.allow_diagonal_movement:
            choices += [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for i, j in choices:
            u = (s[0] + i, s[1] + j) 
            # ensure index validity
            if self.HasValidIndices(u):
                adjacent.append(u)
        return adjacent

    # returns adjacent vertices that are connected by an edge (i.e. traversable)
    def GetTraversableAdjacent(self, s : Tuple[int, int]) -> List[Tuple[int, int]]:
        traversable_adjacent = []
        # loop through the current vertex's adjacents
        for adjacent in self.GetAdjacent(s):
            # check if an edge exists
            if (self.EdgeExists(self.GetEdge(s, adjacent))):
                traversable_adjacent.append(adjacent)
        return traversable_adjacent

    # tells whether the edge exists 
    # precondition: e[0] >= 0 and e[0] < self.n and e[1] >= 0 and e[1] < self.n:
    def EdgeExists(self, e : Tuple[int, int]) -> bool:
        return self.maze[e[0]][e[1]] == self.EMPTY_OR_EDGE or \
            self.maze[e[0]][e[1]] == self.NEW_EDGE

    # returns the edge cost between s and u
    def GetCost(self, s : Tuple[int, int], u : Tuple[int, int]) -> float:
        # there is a wall between s and u (no edge between them)
        if not self.EdgeExists(self.GetEdge(s, u)):
            return float('inf')
        # same vertex
        elif s == u:
            return 0
        # there is an edge between s and u (no wall)
        else:
            return 1