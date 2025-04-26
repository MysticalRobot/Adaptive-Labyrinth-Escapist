import random as r
from graph import Graph
from dstar import DStar

# TODO (almost done): maze generation, visualization, maze updating
# TODO debug dstar, complete Procedure Main() (and integrate dstar into game.py), graph creation from text file input

# create Graph
G = Graph(n=20, allow_diagonal_movement=False)
last = G.start
dstar = DStar(G)
# print graph
print(G)
dstar.ComputeShortestPath()
# number of steps before graph changes
m = 5
while (G.start != G.goal):
    # might cause an error. if the condition is true, then there is no known path.
    if dstar.g[G.start] == float('inf'):
        break

    # pick the successor s' that minimizes c(s, s') + g(s')
    val, min_s = float('inf'), None
    # maybe use G.GetTraversableAdjacent
    for s in G.GetAdjacent(G.start):
        curr_val = G.GetCost(G.start, s) + dstar.g[s] 
        if curr_val <= val:
            val, min_s = curr_val, s
    # TODO min_s is sometimes None, but there should be at least 1 successor 
    G.MoveStart(min_s)
    print()
    print(G)
    if m == 0:
        m += 5
        # changed_edges = G.AddEdges() if G.randint(0, 1) else G.RemoveEdges()
        # changed_edges = G.AddEdges()
        changed_edges = G.RemoveEdges()
        dstar.k_m = dstar.k_m + dstar.heuristic(last, G.start)
        last = G.start
        for e in changed_edges:
            for s in G.GetVerticesConnectedByEdge(e):
                dstar.UpdateVertex(s)
        dstar.ComputeShortestPath()
    m -= 1