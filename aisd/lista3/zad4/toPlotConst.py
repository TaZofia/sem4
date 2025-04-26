import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

# Ścieżki do folderów
folder_path = 'K:\\studia\\sem4\\aisd\\lista3\\zad4\\results'  
plots_dir = 'K:\\studia\\sem4\\aisd\\lista3\\zad4\\plots'  

os.makedirs(plots_dir, exist_ok=True)

# Znajdź wszystkie pliki CSV
files = glob.glob(os.path.join(folder_path, '*.csv'))

# Etykiety ręcznie przypisane na podstawie kolejności plików
labels = [
    'Near the beginning',  # file 0
    'Near the middle',     # file 1
    'Near the end',        # file 2
    'Non-existent element',# file 3
    'Random element'       # file 4
]

colors = ['red', 'blue', 'green', 'orange', 'purple']

# Wczytaj wszystkie dane z plików
datasets = []
for file in files:
    df = pd.read_csv(file, header=None, names=['n', 'k', 'comparisons', 'execution_time'], dtype=str)
    df = df.apply(pd.to_numeric, errors='coerce')  # Wymuś numerowanie
    datasets.append(df)

# Funkcja do rysowania wykresów
def plot_metric(datasets_idx, metric, ylabel, filename_suffix, title, plot_log=False):
    plt.figure(figsize=(12, 8))  # Zwiększenie rozmiaru wykresu

    # Przetwarzaj dane dla każdego zestawu danych
    for idx in datasets_idx:
        df = datasets[idx]
        avg = df.groupby('n')[metric].mean()  # Średnia dla każdej wartości n
        avg = avg / np.log2(avg.index)  # Podziel przez logarytm o podstawie 2 z n
        plt.plot(avg.index, avg.values, label=labels[idx], color=colors[idx], linewidth=2)  # Zwiększ grubość linii

    # Ustawienia wykresu
    plt.title(title)
    plt.xlabel('Array Size (n)')
    plt.ylabel(f'Normalized {ylabel} (avg / log2(n))')
    plt.legend(loc='upper left', fontsize=12)
    plt.grid(True)
    
    # Ustawienie zakresu osi Y
    plt.ylim(0, 2)  # Ustawienie osi Y od 0 do 2
    
    # Zwiększenie rozdzielczości i oddalenie wykresu
    plt.tight_layout(pad=3.0)  # Zwiększamy odstępy, aby wykres był bardziej oddalony

    # Zapisz wykres do pliku
    output_path = os.path.join(plots_dir, filename_suffix)
    plt.savefig(output_path)
    print(f"Wykres zapisany jako: {output_path}")  # Informacja o zapisaniu pliku
    plt.close()

# Generujemy wykresy dla różnych typów wyszukiwania na trzech oddzielnych wykresach

# 1. Porównania: Beginning + End
plot_metric(
    [0, 2],  # Zestawy danych dla Beginning i End
    'comparisons', 
    'Comparisons', 
    'beg_end_comparisons.png',  # Zmieniona nazwa pliku
    'Comparisons (Beginning + End)',
    plot_log=False  # Nie używamy log(n) w tym przypadku
)

# 2. Porównania: Middle
plot_metric(
    [1],  # Zestaw danych dla Middle
    'comparisons', 
    'Comparisons', 
    'middle_comparisons.png',  # Zmieniona nazwa pliku
    'Comparisons (Middle)',
    plot_log=False  # Nie używamy log(n) w tym przypadku
)

# 3. Porównania: Random In + Random Out
plot_metric(
    [4, 3],  # Zestawy danych dla Random In i Random Out
    'comparisons', 
    'Comparisons', 
    'random_in_out_comparisons.png',  # Zmieniona nazwa pliku
    'Comparisons (Random In + Random Out)',
    plot_log=False  # Nie używamy log(n) w tym przypadku
)
