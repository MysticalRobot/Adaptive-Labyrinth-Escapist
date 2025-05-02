from graph import Graph
from algorithms import algorithms

# TODO change algorithm name here
algorithm_name = 'd* lite'

# initialize graph and algorithm 
maze_to_recreate = '' # replace with 'previous_maze.txt' to use the last maze
G = Graph(n=10, allow_diagonal_movement=True, maze_to_recreate=maze_to_recreate)
algorithm = algorithms[algorithm_name](G)
with open('previous_maze.txt', 'w') as f:
    f.write(algorithm.G.GetRecreationInfo())
algorithm.ComputePath() 
print(algorithm.G)

# number of steps before graph changes
m_steps = 5
m = m_steps

while (algorithm.G.start != algorithm.G.goal):
    # pick a successor and move to it
    algorithm.G.MoveStart(algorithm.PickSuccessor())
    # m_steps have been made, so change the graph and make the algorithm adapt to it
    if m == 0:
        m = m_steps
        # changed_edges = algorithm.G.AddEdges() if G.randint(0, 1) else algorithm.G.RemoveEdges()
        changed_edges = algorithm.G.AddEdges()
        # changed_edges = algorithm.G.RemoveEdges()
        algorithm.AdaptToChanges(changed_edges)
    print(f'\n{algorithm.G}')
    m -= 1