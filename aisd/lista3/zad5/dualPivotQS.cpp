#include <iostream>
#include <vector>
#include <sstream>
#include "functions.h"
#include "selectFunctions.h"
void dualPivotQuickSort(std::vector<int>& A, int p, int r) {
    if (p < r) {
        int size = r - p + 1;
        int oneThirdIndex = p + size / 3;
        int twoThirdIndex = p + 2 * size / 3;

        int pval = select(A, p, r, oneThirdIndex - p + 1); // 1-based index
        int qval = select(A, p, r, twoThirdIndex - p + 1); // 1-based index

        if (pval > qval) std::swap(pval, qval);

        int indexP = -1, indexQ = -1;
        for (int i = p; i <= r; i++) {
            countComparisons();
            if (A[i] == pval && indexP == -1) {
                indexP = i;
            } else if (A[i] == qval && indexQ == -1) {
                indexQ = i;
            }
            if (indexP != -1 && indexQ != -1) break;
        }

        std::swap(A[p], A[indexP]);
        countSwaps();
        if (indexQ == p) indexQ = indexP; // handle swap conflict
        std::swap(A[r], A[indexQ]);
        countSwaps();

        int i = p + 1;
        int lt = p + 1;
        int gt = r - 1;
        int pivot1 = A[p];
        int pivot2 = A[r];

        while (i <= gt) {
            countComparisons();
            if (A[i] < pivot1) {
                std::swap(A[i], A[lt]);
                countSwaps();
                lt++;
            } else if (A[i] > pivot2) {
                while (A[gt] > pivot2 && i < gt) {
                    countComparisons();
                    gt--;
                }
                std::swap(A[i], A[gt]);
                countSwaps();
                gt--;
                if (A[i] < pivot1) {
                    std::swap(A[i], A[lt]);
                    countSwaps();
                    lt++;
                }
            }
            i++;
        }

        lt--;
        gt++;
        std::swap(A[p], A[lt]);
        countSwaps();
        std::swap(A[r], A[gt]);
        countSwaps();

        if (!bigArray) printArray(A);

        dualPivotQuickSort(A, p, lt - 1);
        dualPivotQuickSort(A, lt + 1, gt - 1);
        dualPivotQuickSort(A, gt + 1, r);
    }
}

int main() {
    std::string input;
    std::getline(std::cin, input);
    std::stringstream ss(input);
    std::vector<int> numbers;
    std::string token;
    
    while (std::getline(ss, token, ',')) { 
        numbers.push_back(std::stoi(token));
    }

    int n = numbers[0]; // Number of elements
    numbers.erase(numbers.begin());

    if(numbers.size() >= 40) {
        bigArray = true;
    }

    std::vector<int> entranceArray = numbers;

    if(entranceArray.size() < 40) {
        std::cout << "Entrance array: ";
        printArray(numbers);
    }

    dualPivotQuickSort(numbers, 0, numbers.size()-1);

    if(entranceArray.size() < 40) {
        std::cout << "Entrance array again: ";
        printArray(entranceArray);

        std::cout << "Array after Dual-Pivot QuickSort: ";
        printArray(numbers);
    }
    
    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;
    
    if (isSorted(numbers)) {
        std::cout << "Dual-Pivot QS works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }
    return 0;
}
