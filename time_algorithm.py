import sys
import random
import time
from init_algorithm import initialize_algorithm

# seed random number generator
random_seed = int(sys.argv[3])
random.seed(random_seed)

# generate maze and initialize algorithm
algorithm_name = sys.argv[5]
init_time, algorithm = initialize_algorithm(algorithm_name=algorithm_name, n=int(sys.argv[1]), allow_diagonal_movement=True if sys.argv[2] == 'True' else False, random_seed=random_seed)
algorithm.ComputeShortestPath() 

# time initial path computation
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

while (algorithm.G.start != algorithm.G.goal):
    path_length += 1

    # pick a successor and move to it
    start = time.time_ns()
    new_start = algorithm.PickSuccessor()
    end = time.time_ns()
    move_making_times.append(end - start)
    algorithm.G.MoveStart(new_start)

    # m_steps have been made, so change the graph and allow the algorithm to adapt
    if m == 0:
        m = m_steps
        # changed_edges = G.AddEdges() if random.randint(0, 1) else G.RemoveEdges()
        changed_edges = algorithm.G.AddEdges()
        # changed_edges = G.RemoveEdges()
        start = time.time_ns()
        path = algorithm.AdaptToChanges(changed_edges)
        end = time.time_ns()
        adapting_to_changes_times.append(end - start)
    m -= 1

total_time = init_time + initial_compute_shortest_path_time + \
    sum(move_making_times) + sum(adapting_to_changes_times)
with open('algorithm_data.csv', 'a') as out:
    out.write(f'''{algorithm_name},{algorithm.G.old_n},{algorithm.G.allow_diagonal_movement},{m_steps},{total_time},{path_length}\n''')