import math
import heapq
from graph import Graph
from dstar import DStar, Entry, Key

# TODO maze generation, maze updating, path reconstruction, visualization, creating maze (file or interactive)

n = ?
# create Graph
G = Graph(n)
G.SwapEndpoints()
dstar = DStar(G)
dstar.ComputeShortestPath()
while (G.start != G.goal):
    # no known path
    if dstar.rhs[G.start] == float('inf'):
        break
    G.start = min([G.Cost(s) + dstar.g[s] for s in G.Adjacent(G.start)])
    if Graph has changed:
        dstar.k_m = dstar.k_m + dstar.h(G.last, G.start)
        G.SwapEndpoints()
      
