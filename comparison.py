import sys
import random
import time
from graph import Graph

# create Graph and seed random number generator from the command line arguments
random_seed = int(sys.argv[3])
random.seed(random_seed)
G = Graph(n=int(sys.argv[1]), allow_diagonal_movement=True if sys.argv[2] == 'True' else False, random_seed=random_seed)
# print(G)

# times for the different components of the algorithm
find_path_times = []
move_making_times = []

start = time.time_ns()
path = G.FindPath() 
end = time.time_ns()
find_path_times.append(end - start)

# number of steps before graph changes
m_steps = int(sys.argv[4])
m = m_steps

# record path length
path_length = 0

while (G.start != G.goal):
    path_length += 1
    start = time.time_ns()
    new_start = path.pop()
    end = time.time_ns()
    move_making_times.append(end - start)

    G.MoveStart(new_start)
    if m == 0:
        m = m_steps
        # changed_edges = G.AddEdges() if random.randint(0, 1) else G.RemoveEdges()
        changed_edges = G.AddEdges()
        # changed_edges = G.RemoveEdges()
        start = time.time_ns()
        path = G.FindPath()
        end = time.time_ns()
        find_path_times.append(end - start)
    # print()
    # print(G)
    m -= 1

total_time = sum(find_path_times) + sum(move_making_times)
with open('timings.csv', 'a') as out:
    out.write(f'bfs, {G.old_n}, {G.allow_diagonal_movement}, {m_steps}, {total_time}, {path_length}\n')