import subprocess
import os

def generate_input(generator, n, statPos, output_file):
    with open(output_file, "w") as f:
        subprocess.run([generator, str(n), statPos], stdout=f)

def run_sort(sort_program, input_file, divider):
    with open(input_file, "r") as f:
        input_data = f.read()

    result = subprocess.run(
        [sort_program, str(divider)],
        input=input_data,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    cmp, swp = None, None
    for line in result.stdout.splitlines():
        if line.startswith("# of comparisons:"):
            cmp = int(line.removeprefix("# of comparisons:").strip())
        elif line.startswith("# of swaps:"):
            swp = int(line.removeprefix("# of swaps:").strip())
    return cmp, swp

def main():
    zad3_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad3"
    results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad3\\results"
    temp_input_file = "temp_input.txt"

    generators = {
        "random": os.path.join(zad3_path, "randomGen.exe"),
        "ascending": os.path.join(zad3_path, "ascendingGen.exe"),
        "descending": os.path.join(zad3_path, "descendingGen.exe"),
    }
    algorithms = {
        "Select": (os.path.join(zad3_path, "select.exe"), "se"),
    }
    statPos_options = {
        "m": "median",
        #"r": "randomStatPos",
        "1": "firstStatPos"
    }
    ks = [3, 5, 7, 9]

    ns = list(range(1000, 50001, 1000))
    m = 10

    for gen_name, gen_path in generators.items():
        for algo_name, (algo_path, algo_short) in algorithms.items():
            for stat_code, stat_label in statPos_options.items():
                for k in ks:
                    result_file = os.path.join(results_path, f"Results_{algo_short}_{k}_{gen_name}_{stat_label}.csv")
                    with open(result_file, "w") as file:
                        file.write("n,m,comparisons,swaps\n")

                        for n in ns:
                            generate_input(gen_path, n, stat_code, temp_input_file)

                            for rep in range(1, m + 1):
                                cmp, swp = run_sort(algo_path, temp_input_file, k)
                                if cmp is None: cmp = 0
                                if swp is None: swp = 0

                                file.write(f"{n},{rep},{cmp},{swp}\n")

                    print(f"[DONE] {algo_name}, generator: {gen_name}, statPos: {stat_label}, k={k} → {result_file}")


if __name__ == "__main__":
    main()
