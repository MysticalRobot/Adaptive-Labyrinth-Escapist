import heapq
from graph import Graph
from typing import Tuple

class Key:
    def __init__(self, k1, k2):
        self.k1 = k1
        self.k2 = k2

    def __lt__(self, other):
        if (self.k1 < other.k1):
            return True
        elif (self.k1 == other.k1 and self.k2 <= other.k2):
            return True
        else:
            return False
        
    def __str__(self):
        return f'({self.k1}, {self.k2})'
    
    def __repr__(self):
        return str(self)

class Entry:
    def __init__(self, s, k : Key):
        self.s = s
        self.k = k

    def __lt__(self, other):
        self.k < other.k

    def __eq__(self, other):
        return self.s == other.s
    
    def __str__(self):
        return f'[{self.s}, {self.k}]'
    
    def __repr__(self):
        return str(self)
    
class DStar:
    # procedure Initialize()
    def __init__(self, G : Graph):
        self.G = G
        self.U = []
        self.k_m = 0
        self.rhs = {}
        self.g = {}

        # maybe change this to only a few vertices
        for s in self.G.Vertices():
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
        for entry in self.U:
            if (entry.s == s):
                return True
        return False
    
    # removes s from U
    def Remove(self, s : Tuple[int, int]) -> None:
        # create entry with dummy key
        self.U.remove(Entry(s, Key(-1, -1)))
        heapq.heapify(self.U)
    
    # procedure UpdateVertex(s)
    def UpdateVertex(self, s : Tuple[int, int]) -> None:
        if (self.Contains(s)):
            self.Remove(s)
        if (self.g[s] != self.rhs[s]):
            heapq.heappush(self.U, Entry(s, self.CalculateKey(s)))

    # procedure ComputeShortestPath()
    def ComputeShortestPath(self) -> None:
        while (self.U[0].k < self.CalculateKey(self.G.start) or self.rhs[self.G.start] > self.g[self.G.start]):
            s = self.U[0].s
            k_old = self.U[0].k
            k_new = self.CalculateKey(s)
            
            if (k_old < k_new):
                self.Remove(s)
                heapq.heappush(self.U, Entry(s, k_new))
            elif (self.g[s] > self.rhs[s]):
                self.g[s] = self.rhs[s]
                self.Remove(s)

                for u in self.G.Adjacent(s):
                    if (u != self.G.goal):
                        self.rhs[u] = min(self.rhs[u], self.G.Cost(u, s), + self.g[s])
                        self.UpdateVertex(u)
            else:
                g_old = self.g[s]
                self.g[s] = float('inf')
                
                # the local neighborhood— everything around the vertex, including itself
                s_and_adjacents = [s] + self.G.Adjacent(s)
                for u in s_and_adjacents:
                    if (self.rhs[u] == self.G.Cost(u, s) + g_old):
                        if (u != self.G.goal):
                            self.rhs[u] = min([self.G.Cost(u, u_adj) + self.g[u_adj] for u_adj in self.G.Adjacent(u)])
                    self.UpdateVertex(u)