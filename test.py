from graph import Graph

# simple check to see graph generation
G = Graph(n=2, allow_diagonal_movement=False)
print(G)
G.AddEdges()
print(G)
G.RemoveEdges()
print(G)