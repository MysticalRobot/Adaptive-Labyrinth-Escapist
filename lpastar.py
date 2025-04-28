import heapq
from entry import Entry, Key
from graph import Graph
from typing import Tuple, List
from search_algorithm import SearchAlgorithm
from unittest import TestCase as test
    
class LifelongPlanningAStar(SearchAlgorithm):
    
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
        self.rhs = {}
        self.g = {}

        for s in self.G.GetVertices():
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        
        self.rhs[self.G.start] = 0
        self.InsertIntoU(self.G.start, self.CalculateKey(self.G.start))

        self.last = self.G.start
    
    # our Hueristic is based on whether diagonal movement is allowed
    def heuristic(self, u1 : Tuple[int, int], u2 : Tuple[int, int]) -> float:
        ''' sussy
        if not self.G.EdgeExists(self.G.GetEdge(u1, u2)):
            return float('inf')
        '''
        # Chebyshev Distance
        if self.G.allow_diagonal_movement:
            return max(abs(u1[0] - u2[0]), abs(u1[1] - u2[1]))
        # Manhattan Distance
        else:
            return abs(u1[0] - u2[0]) + abs(u1[1] - u2[1])
    
    # procedure CalculateKey(s)
    def CalculateKey(self, s : Tuple[int, int]) -> Key:
        return Key(min(self.g[s], self.rhs[s]) + self.heuristic(s, self.G.goal), min(self.g[s], self.rhs[s]))
    
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
        if (u != self.G.start):
            self.rhs[u] = min([self.G.GetCost(u, u_adjacent) + self.g[u_adjacent] for u_adjacent in self.G.GetAdjacent(u)])
        if (self.UContains(u)):
            self.RemoveFromU(u)
        if (self.g[u] != self.rhs[u]):
            self.InsertIntoU(u, self.CalculateKey(u))

    # procedure ComputeShortestPath()
    def ComputeShortestPath(self) -> None:
        '''
        vertex_expansion_count = {}
        last_key = None
        '''
        while (self.U and self.U[0].key < self.CalculateKey(self.G.goal) or self.rhs[self.G.goal] != self.g[self.G.goal]):
            top_entry = self.PopFromU()
            u = top_entry.s
            k = top_entry.key
            '''
            if last_key:
                test.assertTrue(expr=last_key < k)
            last_key = k
            '''
            if (self.g[u] > self.rhs[u]):
                self.g[u] = self.rhs[u]
                # TODO maybe change to GetTraversableAdjacent(u)
                for s in self.G.GetAdjacent(u):
                    self.UpdateVertex(s)
            else: 
                self.g[u] = float('inf')
                for s in self.G.GetAdjacent(u) + [u]:
                    self.UpdateVertex(s)

            '''
            # theorem 1
            if (u in vertex_expansion_count):
                vertex_expansion_count[u] += 1
            else:
                vertex_expansion_count[u] = 1
            '''

        '''    
        for vertex in vertex_expansion_count.keys():
            test.assertFalse(expr=vertex_expansion_count[vertex] > 2)
        '''

    def PickSuccessor(self) -> Tuple[int, int]:
        # pick the successor s' that minimizes c(s, s') + g(s')
        val, min_s = float('inf'), None
        # TODO maybe use G.GetTraversableAdjacent
        for s in self.G.GetAdjacent(self.G.start):
            curr_val = self.G.GetCost(self.G.start, s) + self.g[s] 
            if curr_val <= val:
                val, min_s = curr_val, s
        return min_s
    
    def AdaptToChanges(self, changed_edges : List[Tuple[int, int]]) -> Tuple[int, int]:
        for e in changed_edges:
            for s in self.G.GetVerticesConnectedByEdge(e):
                self.UpdateVertex(s)
        self.ComputeShortestPath()
