import subprocess
import os

def generate_input(generator, n, output_file):
    with open(output_file, "w") as f:
        subprocess.run([generator, str(n)], stdout=f)

def run_sort(sort_program, input_file, statPos):
    with open(input_file, "r") as f:
        result = subprocess.run([sort_program, statPos], stdin=f, capture_output=True, text=True, encoding="utf-8")
    
    cmp, swp = None, None
    for line in result.stdout.splitlines():
        if line.startswith("# of comparisons:"):
            cmp = int(line.removeprefix("# of comparisons:").strip())
        elif line.startswith("# of swaps:"):
            swp = int(line.removeprefix("# of swaps:").strip())
    return cmp, swp

def main():
    zad1_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad1"
    results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad2\\results2"
    temp_input_file = "temp_input.txt"

    generators = {
        "random": os.path.join(zad1_path, "randomGen.exe"),
        "ascending": os.path.join(zad1_path, "ascendingGen.exe"),
        "descending": os.path.join(zad1_path, "descendingGen.exe"),
    }
    algorithms = {
        "Select": (os.path.join(zad1_path, "select.exe"), "se"),
        "Randomized Select": (os.path.join(zad1_path, "randomizedSelect.exe"), "rs"),
    }
    statPos_options = {
        "m": "median",
        "r": "randomStatPos",
        "1": "firstStatPos"
    }

    ns = list(range(100, 50001, 100))
    m = 10

    for gen_name, gen_path in generators.items():
        for algo_name, (algo_path, algo_short) in algorithms.items():
            for stat_code, stat_label in statPos_options.items():
                result_file = os.path.join(results_path, f"Results_{algo_short}_{gen_name}_{stat_label}.csv")
                with open(result_file, "w") as file:
                    file.write("n,m,comparisons,swaps\n")
                    for n in ns:
                        for rep in range(1, m + 1):
                            # 1. Generate input once
                            generate_input(gen_path, n, temp_input_file)

                            # 2. Run the algorithm on the same input
                            cmp, swp = run_sort(algo_path, temp_input_file, stat_code)
                            if cmp is None: cmp = 0
                            if swp is None: swp = 0

                            # 3. Save results
                            file.write(f"{n},{rep},{cmp},{swp}\n")

                print(f"[DONE] {algo_name}, generator: {gen_name}, statPos: {stat_label} → {result_file}")

if __name__ == "__main__":
    main()
