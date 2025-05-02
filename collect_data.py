from typing import Tuple
import random
import time
from graph import Graph
from algorithms import algorithms

# TODO add/remove algorithm names from this list
algorithm_names = list(algorithms.keys())

# use the same seed for all the algorithms to compare them on the exact same mazes
random_seed = 69
random.seed(random_seed)

def measure_performance(algorithm_name : str, n : int, allow_diagonal_movement : bool) -> Tuple[int, int]:
    # record execution time and path length
    execution_time = 0
    path_length = 0
    
    # generate maze and initialize algorithm
    G = Graph(n=n, allow_diagonal_movement=allow_diagonal_movement, random_seed=random_seed)
    start = time.time_ns()
    algorithm = algorithms[algorithm_name](G)
    end = time.time_ns()
    execution_time = end - start

    # time initial path computation
    start = time.time_ns()
    algorithm.ComputePath() 
    end = time.time_ns()
    execution_time += end - start

    # parametrize the number of steps before the mazes change 
    m_steps = 5
    m = m_steps

    while (algorithm.G.start != algorithm.G.goal):
        path_length += 1

        # pick a successor and move to it
        start = time.time_ns()
        new_start = algorithm.PickSuccessor()
        end = time.time_ns()
        execution_time += end - start
        algorithm.G.MoveStart(new_start)

        # m_steps have been made, so change the graph and allow the algorithm to adapt
        if m == 0:
            m = m_steps
            # changed_edges = G.AddEdges() if random.randint(0, 1) else G.RemoveEdges()
            changed_edges = algorithm.G.AddEdges()
            # changed_edges = G.RemoveEdges()
            start = time.time_ns()
            algorithm.AdaptToChanges(changed_edges)
            end = time.time_ns()
            execution_time += end - start
        m -= 1
    
    return (execution_time, path_length)

# define range of n to gather data about
n_lo, n_hi, n_step = 2, 13, 5

# repeat each measurement this many times:
num_trials = 5

# generate rows of data
data = [[str(n)] for n in range(n_lo, n_hi, n_step)]
# for each algorithm and movement setting:
for algorithm_name in algorithm_names: 
    for allow_diagonal_movement in [True, False]:
        # track the index of the row where the data should be added
        i = 0
        # try various graph sizes
        for n in range(n_lo, n_hi, n_step):
            execution_times, path_lengths = 0, 0
            for trial in range(0, num_trials):
                execution_time, path_length = measure_performance(algorithm_name=algorithm_name, n=n, allow_diagonal_movement=allow_diagonal_movement)
                execution_times += execution_time
                path_lengths += path_length # this number is probably constant across trials but whatever
            data[i].append(str(execution_times // num_trials))
            data[i].append(str(path_lengths // num_trials))
            i += 1

with open('collected_data.csv', 'w') as out:
    # generate and write csv column headers
    header = 'n'
    for name in algorithm_names:
        header += f',{name} diag timing,{name} diag length,{name} no diag timing,{name} no diag length'
    out.write(f'{header}\n')
    # write each row of data
    for row in data:
        out.write(f"{','.join(row)}\n")