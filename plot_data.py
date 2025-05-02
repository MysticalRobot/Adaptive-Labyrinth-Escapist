import matplotlib.pyplot as plt
import pandas as pd
from algorithms import algorithms

# TODO add/remove algorithm names from this list
algorithm_names = list(algorithms.keys())

# create a dataframe to easily handle the csv data
data = pd.read_csv('collected_data.csv', index_col='n')

# plot execution times with diagonal movement allowed
plot = data[[f'{name} diag timing' for name in algorithm_names]].plot()
plot.set(ylabel='time (s)', xlabel='n (number of rows and columns of vertices)', title='Execution times with diagonal movement allowed')
plot.legend(algorithm_names)
plot.get_figure().savefig(fname='plots/diag_timing.png')

# plot path lengths with diagonal movement allowed
plot = data[[f'{name} diag length' for name in algorithm_names]].plot()
plot.set(ylabel='path length (from start vertex to goal vertex)', xlabel='n (number of rows and columns of vertices)', title='Path lengths with diagonal movement allowed')
plot.legend(algorithm_names)
plot.get_figure().savefig(fname='plots/diag_length.png')

# plot execution times with diagonal movement not allowed
plot = data[[f'{name} no diag timing' for name in algorithm_names]].plot()
plot.set(ylabel='time (s)', xlabel='n (number of rows and columns of vertices)', title='Execution times with diagonal movement not allowed')
plot.legend(algorithm_names)
plot.get_figure().savefig(fname='plots/no_diag_timing.png')

# plot path lengths with diagonal movement not allowed
plot = data[[f'{name} no diag length' for name in algorithm_names]].plot()
plot.set(ylabel='path length (from start vertex to goal vertex)', xlabel='n (number of rows and columns of vertices)', title='Path lengths with diagonal movement not allowed')
plot.legend(algorithm_names)
plot.get_figure().savefig(fname='plots/no_diag_length.png')

# show the plot
plt.show()