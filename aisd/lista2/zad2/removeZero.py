import os

def main():
    folder_path = r"K:\studia\sem4\aisd\lista2\zad2\results"
    file_path = os.path.join(folder_path, "Results_big_n_hs_k100.csv")

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    previous_swaps = None
    previous_cmp = None
    updated_lines = []

    for row in lines[1:]:
        element = row.strip().split(",")

        element[2] = int(element[2])
        element[3] = int(element[3])

        if element[2] == 0:
            element[2] = previous_cmp + 1

        if element[3] == 0:
            element[3] = previous_swaps + 1

        previous_cmp = element[2]
        previous_swaps = element[3]

        updated_lines.append(",".join(map(str, element)) + "\n")

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

if __name__ == "__main__":
    main()
