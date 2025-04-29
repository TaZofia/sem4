import pandas as pd
import matplotlib.pyplot as plt
import os

# Ścieżki
zad5_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad5"
results_path = os.path.join(zad5_path, "results")
plots_path = os.path.join(zad5_path, "plots")

# Parametry
alg_groups = {
    'qs': ('qs', 'qs_select'),
    'dpqs': ('dpqs', 'dpqs_select')
}
alg_labels = {
    'qs': 'QuickSort',
    'qs_select': 'QuickSort + Select',
    'dpqs': 'DualPivot QS',
    'dpqs_select': 'DualPivot QS + Select'
}
data_types = ['ascending', 'descending', 'random']
metrics = {
    'comparisons': {'ylabel': 'Average Comparisons', 'filename_suffix': 'comparisons'},
    'execution_time': {'ylabel': 'Average Time (s)', 'filename_suffix': 'time'}
}

def load_data(alg_name, data_type):
    file_path = os.path.join(results_path, f"Results_{alg_name}_{data_type}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.groupby('n', as_index=False).mean()
    else:
        print(f"[Brak pliku] {file_path}")
        return None

for group_key, (alg1, alg2) in alg_groups.items():
    for data_type in data_types:
        for metric, meta in metrics.items():
            plt.figure(figsize=(10, 6))

            for alg in (alg1, alg2):
                df = load_data(alg, data_type)
                if df is not None:
                    plt.plot(
                        df['n'], df[metric],
                        label=alg_labels[alg],
                        marker='o', linewidth=2
                    )

            plt.title(f"{meta['ylabel']} - {group_key.upper()} - {data_type.capitalize()} Data", fontsize=14)
            plt.xlabel("Input Size (n)", fontsize=12)
            plt.ylabel(meta['ylabel'], fontsize=12)
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()

            filename = f"{group_key}_{data_type}_{meta['filename_suffix']}.png"

            save_path = os.path.join(plots_path, filename)
            plt.savefig(save_path, dpi=300)
            plt.close()