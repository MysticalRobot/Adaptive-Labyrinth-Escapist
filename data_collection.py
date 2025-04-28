import os

# clear old timing data, generate csv column headers
with open('algorithm_data.csv', 'w') as out:
    out.write('algorithm,n (maze size),diagonal movement allowed,m (steps before change in maze),time (ns),path length')

# use the same seed for all the algorithms to compare them on the exact same mazes
random_seed = 69
# parametrize the number of steps before the mazes change 
m = 5

# for each algorithm and movement setting
for algorithm in ['dstar', 'bfs']: # TODO add additional algorithm names here 
    for allow_diagonal_movement in [True, False]:
        # try various graph sizes, 10 times each
        for n in [10, 50, 100]:
            for trial in range(0, 10):
                # TODO may have to change python3 to whatever works for your machine
                # run implementation each (which will record its own time)
                os.system(f'python3 time_algorithm.py {n} {allow_diagonal_movement} {random_seed} {m} {algorithm}')