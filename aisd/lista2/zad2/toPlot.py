import pandas as pd
import matplotlib.pyplot as plt
import os

current_dir = os.getcwd()
results_dir = os.path.join(current_dir, "results")
plots_dir = os.path.join(current_dir, "plots")

ks = [1, 10, 100]

for k in ks:
    #df_is = pd.read_csv(os.path.join(results_dir, f"Results_is_k{k}.csv"))
    df_qs = pd.read_csv(os.path.join(results_dir, f"Results_big_n_qs_k{k}.csv"))
    df_hs = pd.read_csv(os.path.join(results_dir, f"Results_big_n_hs_k{k}.csv"))

    #df_is = pd.read_csv(os.path.join(results_dir, "Results_test_the_best_switch_is_k5.csv"))
    #df_qs = pd.read_csv(os.path.join(results_dir, "Results_test_the_best_switch_qs_k5.csv"))

    #df_is['algorithm'] = 'Insertion Sort'
    df_qs['algorithm'] = 'Quick Sort'
    df_hs['algorithm'] = 'Hybrid Sort'

    df_all = pd.concat([df_qs, df_hs])

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

    plt.savefig(os.path.join(plots_dir, f"big_n_avg_per_n_k{k}.png"))


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

    plt.savefig(os.path.join(plots_dir, f"big_n_avg_k{k}.png"))
