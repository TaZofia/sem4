import subprocess
import os
import numpy as np

def run_test(sort_program, generator, n):

    cmd = f"{generator} {n} | {sort_program}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")

    cmp, swp = None, None
    for line in result.stdout.splitlines():
        if line.startswith("# of comparisons:"):
            cmp = int(line.removeprefix("# of comparisons:").strip())
        if line.startswith("# of swaps:"):
            swp = int(line.removeprefix("# of swaps:").strip())
    
    return cmp, swp

def main():
    zad1_path = r"K:\\studia\\sem4\\aisd\\lista2\\zad1"
    results_path = r"K:\studia\sem4\aisd\lista2\zad2\results"

    generators = {
        "random": os.path.join(zad1_path, "randomGen.exe"),
    }
    algorithms = {
        #"Insertion Sort": (os.path.join(zad1_path, "insertionSort.exe"), "is"),
        #"Quick Sort": (os.path.join(zad1_path, "quickSort.exe"), "qs"),
        "Hybrid Sort": (os.path.join(zad1_path, "hybrid.exe"), "hs"),
    }
    
    ns = list(range(10, 51, 10)) 
    ks = [1, 10, 100]
    

    for algo_name, (prog, algo_short) in algorithms.items():
        for k in ks:
            filename = os.path.join(results_path, f"Results_{algo_short}_k{k}.csv")
            with open(filename, "w") as file:
                file.write("n,k,comparisons,swaps\n")
                for n in ns:
                    for i in range(k):
                        cmp, swp = run_test(prog, generators["random"], n)
                        if cmp == None:
                            cmp = 0
                        if swp == None:
                            swp = 0                        
                        file.write(f"{n},{i+1},{cmp},{swp}\n")
            print(f"Results: {algo_name} and k={k} -> {filename}")

if __name__ == "__main__":
    main()
