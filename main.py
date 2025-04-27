import sys
import random
import time
from graph import Graph
from dstar import DStar

# create Graph and seed random number generator from the command line arguments
random_seed = int(sys.argv[3])
random.seed(random_seed)
G = Graph(n=int(sys.argv[1]), allow_diagonal_movement=True if sys.argv[2] == 'True' else False, random_seed=random_seed)
# print(G)

# initialize dstar
start = time.time_ns()
dstar = DStar(G)
last = G.start
end = time.time_ns()

# times for the different components of the algorithm
init_time = end - start
compute_shortest_path_times = []
move_making_times = []
adapting_to_changes_times = []

start = time.time_ns()
dstar.ComputeShortestPath()
end = time.time_ns()
compute_shortest_path_times.append(end - start)

# number of steps before graph changes
m_steps = int(sys.argv[4])
m = m_steps

# record path length
path_length = 0

while (G.start != G.goal):
    path_length += 1
    start = time.time_ns()
    # TODO might cause an error. if the condition is true, then there is no known path.
    if dstar.g[G.start] == float('inf'):
        break

    # pick the successor s' that minimizes c(s, s') + g(s')
    val, min_s = float('inf'), None
    # maybe use G.GetTraversableAdjacent
    for s in G.GetAdjacent(G.start):
        curr_val = G.GetCost(G.start, s) + dstar.g[s] 
        if curr_val <= val:
            val, min_s = curr_val, s
    end = time.time_ns()
    move_making_times.append(end - start)

    # TODO min_s is sometimes None, but there should be at least 1 successor 
    G.MoveStart(min_s)
    if m == 0:
        m = m_steps
        # changed_edges = G.AddEdges() if G.randint(0, 1) else G.RemoveEdges()
        changed_edges = G.AddEdges()
        # changed_edges = G.RemoveEdges()
        start = time.time_ns()
        dstar.k_m = dstar.k_m + dstar.heuristic(last, G.start)
        last = G.start
        for e in changed_edges:
            for s in G.GetVerticesConnectedByEdge(e):
                dstar.UpdateVertex(s)
        end = time.time_ns()
        adapting_to_changes_times.append(end - start)
        
        start = time.time_ns()
        dstar.ComputeShortestPath()
        end = time.time_ns()
        compute_shortest_path_times.append(end - start)
    # print()
    # print(G)
    m -= 1

# total the times and record it
total_time = init_time + sum(compute_shortest_path_times) \
            + sum(move_making_times) + sum(adapting_to_changes_times) 
with open('timings.csv', 'a') as out:
    out.write(f'dstar, {G.old_n}, {G.allow_diagonal_movement}, {m_steps}, {total_time}, {path_length}\n')