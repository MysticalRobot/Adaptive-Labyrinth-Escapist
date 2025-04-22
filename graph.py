class Graph:

    # Let us be schizophrenic
    # Graph = G
    # S = G.vertices
    # Current vertex = s
    # Cost of path between vertices = c(v1, v2). Infinity cost represents path to wall.
    # List of predecessor and successor vertices = G.Adjacent(s)
    # Start = g.start
    # End/Vent = g.end
    # Estimated cost from start to current = g(s)

    # n = number of rows and columns (nxn maze)
    def __init__(self, n):
        self.n = n
        self.maze = [[[0] * n] for row in range(n)]
        # still need to put down obstacles
        # self.start = start
        # self.goal = goal

    # swap the start and end points
    def SwapEndpoints(self) -> None:
        temp = self.start
        self.start = self.end
        self.end = temp
    
    # returns a list of all the valid adjacent vertices
    def Adjacent(self, s) -> list:
        adj = []
        for i in -1, 0, 1:
            for j in -1, 0, 1:
                if i == 0 and j == 0:
                    continue
                if s[0] + i >= 0 and s[0] + i < self.n and s[1] + j >= 0 and s[1] + j < self.n:
                    adj.append((s[0] + i, s[1] + j))
        return adj

    # returns 1 if the spot can be traversed, inf otherwise
    def Cost(self, u) -> float:
        if self.maze[u[0]][u[1]] == -1:
            return float('inf')
        else:
            return 1