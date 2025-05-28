import subprocess
import re
import csv

# wartości n, 20 testów dla każdej
ns = list(range(10000, 100001, 10000))
tests_per_n = 20

# nazwy plików wyjściowych
files = {
    "ascending_insert": "ascending_insert.csv",
    "random_delete_after_ascending_insert": "random_delete_after_ascending_insert.csv",
    "random_insert": "random_insert.csv",
    "random_delete_after_random_insert": "random_delete_after_random_insert.csv",
    "summary": "summary.csv"
}

# funkcje pomocnicze do parsowania wyjścia programu
def parse_output(output):

    data = {}

    # wzorce dla każdej sekcji (średnie i maksymalne)
    patterns = {
        "ascending_insert": {
            "avg_comparisons": r"Ascending insert average cost comparisons: (\d+)",
            "avg_pointer": r"Ascending insert average cost pointer: (\d+)",
            "avg_height": r"Ascending insert average height: (\d+)",
            "max_comparisons": r"Ascending insert max comparisons: (\d+)",
            "max_pointer": r"Ascending insert max pointer: (\d+)",
            "max_height": r"Ascending insert max height: (\d+)"
        },
        "random_delete_after_ascending_insert": {
            "avg_comparisons": r"Random delete after ascending insert average cost comparisons: (\d+)",
            "avg_pointer": r"Random delete after ascending insert average cost pointer: (\d+)",
            "avg_height": r"Random delete after ascending insert average height: (\d+)",
            "max_comparisons": r"Random delete after ascending insert max comparisons: (\d+)",
            "max_pointer": r"Random delete after ascending insert max pointer: (\d+)",
            "max_height": r"Random delete after ascending insert max height: (\d+)"
        },
        "random_insert": {
            "avg_comparisons": r"Random insert average cost comparisons: (\d+)",
            "avg_pointer": r"Random insert average cost pointer: (\d+)",
            "avg_height": r"Random insert average height: (\d+)",
            "max_comparisons": r"Random insert max comparisons: (\d+)",
            "max_pointer": r"Random insert max pointer: (\d+)",
            "max_height": r"Random insert max height: (\d+)"
        },
        "random_delete_after_random_insert": {
            "avg_comparisons": r"Random delete after random insert average cost comparisons: (\d+)",
            "avg_pointer": r"Random delete after random insert average cost pointer: (\d+)",
            "avg_height": r"Random delete after random insert average height: (\d+)",
            "max_comparisons": r"Random delete after random insert max comparisons: (\d+)",
            "max_pointer": r"Random delete after random insert max pointer: (\d+)",
            "max_height": r"Random delete after random insert max height: (\d+)"
        }
    }

    for scenario, pats in patterns.items():
        data[scenario] = {}
        for key, pat in pats.items():
            m = re.search(pat, output)
            if m:
                data[scenario][key] = int(m.group(1))
            else:
                data[scenario][key] = None

    return data


def run_and_collect(n, test_id):
    print(f"Running test {test_id} for n={n}...")
    proc = subprocess.run([r"..\zad5\sp", str(n)], capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error running for n={n}: {proc.stderr}")
        return None
    return parse_output(proc.stdout)


def write_csv(filename, fieldnames, rows):
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ascending_insert_rows = []
    random_delete_after_asc_rows = []
    random_insert_rows = []
    random_delete_after_rand_rows = []

    summary_rows = []

    for n in ns:
        temp_results = {
            "ascending_insert": [],
            "random_delete_after_ascending_insert": [],
            "random_insert": [],
            "random_delete_after_random_insert": []
        }

        for test_id in range(1, tests_per_n + 1):
            data = run_and_collect(n, test_id)
            if data is None:
                continue

            for scenario in temp_results.keys():
                vals = data[scenario]
                row = {
                    "n": n,
                    "test_id": test_id,
                    "comparisons": vals["avg_comparisons"],
                    "pointer_ops": vals["avg_pointer"],
                    "height": vals["avg_height"],
                    "max_comparisons": vals["max_comparisons"],
                    "max_pointer_ops": vals["max_pointer"],
                    "max_height": vals["max_height"]
                }
                if scenario == "ascending_insert":
                    ascending_insert_rows.append(row)
                elif scenario == "random_delete_after_ascending_insert":
                    random_delete_after_asc_rows.append(row)
                elif scenario == "random_insert":
                    random_insert_rows.append(row)
                elif scenario == "random_delete_after_random_insert":
                    random_delete_after_rand_rows.append(row)

                temp_results[scenario].append(vals)

        for scenario, results_list in temp_results.items():
            if not results_list:
                continue
            comp_list = [r["avg_comparisons"] for r in results_list if r["avg_comparisons"] is not None]
            ptr_list = [r["avg_pointer"] for r in results_list if r["avg_pointer"] is not None]
            h_list = [r["avg_height"] for r in results_list if r["avg_height"] is not None]
            comp_max_list = [r["max_comparisons"] for r in results_list if r["max_comparisons"] is not None]
            ptr_max_list = [r["max_pointer"] for r in results_list if r["max_pointer"] is not None]
            h_max_list = [r["max_height"] for r in results_list if r["max_height"] is not None]

            avg_comp = int(sum(comp_list) / len(comp_list)) if comp_list else None
            avg_ptr = int(sum(ptr_list) / len(ptr_list)) if ptr_list else None
            avg_h = int(sum(h_list) / len(h_list)) if h_list else None

            max_comp = max(comp_max_list) if comp_max_list else None
            max_ptr = max(ptr_max_list) if ptr_max_list else None
            max_h = max(h_max_list) if h_max_list else None

            summary_rows.append({
                "n": n,
                "scenario": scenario,
                "avg_comparisons": avg_comp,
                "avg_pointer_ops": avg_ptr,
                "avg_height": avg_h,
                "max_comparisons": max_comp,
                "max_pointer_ops": max_ptr,
                "max_height": max_h
            })

    write_csv(files["ascending_insert"], ["n","test_id","comparisons","pointer_ops","height","max_comparisons","max_pointer_ops","max_height"], ascending_insert_rows)
    write_csv(files["random_delete_after_ascending_insert"], ["n","test_id","comparisons","pointer_ops","height","max_comparisons","max_pointer_ops","max_height"], random_delete_after_asc_rows)
    write_csv(files["random_insert"], ["n","test_id","comparisons","pointer_ops","height","max_comparisons","max_pointer_ops","max_height"], random_insert_rows)
    write_csv(files["random_delete_after_random_insert"], ["n","test_id","comparisons","pointer_ops","height","max_comparisons","max_pointer_ops","max_height"], random_delete_after_rand_rows)
    write_csv(files["summary"], ["n","scenario","avg_comparisons","avg_pointer_ops","avg_height","max_comparisons","max_pointer_ops","max_height"], summary_rows)

    print("Finished! CSV files generated.")

if __name__ == "__main__":
    main()
