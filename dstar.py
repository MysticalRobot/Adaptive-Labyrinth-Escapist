import heapq
from entry import Entry, Key
from graph import Graph
from typing import Tuple
    
class DStar:
    # procedure Initialize()
    def __init__(self, G : Graph):
        self.G = G
        self.U = []
        self.k_m = 0
        self.rhs = {}
        self.g = {}

        # maybe change this to only a few vertices
        for s in self.G.GetVertices():
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        
        self.rhs[self.G.goal] = 0
        heapq.heappush(self.U, Entry(self.G.goal, Key(self.h(self.G.start, self.G.goal), 0)))
    
    # Our Hueristic: Manhattan Distance
    def h(self, s1 : Tuple[int, int], s2 : Tuple[int, int]) -> int:
        return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])
    
    # procedure CalculateKey(s)
    def CalculateKey(self, s : Tuple[int, int]) -> Key:
        return Key(min(self.g[s], self.rhs[s]) + self.h(self.G.start, s) + self.k_m, min(self.g[s], self.rhs[s]))
    
    # checks if s is in U
    def Contains(self, s : Tuple[int, int]) -> bool: 
        # create entry with dummy key
        return Entry(s, Key(-1, -1)) in self.U
    
    # removes s from U
    def Remove(self, s : Tuple[int, int]) -> None:
        # create entry with dummy key
        self.U.remove(Entry(s, Key(-1, -1)))
        heapq.heapify(self.U)
    
    # procedure UpdateVertex(s)
    def UpdateVertex(self, s : Tuple[int, int]) -> None:
        if (self.g[s] != self.rhs[s]):
            if (self.Contains(s)):
                self.Remove(s)
            heapq.heappush(self.U, Entry(s, self.CalculateKey(s)))
        elif (self.Contains(s)):
            self.Remove(s)

    # procedure ComputeShortestPath()
    def ComputeShortestPath(self) -> None:
        while (self.U[0].k < self.CalculateKey(self.G.start) or self.rhs[self.G.start] > self.g[self.G.start]):
            s = self.U[0].s
            k_old = self.U[0].k
            k_new = self.CalculateKey(s)
            
            if (self.g[s] > self.rhs[s]):
                self.g[s] = self.rhs[s]
                self.Remove(s)

                for u in self.G.GetAdjacent(s):
                    if (u != self.G.goal):
                        self.rhs[u] = min(self.rhs[u], self.G.GetCost(u, s), + self.g[s])
                        self.UpdateVertex(u)
            elif (k_old < k_new):
                self.Remove(s)
                heapq.heappush(self.U, Entry(s, k_new))
            else:
                g_old = self.g[s]
                self.g[s] = float('inf')
                
                # the local neighborhood— everything around the vertex, including itself
                s_and_adjacents = [s] + self.G.GetAdjacent(s)
                for u in s_and_adjacents:
                    if (self.rhs[u] == self.G.GetCost(u, s) + g_old):
                        if (u != self.G.goal):
                            self.rhs[u] = min([self.G.GetCost(u, u_adj) + self.g[u_adj] for u_adj in self.G.GetAdjacent(u)])
                    self.UpdateVertex(u)