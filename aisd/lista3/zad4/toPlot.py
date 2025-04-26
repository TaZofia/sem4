import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

folder_path = 'K:\\studia\\sem4\\aisd\\lista3\\zad4\\results'  
plots_dir = 'K:\\studia\\sem4\\aisd\\lista3\\zad4\\plots'  

os.makedirs(plots_dir, exist_ok=True)

# Find all CSV files
files = glob.glob(os.path.join(folder_path, '*.csv'))

# Assign labels manually based on file order (make sure they match correctly!)
labels = [
    'Near the beginning',  # file 0
    'Near the middle',     # file 1
    'Near the end',        # file 2
    'Non-existent element',# file 3
    'Random element'       # file 4
]

colors = ['red', 'blue', 'green', 'orange', 'purple']

# Load all datasets first
datasets = []
for file in files:
    df = pd.read_csv(file, header=None, names=['n', 'k', 'comparisons', 'execution_time'], dtype=str)
    df = df.apply(pd.to_numeric, errors='coerce')  # Force numeric
    datasets.append(df)

# Helper function to plot
def plot_metric(datasets_idx, metric, ylabel, filename_suffix, title, plot_log=False):
    plt.figure(figsize=(10, 6))
    
    # Plot each dataset
    for idx in datasets_idx:
        df = datasets[idx]
        avg = df.groupby('n')[metric].mean()
        plt.plot(avg.index, avg.values, label=labels[idx], color=colors[idx])

    # Plot log(n) line (log base 2) only for 'comparisons' metric
    if plot_log:
        for idx in datasets_idx:
            df = datasets[idx]
            n_values = df['n'].unique()  # Get unique values of n
            log_n = np.log2(n_values)  # Calculate log2(n)
            plt.plot(n_values, log_n, label=r'$\log_2(n)$', color='gray', linestyle='--', linewidth=1)

    # Plot settings
    plt.title(title)
    plt.xlabel('Array Size (n)')
    plt.ylabel(f'Average {ylabel}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, filename_suffix))
    plt.close()

# Now the six specific plots:

# 1. Comparisons: Random + Non-existent (with log(n))
plot_metric(
    [4, 3], 
    'comparisons', 
    'Number of Comparisons', 
    'comparisons_random_nonexistent.png',
    'Number of Comparisons',
    plot_log=True
)

# 2. Comparisons: Beginning + End (with log(n))
plot_metric(
    [0, 2], 
    'comparisons', 
    'Number of Comparisons', 
    'comparisons_beg_end.png',
    'Number of Comparisons',
    plot_log=True
)

# 3. Comparisons: Middle (with log(n))
plot_metric(
    [1], 
    'comparisons', 
    'Number of Comparisons', 
    'comparisons_middle.png',
    'Number of Comparisons',
    plot_log=True
)

# 4. Execution Time: Random + Non-existent (no log(n))
plot_metric(
    [4, 3], 
    'execution_time', 
    'Execution Time (seconds)', 
    'execution_time_random_nonexistent.png',
    'Execution Time',
    plot_log=False
)

# 5. Execution Time: Beginning + End (no log(n))
plot_metric(
    [0, 2], 
    'execution_time', 
    'Execution Time (seconds)', 
    'execution_time_beg_end.png',
    'Execution Time',
    plot_log=False
)

# 6. Execution Time: Middle (no log(n))
plot_metric(
    [1], 
    'execution_time', 
    'Execution Time (seconds)', 
    'execution_time_middle.png',
    'Execution Time',
    plot_log=False
)
