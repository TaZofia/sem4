import pandas as pd
import matplotlib.pyplot as plt
import os

zad2_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad2"
results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad2\\results2"
plots_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad2\\plots"

# Ustawienia
algorithms = {'rs': 'Randomized Select', 'se': 'Select'}
data_types = ['random', 'ascending', 'descending']
stat_positions = {
    'firstStatPos': 'First Stat',
    'median': 'Median',
    'randomStatPos': 'Random Stat'
}
metrics = ['comparisons', 'swaps']
metric_styles = {
    'comparisons': {'linestyle': '-', 'label_suffix': ' (Comparisons)', 'color': 'blue'},
    'swaps': {'linestyle': '--', 'label_suffix': ' (Swaps)', 'color': 'green'}
}

# Funkcja pomocnicza do wczytania danych i obliczenia średnich
def load_data(algorithm, data_type, stat_position):
    filename = os.path.join(results_path, f'Results_{algorithm}_{data_type}_{stat_position}.csv')
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
        # Wykres dla comparisons
        plt.figure(figsize=(12, 8))
        for alg_key, alg_name in algorithms.items():
            df = load_data(alg_key, data_type, stat_key)
            if df is not None:
                plt.plot(
                    df['n'], df['comparisons'],
                    label=f"{alg_name} (Comparisons)",
                    marker='o', markersize=6,
                    linewidth=1.5,
                    color='blue' if alg_key == 'rs' else 'red'
                )

        plt.title(f"Comparisons - {stat_label} - {data_type.capitalize()} Data", fontsize=16)
        plt.xlabel("n (Input Size)", fontsize=14)
        plt.ylabel("Average Comparisons", fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        comparisons_filename = f"{data_type}_{stat_key}_comparisons.png"
        plt.savefig(os.path.join(plots_path, comparisons_filename), dpi=300)

        # Wykres dla swaps
        plt.figure(figsize=(12, 8))
        for alg_key, alg_name in algorithms.items():
            df = load_data(alg_key, data_type, stat_key)
            if df is not None:
                plt.plot(
                    df['n'], df['swaps'],
                    label=f"{alg_name} (Swaps)",
                    marker='o', markersize=6,
                    linewidth=1.5,
                    linestyle='--',
                    color='blue' if alg_key == 'rs' else 'red'
                )

        plt.title(f"Swaps - {stat_label} - {data_type.capitalize()} Data", fontsize=16)
        plt.xlabel("n (Input Size)", fontsize=14)
        plt.ylabel("Average Swaps", fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        swaps_filename = f"{data_type}_{stat_key}_swaps.png"
        plt.savefig(os.path.join(plots_path, swaps_filename), dpi=300)
