import pandas as pd
import matplotlib.pyplot as plt

# Wczytywanie danych
insert_df = pd.read_csv("random_insert.csv")
delete_df = pd.read_csv("random_delete_after_random_insert.csv")

# Grupowanie i liczenie średnich
insert_avg = insert_df.groupby("n").mean().reset_index()
delete_avg = delete_df.groupby("n").mean().reset_index()

# Parametry: metryki i etykiety
metrics = {
    "comparisons": "Number of Comparisons",
    "pointer_ops": "Number of Pointer Operations",
    "height": "Tree Height"
}

# Funkcja do rysowania wykresów
def plot(metric, value_type, title_suffix, filename_suffix):
    plt.figure(figsize=(10, 6))

    col = metric if value_type == "avg" else f"max_{metric}"

    plt.plot(insert_avg["n"], insert_avg[col], label="Random Insert", marker='o')
    plt.plot(delete_avg["n"], delete_avg[col], label="Delete After Random", marker='s')

    plt.title(f"{metrics[metric]} ({title_suffix})")
    plt.xlabel("n")
    plt.ylabel(metrics[metric])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"rand_{metric}_{filename_suffix}.png")
    plt.show()

# Rysowanie wykresów
for metric in metrics:
    plot(metric, "avg", "Average", "avg")
    plot(metric, "max", "Maximum", "max")
