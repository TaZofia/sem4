import pandas as pd
import matplotlib.pyplot as plt

# Pliki i odpowiadające etykiety
files = {
    "ascending_insert": ("ascending_insert.csv", "Ascending Insert"),
    "random_insert": ("random_insert.csv", "Random Insert"),
    "random_delete_after_ascending_insert": ("random_delete_after_ascending_insert.csv", "Delete After Ascending"),
    "random_delete_after_random_insert": ("random_delete_after_random_insert.csv", "Delete After Random")
}

# Wczytywanie i grupowanie danych
data = {}
for key, (filename, label) in files.items():
    df = pd.read_csv(filename)
    grouped = df.groupby("n").mean(numeric_only=True).reset_index()
    data[key] = {"df": grouped, "label": label}

# Parametry do rysowania
metrics = {
    "comparisons": "Number of Comparisons",
    "pointer_ops": "Number of Pointer Operations",
    "height": "Tree Height"
}

# Funkcja rysująca wykres
def plot_metric(metric, value_type, title_suffix, filename_suffix):
    plt.figure(figsize=(10, 6))

    for insert_key, delete_key in [
        ("ascending_insert", "random_delete_after_ascending_insert"),
        ("random_insert", "random_delete_after_random_insert")
    ]:
        for key in [insert_key, delete_key]:
            df = data[key]["df"]
            label = data[key]["label"]
            y_col = metric if value_type == "avg" else f"max_{metric}"
            plt.plot(df["n"], df[y_col], label=f"{label} ({value_type})", marker='o')

    plt.title(f"{metrics[metric]} ({title_suffix})")
    plt.xlabel("n")
    plt.ylabel(metrics[metric])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{metric}_{filename_suffix}.png")
# Rysowanie wykresów
for metric in metrics:
    plot_metric(metric, "avg", "Average", "avg")
    plot_metric(metric, "max", "Maximum", "max")
