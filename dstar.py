import heapq
from entry import Entry, Key
from graph import Graph
from typing import Tuple, List
from search_algorithm import SearchAlgorithm
from unittest import TestCase as test
    
class DStar(SearchAlgorithm):
    
    # G = Graph
    # S = G.GetVertices()
    # s = Current vertex
    # G.Cost(v1, v2) = Cost of path between vertices. ∞ cost represents no edge/wall.
    # G.GetAdjacent(s) = List of current vertex's predecessor and successor vertices
    # G.start = Start/AmongUs/SussyBaka
    # G.end = End/Vent/Imposter
    # g(s) = Estimated cost from start to current vertex

    # procedure Initialize()
    def __init__(self, G : Graph):
        self.G = G
        # U = fringe
        self.U = []
        # k_m accumulates heuristic
        self.k_m = 0
        self.rhs = {}
        self.g = {}
        self.recently_visited = []  # track recently visited nodes with frequency

        for s in self.G.GetVertices():
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        
        self.rhs[self.G.goal] = 0
        self.InsertIntoU(self.G.goal, self.CalculateKey(self.G.goal))

        self.last = self.G.start
    
    # our Hueristic is based on whether diagonal movement is allowed
    def heuristic(self, u1 : Tuple[int, int], u2 : Tuple[int, int]) -> float:
        # Chebyshev Distance
        if self.G.allow_diagonal_movement:
            return max(abs(u1[0] - u2[0]), abs(u1[1] - u2[1]))
        # Manhattan Distance
        else:
            return abs(u1[0] - u2[0]) + abs(u1[1] - u2[1])
    
    # procedure CalculateKey(s)
    def CalculateKey(self, s : Tuple[int, int]) -> Key:
        return Key(min(self.g[s], self.rhs[s]) + self.heuristic(self.G.start, s) + self.k_m, min(self.g[s], self.rhs[s]))
    
    # checks if s is in U
    def UContains(self, s : Tuple[int, int]) -> bool: 
        # create entry with dummy key
        return Entry(s, Key(-1, -1)) in self.U
    
    # inserts Entry (vertex and calculated key) into U
    def InsertIntoU(self, u : Tuple[int, int], calculated_key : Key) -> None:
        heapq.heappush(self.U, Entry(u, calculated_key))
    
    # removes s from U
    def RemoveFromU(self, s : Tuple[int, int]) -> None:
        # create entry with dummy key
        self.U.remove(Entry(s, Key(-1, -1)))
        heapq.heapify(self.U)
    
    # pops the top entry from U (assumes that it is nonempty)
    def PopFromU(self) -> Tuple[int, int]:
        return heapq.heappop(self.U)

    # procedure UpdateVertex(u)
    def UpdateVertex(self, u : Tuple[int, int]) -> None:
        if (u != self.G.goal):
            self.rhs[u] = min([float('inf')] + [self.G.GetCost(u, u_adjacent) + self.g[u_adjacent] for u_adjacent in self.G.GetTraversableAdjacent(u)])
        if (self.UContains(u)):
            self.RemoveFromU(u)
        if (self.g[u] != self.rhs[u]):
            self.InsertIntoU(u, self.CalculateKey(u))

    # procedure ComputeShortestPath()
    def ComputeShortestPath(self) -> None:
        # Process the priority queue until the shortest path is found
        while (self.U and self.U[0].key < self.CalculateKey(self.G.start) or self.rhs[self.G.start] != self.g[self.G.start]):
            top_entry = self.PopFromU()
            u = top_entry.s
            k_old = top_entry.key
            k_new = self.CalculateKey(u)
            if k_old < k_new:
                self.InsertIntoU(u, k_new)
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.G.GetAdjacent(u):
                    self.UpdateVertex(s)
            else:
                self.g[u] = float('inf')
                self.UpdateVertex(u)
                for s in self.G.GetAdjacent(u) + [u]:
                    self.UpdateVertex(s)

    def PickSuccessor(self) -> Tuple[int, int]:
        # pick the successor s' that minimizes c(s, s') + g(s')
        val = float('inf')
        min_s = None

        # Track the previous direction
        prev_direction = (self.G.start[0] - self.last[0], self.G.start[1] - self.last[1])

        # get traversable adjacent nodes to the current position
        for s in self.G.GetTraversableAdjacent(self.G.start):
            # introduce a dynamically increasing penalty for revisiting recently visited nodes
            # random ahh numbers
            revisit_penalty = 0.5 + 0.2 * (1.5 ** self.recently_visited.count(s)-1)
            
            # compute direction change penalty
            curr_direction = (s[0] - self.G.start[0], s[1] - self.G.start[1])
            direction_change_penalty = 0 if prev_direction == curr_direction else 0.5  # penalize direction changes
            
            curr_val = self.G.GetCost(self.G.start, s) + self.g[s] + revisit_penalty

            # break ties using the heuristic (closer to the goal is better)
            if curr_val < val or (curr_val == val and (min_s is None or self.heuristic(s, self.G.goal) < self.heuristic(min_s, self.G.goal))):
                val, min_s = curr_val, s

        # add the chosen successor to recently visited nodes
        self.recently_visited.append(min_s)
        if len(self.recently_visited) > 10:  # Limit the size of recently visited nodes
            self.recently_visited.pop(0)  # Remove the oldest entry to maintain a sliding window

        return min_s
    
    def AdaptToChanges(self, changed_edges : List[Tuple[int, int]]) -> Tuple[int, int]:
        self.k_m +=  self.heuristic(self.last, self.G.start)    # update heuristic shift
        self.last = self.G.start

        # update affected vertices and neighbors
        affected_vertices = set()
        for e in changed_edges:
            for s, u in self.G.GetVerticesConnectedByEdge(e):
                affected_vertices.update([s, u])
                for (a, b) in [(s, u), (u, s)]:
                    if self.rhs[a] == self.G.GetCost(a, b) + self.g[b]:
                        if a != self.G.goal:
                            self.rhs[a] = min([float('inf')] + [self.G.GetCost(a, c) + self.g[c] for c in self.G.GetAdjacent(a)])
                    self.UpdateVertex(a)
        
        # only recompute path if a significant change occurred
        if len(affected_vertices) > 5:  # threshold for significant change
            for vertex in affected_vertices:
                for neighbor in self.G.GetAdjacent(vertex):
                    self.UpdateVertex(neighbor)
            self.ComputeShortestPath()