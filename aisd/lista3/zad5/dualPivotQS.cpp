#include <iostream>
#include <vector>
#include <sstream>
#include "functions.h"
#include "selectFunctions.h"



void dualPivotPartition(std::vector<int>& A, int low, int high, int& lp, int& rp) {
    int n = high - low + 1;

    int oneThirdIndex = low + n / 3;
    int twoThirdIndex = low + 2 * n / 3;

    int p = select(A, low, high, oneThirdIndex - low + 1); // 1-indexed
    int q = select(A, low, high, twoThirdIndex - low + 1);

    countComparisons();
    if (p > q) {
        std::swap(p, q);
        countSwaps();
    }

    int i = low;
    int k = low;
    int j = high;

    while (k <= j) {
        countComparisons();
        if (A[k] < p) {
            std::swap(A[i], A[k]);
            countSwaps();
            i++;
        } else {
            countComparisons();
            if (A[k] > q) {
                while (k < j && A[j] > q) {
                    countComparisons();
                    j--;
                }
                std::swap(A[k], A[j]);
                countSwaps();
                j--;

                countComparisons();
                if (A[k] < p) {
                    std::swap(A[i], A[k]);
                    countSwaps();
                    i++;
                }
            }
        }
        k++;
    }
    lp = i - 1;
    rp = j + 1;

    if (!bigArray) printArray(A);
}


void dualPivotQuickSort(std::vector<int>& A, int low, int high) {
    if (low < high) {
        int lp, rp;
        dualPivotPartition(A, low, high, lp, rp);
        dualPivotQuickSort(A, low, lp - 1);
        dualPivotQuickSort(A, lp + 1, rp - 1);
        dualPivotQuickSort(A, rp + 1, high);
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
