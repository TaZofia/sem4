import pandas as pd
import matplotlib.pyplot as plt
import os

zad3_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad3"
results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad3\\results"
plots_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad3\\plots"

# Ustawienia
algorithms = {'se': 'Select'}
data_types = ['random', 'ascending', 'descending']
stat_positions = {
    'firstStatPos': 'First Stat',
    'median': 'Median',
    # 'randomStatPos': 'Random Stat'
}
ks = [3, 5, 7, 9]
metrics = ['comparisons', 'swaps']

# Funkcja pomocnicza do wczytania danych i obliczenia średnich
def load_data(algorithm, k, data_type, stat_position):
    filename = os.path.join(results_path, f'Results_{algorithm}_{k}_{data_type}_{stat_position}.csv')
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df_mean = df.groupby('n', as_index=False)[['comparisons', 'swaps']].mean()
        return df_mean
    else:
        print(f"Plik {filename} nie istnieje.")
        return None

# Tworzenie wykresów
for data_type in data_types:
    for stat_key, stat_label in stat_positions.items():
        for metric in metrics:
            plt.figure(figsize=(12, 8))
            for k in ks:
                for alg_key, alg_name in algorithms.items():
                    df = load_data(alg_key, k, data_type, stat_key)
                    if df is not None:
                        plt.plot(
                            df['n'], df[metric],
                            label=f"k={k}",
                            marker='o', markersize=5,
                            linewidth=1.5
                        )

            metric_label = "Comparisons" if metric == 'comparisons' else "Swaps"
            plt.title(f"{metric_label} - {stat_label} - {data_type.capitalize()} Data", fontsize=16)
            plt.xlabel("n (Input Size)", fontsize=14)
            plt.ylabel(f"Average {metric_label}", fontsize=14)
            plt.legend(title="k", fontsize=10)
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.tight_layout()

            # Zapis wykresu
            plot_filename = f"{data_type}_{stat_key}_{metric}.png"
            plt.savefig(os.path.join(plots_path, plot_filename), dpi=300)
            plt.close()
