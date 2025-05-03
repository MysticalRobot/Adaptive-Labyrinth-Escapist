from typing import Tuple
from statistics import median
import random
import time
from graph import Graph
from algorithms import algorithms

# TODO add/remove algorithm names from this list
algorithm_names = list(algorithms.keys())

# define range of n to gather data about
n_lo, n_hi, n_step = 2, 101, 1

# repeat each measurement this many times:
num_trials = 5

# use the same seed for all the algorithms to compare them on the exact same mazes
random_seed = random.randint(69, 420)
random.seed(random_seed)
    
def measure_performance(algorithm_name : str, graph_to_clone : Graph) -> Tuple[int, int]:
    # record execution time and path length
    execution_time = 0
    path_length = 0
    
    # cloned already generated maze and initialize algorithm
    G = Graph(random_seed=random_seed, graph_to_clone=graph_to_clone)
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
    m_steps = 5 + 10 * (G.n // 25)
    m = m_steps

    while (G.start != G.goal):
        path_length += 1

        # pick a successor and move to it
        start = time.time_ns()
        new_start = algorithm.PickSuccessor()
        end = time.time_ns()
        execution_time += end - start
        G.MoveStart(new_start)

        # m_steps have been made, so change the graph and allow the algorithm to adapt
        if m == 0:
            m = m_steps
            # changed_edges = G.AddEdges() if random.randint(0, 1) else G.RemoveEdges()
            changed_edges = G.AddEdges()
            # changed_edges = G.RemoveEdges()
            start = time.time_ns()
            algorithm.AdaptToChanges(changed_edges)
            end = time.time_ns()
            execution_time += end - start
        m -= 1
    
    return (execution_time, path_length)

with open('collected_data.csv', 'w') as out:
    # generate and write csv column headers
    header = 'n'
    for name in algorithm_names:
        header += f',{name} diag timing,{name} diag length,{name} no diag timing,{name} no diag length'
    out.write(f'{header}\n')
    # generate rows of data and write them immediately
    # regarding various graph sizes for each algorithm and movement setting
    for n in range(n_lo, n_hi, n_step):
        print(f'Measuring algorithm performance on mazes with n = {n} ...')
        data = [str(n)]
        # memoize maze generation (not even sure if this improves data collection time)
        diag_graph = Graph(n=n, allow_diagonal_movement=True, random_seed=random_seed)
        no_diag_graph = Graph(n=n, allow_diagonal_movement=False, random_seed=random_seed)
        for algorithm_name in algorithm_names: 
            for allow_diagonal_movement in True, False:
                execution_times, path_lengths = [], []
                for trial in range(0, num_trials):
                    execution_time, path_length = measure_performance(algorithm_name=algorithm_name, graph_to_clone=diag_graph if allow_diagonal_movement else no_diag_graph)
                    execution_times.append(execution_time)
                    path_lengths.append(path_length) # this number is probably constant across trials but whatever
                data.append(str(median(execution_times) * 10**(-9)))
                data.append(str(median(path_lengths)))
        out.write(f"{','.join(data)}\n")
print('Finished measuring algorithm performance...')
