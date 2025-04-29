import subprocess
import os
import time

def generate_input(generator, n, output_file):
    with open(output_file, "w") as f:
        subprocess.run([generator, str(n)], stdout=f)

def run_sort(sort_program, input_file):
    with open(input_file, "r") as f:
        input_data = f.read()

    result = subprocess.run(
        [sort_program],
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
    zad5_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad5"
    old_sorts_path = r"K:\\studia\\sem4\\aisd\\lista2\\zad1"
    results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad5\\results"
    temp_input_file = "temp_input.txt"

    generators = {
        "random": os.path.join(zad5_path, "randomGen.exe"),
        "ascending": os.path.join(zad5_path, "ascendingGen.exe"),
        "descending": os.path.join(zad5_path, "descendingGen.exe"),
    }
    algorithms = {
        "Quick Sort Select": (os.path.join(zad5_path, "quickSort.exe"), "qs_select"),
        "Dual Pivot Quick Sort Select": (os.path.join(zad5_path, "dualPivotQS.exe"), "dpqs_select"),
        "Quick Sort": (os.path.join(old_sorts_path, "quickSort.exe"), "qs"),
        "Dual Pivot Quick Sort": (os.path.join(old_sorts_path, "dualPivotQS.exe"), "dpqs"),
    }

    ns = list(range(100, 10001, 100))
    k = 10  # number of repetitions

    for gen_name, gen_path in generators.items():
        for algo_name, (algo_path, algo_short) in algorithms.items():
            result_file = os.path.join(results_path, f"Results_{algo_short}_{gen_name}.csv")
            with open(result_file, "w") as file:
                file.write("n,m,comparisons,swaps,execution_time\n")

                for n in ns:
                    generate_input(gen_path, n, temp_input_file)

                    for rep in range(1, k + 1):
                        start = time.perf_counter()
                        cmp, swp = run_sort(algo_path, temp_input_file)
                        end = time.perf_counter()
                        if cmp is None: cmp = 0
                        if swp is None: swp = 0

                        exe_time = end - start

                        file.write(f"{n},{rep},{cmp},{swp},{exe_time}\n")

            print(f"[DONE] {algo_name}, generator: {gen_name} → {result_file}")


if __name__ == "__main__":
    main()
