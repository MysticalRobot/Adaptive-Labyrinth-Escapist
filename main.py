from graph import Graph
from dstar import DStar

# TODO-NE: maze generation, visualization 
# TODO debugging dstar, maze updating, Procedure Main(), allow maze creation interactively

n = 2
# create Graph
G = Graph(n)
last = G.start
dstar = DStar(G)
# temporary addition for motivation 
# (so that at least the case that G.start == G.goal works)
i = 0
while (G.start != G.goal):
    if i == 0:
        dstar.ComputeShortestPath()
    # no known path
    if dstar.rhs[G.start] == float('inf'):
        break
    G.MoveStart(min([G.Cost(s) + dstar.g[s] for s in G.Adjacent(G.start)]))
    i += 1