import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import numpy as np

current_dir = os.getcwd()
results_dir = os.path.join(current_dir, "results")
plots_dir = os.path.join(current_dir, "plotsDualPivotQSAndQS")

ks = [100]

for k in ks:
    df_dpqs = pd.read_csv(os.path.join(results_dir, f"Results_dpqs_k{k}.csv"))
    df_qs = pd.read_csv(os.path.join(results_dir, f"Results_qs_k{k}.csv"))

    df_dpqs['algorithm'] = 'Dual Pivot Quick Sort'
    df_qs['algorithm'] = 'Quick Sort'

    df_all = pd.concat([df_dpqs, df_qs])

    averages = df_all.groupby(['n', 'algorithm']).agg({'comparisons': 'mean', 'swaps': 'mean'}).reset_index()

    plt.figure(figsize=(10, 6))
    for algorithm in averages['algorithm'].unique():
        subset = averages[averages['algorithm'] == algorithm]
        plt.plot(subset['n'], subset['swaps'] / subset['n'] / np.log2(subset['n']) , linestyle='--', label=f'Swaps/nlog2n - {algorithm}', linewidth=2)
        plt.plot(subset['n'], subset['comparisons'] / subset['n'] / np.log2(subset['n']), linestyle='--', label=f'Cmp/nlog2n - {algorithm}', linewidth=2)
        

    plt.title(f'k{k}')
    plt.xlabel('n')
    plt.ylabel('Avg/nlog2n')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig(os.path.join(plots_dir, f"Const_c_near_nlog2n_{k}.png"))

    '''
    plt.figure(figsize=(10, 6))
    for algorithm in averages['algorithm'].unique():
        subset = averages[averages['algorithm'] == algorithm]
        plt.plot(subset['n'], subset['swaps'], marker='o', label=f'Average Swaps - {algorithm}', linewidth=2)
        plt.plot(subset['n'], subset['comparisons'], marker='o', label=f'Average Comparisons - {algorithm}', linewidth=2)
        

    plt.title(f'k{k}')
    plt.xlabel('n')
    plt.ylabel('Avg')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig(os.path.join(plots_dir, f"avg_k{k}.png"))
    '''
