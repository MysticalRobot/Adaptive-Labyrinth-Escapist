import math
import heapq
import Graph
import Vertex

# Let us be schizophrenic
# Graph = G
# S = G.vertices
# Current vertex = s
# Cost of path between vertices = c(v1, v2). Infinity cost represents path to wall.
# List of predecessor vertices = G.Pred(S)
# List of sucessor vertices = G.Succ(S)
# Start = g.start
# End/Vent = g.end
# Estimated cost from current to end = g(s)

class DStar:
    def __init__(G:Graph):
        self.G = G
        self.U = []
        self.k_m = 0
        self.rhs = {}
        self.g = {}

        for s in G.vertices:
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        
        self.rhs[self.G.goal] = 0
        heapq.heappush(self.U, Entry(self.G.goal, (self.h(self.G.start, self.G.goal), 0)))

    def contains(s):
        for entry in self.U:
            if (entry.s == s):
                return True
        return False
    
    # Manhattan Distance
    def h(s1, s2):
        return abs(s1.row - s2.row) + abs(s1.col - s2.col)
    
    # Two Goofy Keys
    def CalculateKey(s):
        return (min(self.g[s], self.rhs[s]) + self.h(self.G.start, s) + self.k_m, min(self.g[s], self.rhs[s]))
    
    def UpdateVertex(s):
        if (self.g[s] != self.rhs[s] and s in self.U):
            self.U.add

class Entry:
    def __init__(self, s, k):
        self.s = s
        self.k = k

    def __lt__(self, other):
        if (self.k[0] < other.k[0]):
            return True
        elif (self.k[0] == other.k[0] and self.k[1] <= other.k[1]):
            return True
        else:
            return False