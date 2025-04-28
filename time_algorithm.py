import sys
import random
import time
from graph import Graph
from dstar import DStar
from bfs import BFS

# seed random number generator
random_seed = int(sys.argv[3])
random.seed(random_seed)

# create Graph 
G = Graph(n=int(sys.argv[1]), allow_diagonal_movement=True if sys.argv[2] == 'True' else False, random_seed=random_seed)

# decide on algorithm
algorithm_name = sys.argv[5]
if algorithm_name == 'dstar':
    start = time.time_ns()
    dstar = DStar(G)
    end = time.time_ns()
    init_time = end - start
    algorithm = dstar
elif algorithm_name == 'lpastar':
    start = time.time_ns()
    lpastar = LifelongPlanningAStar(G)
    end = time.time_ns()
    init_time = end - start
    algorithm = lpastar
elif algorithm_name == 'bfs':
    init_time = 0
    bfs = BFS(G)
    algorithm = bfs
# TODO handle additional algorithms here
else:
    'zehahahaha mugiwara'

start = time.time_ns()
algorithm.ComputeShortestPath() 
end = time.time_ns()
initial_compute_shortest_path_time = end - start

# times for the other components of the algorithm
move_making_times = []
adapting_to_changes_times = []

# number of steps before graph changes
m_steps = int(sys.argv[4])
m = m_steps

# record path length
path_length = 0

while (G.start != G.goal):
    path_length += 1

    # pick a successor and move to it
    start = time.time_ns()
    new_start = algorithm.PickSuccessor()
    end = time.time_ns()
    move_making_times.append(end - start)
    G.MoveStart(new_start)

    # m_steps have been made, so change the graph and allow the algorithm to adapt
    if m == 0:
        m = m_steps
        # changed_edges = G.AddEdges() if random.randint(0, 1) else G.RemoveEdges()
        changed_edges = G.AddEdges()
        # changed_edges = G.RemoveEdges()
        start = time.time_ns()
        path = algorithm.AdaptToChanges(changed_edges)
        end = time.time_ns()
        adapting_to_changes_times.append(end - start)
    m -= 1

total_time = init_time + initial_compute_shortest_path_time + \
    sum(move_making_times) + sum(adapting_to_changes_times)
with open('algorithm_data.csv', 'a') as out:
    out.write(f'''{algorithm_name},{G.old_n},{G.allow_diagonal_movement},{m_steps},{total_time},{path_length}\n''')