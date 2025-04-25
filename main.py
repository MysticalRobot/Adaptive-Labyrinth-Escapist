from graph import Graph
from dstar import DStar

# TODO (almost done): maze generation, visualization, maze updating
# TODO debug dstar, complete Procedure Main() (and integrate dstar into game.py), graph creation from text file input

# create Graph
G = Graph(n=2, allow_diagonal_movement=False)
last = G.start
dstar = DStar(G)
# print graph
print(G)
dstar.ComputeShortestPath()
while (G.start != G.goal):
    # no known path
    if dstar.rhs[G.start] == float('inf'):
        break
    # pick the successor s' that minimizes c(s, s') + g(s')
    val, min_s = float('inf'), None
    for s in G.GetTraversableAdjacent(G.start):
        curr_val = G.GetCost(G.start, s) + dstar.g[s] 
        if curr_val <= val:
            val, min_s = curr_val, s
    # TODO min_s is sometimes None, but there should be at least 1 successor 
    G.MoveStart(min_s)
    print()
    print(G)