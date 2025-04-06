import pandas as pd
import matplotlib.pyplot as plt
import os

current_dir = os.getcwd()
results_dir = os.path.join(current_dir, "resultsMS")
plots_dir = os.path.join(current_dir, "plotsMS")

ks = [100]

for k in ks:
    df_ms = pd.read_csv(os.path.join(results_dir, f"Results_ms_k{k}.csv"))
    df_mySort = pd.read_csv(os.path.join(results_dir, f"Results_mySort_k{k}.csv"))

    df_ms['algorithm'] = 'Merge Sort'
    df_mySort['algorithm'] = 'mySort'

    df_all = pd.concat([df_ms, df_mySort])

    averages = df_all.groupby(['n', 'algorithm']).agg({'comparisons': 'mean', 'swaps': 'mean'}).reset_index()

    plt.figure(figsize=(10, 6))
    for algorithm in averages['algorithm'].unique():
        subset = averages[averages['algorithm'] == algorithm]
        plt.plot(subset['n'], subset['swaps'] / subset['n'], linestyle='--', label=f'Swaps/n - {algorithm}', linewidth=2)
        plt.plot(subset['n'], subset['comparisons'] / subset['n'], linestyle='--', label=f'Cmp/n - {algorithm}', linewidth=2)
        

    plt.title(f'k{k}')
    plt.xlabel('n')
    plt.ylabel('Avg/n')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    #plt.show()

    plt.savefig(os.path.join(plots_dir, f"avg_per_n_k{k}.png"))


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
    #plt.show()

    plt.savefig(os.path.join(plots_dir, f"avg_k{k}.png"))
