import subprocess
import os
import numpy as np
import time

def run_test(sort_program, generator, n, where):

    cmd = f"{generator} {n} {where} | {sort_program}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")

    cmp = None
    for line in result.stdout.splitlines():
        if line.startswith("# of comparisons:"):
            cmp = int(line.removeprefix("# of comparisons:").strip())
    
    return cmp

def main():
    zad4_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad4"
    results_path = r"K:\\studia\\sem4\\aisd\\lista3\\zad4\\results"

    generators = {
        "random": os.path.join(zad4_path, "rand.exe"),
    }
    algorithms = {
        "Binary Search": (os.path.join(zad4_path, "binarySearch.exe"), "bs"),
    }
    wherelabels = {
        "start",
        "middle",
        "end",
        "randomIn",
        "randomOut"
    }
    
    ns = list(range(1000, 100001, 1000)) 
    ks = [10]
    

    for algo_name, (prog, algo_short) in algorithms.items():
        for k in ks:
            for where in wherelabels:

                filename = os.path.join(results_path, f"Results_{algo_short}_{where}.csv")
                with open(filename, "w") as file:
                    file.write("n,k,comparisons, execution_time\n")
                    for n in ns:
                        for i in range(k):
                            start = time.perf_counter()
                            cmp = run_test(prog, generators["random"], n, where)
                            end = time.perf_counter()
                            if cmp == None:
                                cmp = 0  

                            exe_time = end - start
                            file.write(f"{n},{i+1},{cmp},{exe_time}\n")
                print(f"Results: {algo_name} and where: {where} -> {filename}")

if __name__ == "__main__":
    main()
