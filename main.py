from graph import Graph
from dstar import DStar

# initialize graph and dstar
maze_to_recreate = '' # replace with 'current_maze.txt' to use the last maze
G = Graph(n=2, allow_diagonal_movement=False, maze_to_recreate=maze_to_recreate)
with open('current_maze.txt', 'w') as f:
    f.write(G.GetRecreationInfo())
dstar = DStar(G)
dstar.ComputeShortestPath() 
print(G)

# number of steps before graph changes
m_steps = 5
m = m_steps

while (G.start != G.goal):
    # pick a successor and move to it
    G.MoveStart(dstar.PickSuccessor())
    # m_steps have been made, so change the graph and make dstar adapt to it
    if m == 0:
        m = m_steps
        # changed_edges = G.AddEdges() if G.randint(0, 1) else G.RemoveEdges()
        changed_edges = G.AddEdges()
        # changed_edges = G.RemoveEdges()
        dstar.AdaptToChanges(changed_edges)
    print(f'\n{G}')
    m -= 1