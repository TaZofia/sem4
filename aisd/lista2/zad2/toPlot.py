import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

def run_test(sort_program, generator, n, k):
    comparisons, swaps = [], []
    for _ in range(k):
        cmd = f"{generator} {n} | {sort_program}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
        lines = result.stdout.strip().split("\n")

        for line in result.stdout.splitlines():
            if line.startswith("# of comparisons:"): 
                cmp = int(line.removeprefix("# of comparisons:").strip())
            if line.startswith("# of swaps:"):
                swp = int(line.removeprefix("# of swaps:").strip())  

        comparisons.append(cmp)
        swaps.append(swp)
    return np.mean(comparisons), np.mean(swaps)

def plot_results(results, ns, ylabel, title, filename):
    plt.figure()
    for algo, values in results.items():
        plt.plot(ns, values, label=algo, marker='o')
    plt.xlabel("Rozmiar n")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.savefig(filename)

def main():

    zad1_path = r"K:\studia\sem4\aisd\lista2\zad1"

    generators = {
        "random": os.path.join(zad1_path, "randomGen.exe"),
        "sorted": os.path.join(zad1_path, "ascendingGen.exe"),
        "reversed": os.path.join(zad1_path, "descendingGen.exe")
    }
    algorithms = {
        "Insertion Sort": os.path.join(zad1_path, "insertionSort.exe"),
        "Quick Sort": os.path.join(zad1_path, "quickSort.exe"),
        "Hybrid Sort": os.path.join(zad1_path, "hybrid.exe"),
    }
    ns_small = list(range(10, 51, 10))            
    ns_large = list(range(1000, 50001, 1000))
    ks = [1, 10, 100]
    
    for k in ks:
        results_cmp, results_swp = {a: [] for a in algorithms}, {a: [] for a in algorithms}
        
        for n in ns_small:
            for algo, prog in algorithms.items():
                cmp, swp = run_test(prog, generators["random"], n, k)
                results_cmp[algo].append(cmp)
                results_swp[algo].append(swp)
        
        plot_results(results_cmp, ns_small, "Średnia liczba porównań", f"Porównania dla k={k}", f"comparisons_k{k}.png")
        plot_results(results_swp, ns_small, "Średnia liczba przestawień", f"Przestawienia dla k={k}", f"swaps_k{k}.png")
        
        for algo in ["Quick Sort", "Hybrid Sort"]:
            results_cmp[algo], results_swp[algo] = [], []
            for n in ns_large:
                cmp, swp = run_test(algorithms[algo], generators["random"], n, k)
                results_cmp[algo].append(cmp / n)
                results_swp[algo].append(swp / n)
            
        plot_results(results_cmp, ns_large, "c/n", f"Iloraz porównań dla k={k}", f"cmp_ratio_k{k}.png")
        plot_results(results_swp, ns_large, "s/n", f"Iloraz przestawień dla k={k}", f"swp_ratio_k{k}.png")

if __name__ == "__main__":
    main()


