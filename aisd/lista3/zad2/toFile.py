import subprocess
import os

def run_test(sort_program, generator, n, statPos):
    cmd = f"{generator} {n} {statPos} | {sort_program}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")

    cmp, swp = None, None
    for line in result.stdout.splitlines():
        if line.startswith("# of comparisons:"):
            cmp = int(line.removeprefix("# of comparisons:").strip())
        if line.startswith("# of swaps:"):
            swp = int(line.removeprefix("# of swaps:").strip())
    
    return cmp, swp

def main():
    zad1_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad1"
    results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad2\\results"

    generators = {
        "random": os.path.join(zad1_path, "randomGen.exe"),
        "ascending": os.path.join(zad1_path, "ascendingGen.exe"),
        "descending": os.path.join(zad1_path, "descendingGen.exe"),
    }
    algorithms = {
        "Select": (os.path.join(zad1_path, "select.exe"), "se"),
        "Randomized Select": (os.path.join(zad1_path, "randomizedSelect.exe"), "rs"),
    }
    
    ns = list(range(100, 50001, 100)) 
    statPos_options = {
        "m": "median",
        "r": "randomStatPos"
    }

    for gen_name, gen_path in generators.items():
        for algo_name, (prog, algo_short) in algorithms.items():
            for stat_code, stat_label in statPos_options.items():
                filename = os.path.join(results_path, f"Results_{algo_short}_{gen_name}_{stat_label}.csv")
                with open(filename, "w") as file:
                    file.write("n,m,comparisons,swaps\n")
                    for n in ns:
                        for i in range(50):
                            cmp, swp = run_test(prog, gen_path, n, stat_code)
                            if cmp is None:
                                cmp = 0
                            if swp is None:
                                swp = 0
                            file.write(f"{n},{i+1},{cmp},{swp}\n")
                print(f"Results: {algo_name}, generator: {gen_name}, stat: {stat_label} -> {filename}")

if __name__ == "__main__":
    main()
