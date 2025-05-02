from collections import deque
from typing import Tuple, List
from graph import Graph
from search_algorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    
    def __init__(self, G : Graph):
        self.G = G
        self.path = None
        
    # computes and stores the shortest path from the goal to the start vertex
    def ComputePath(self) -> None:
        self.path = []
        # consider edge case (common with small mazes)
        if self.G.start == self.G.goal:
            return
        # track visited vertices
        parent = [[(-1, -1)] * self.G.n for _ in range(self.G.n)] 
        # set the parent tree's root to be its own parent
        parent[self.G.start[0]][self.G.start[1]] = self.G.start
        # fringe stored with queue
        queue = deque([self.G.start])
        while queue:
            s = queue.popleft()
            # consider the adjacent vertices
            for u in self.G.GetAdjacent(s):
                # disregard visited or unreachable vertices
                if parent[u[0]][u[1]] != (-1, -1) or not self.G.EdgeExists(self.G.GetEdge(s, u)):
                    continue 
                # add unprocessed vertices to the fringe and set their parent
                else:
                    queue.append(u)
                    parent[u[0]][u[1]] = s
                    # terminate search when path is found
                    if u == self.G.start:
                        break
        # no path was found
        if parent[self.G.goal[0]][self.G.goal[1]] == (-1, -1):
            return
        # reconstruct path from parent tree
        s = self.G.goal
        while parent[s[0]][s[1]] != s:
            self.path.append(s)
            s = parent[s[0]][s[1]] 

    # returns the next vertex along the path (from the start to the end)
    def PickSuccessor(self) -> Tuple[int, int]:
        # the path is generated in reverse, so the last one is the next one 
        return self.path.pop()
    
    # computes the path from scratch
    def AdaptToChanges(self, changed_edges : List[Tuple[int, int]]) -> None:
        self.ComputePath()