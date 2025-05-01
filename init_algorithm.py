
import time
from typing import Optional, Tuple
from graph import Graph
from search_algorithm import SearchAlgorithm
from dstarlite import DStarLite
from bfs import BFS

def initialize_algorithm(algorithm_name : str, n : int=2, allow_diagonal_movement : bool=False, maze_to_recreate : str='', random_seed : Optional[int]=None) -> Tuple[int, SearchAlgorithm]:
    # generate maze
    G = Graph(n=n, allow_diagonal_movement=allow_diagonal_movement, maze_to_recreate=maze_to_recreate, random_seed=random_seed)
    # decide on algorithm
    if algorithm_name == 'd* lite':
        start = time.time_ns()
        algorithm = DStarLite(G)
        end = time.time_ns()
    elif algorithm_name == 'bfs':
        start = time.time_ns()
        algorithm = BFS(G)
        end = time.time_ns()
    # TODO handle additional algorithms here
    else:
        'zehahahaha mugiwara'
    return ((end - start), algorithm)
