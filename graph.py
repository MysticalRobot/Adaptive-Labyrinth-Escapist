class Graph:

    # Let us be schizophrenic
    # Graph = G
    # S = G.vertices
    # Current vertex = s
    # Cost of path between vertices = c(v1, v2). Infinity cost represents path to wall.
    # List of predecessor vertices = G.Pred(S)
    # List of sucessor vertices = G.Succ(S)
    # Start = g.start
    # End/Vent = g.end
    # Estimated cost from start to current = g(s)

    # n = number of rows and columns (nxn maze)
    def __init__(n=-1, graphpy=''):
        self.graph = graph
        self.start = start
        self.goal = goal

class Vertex:

    def __init__(row, col):
        self.row = row
        self.col = col