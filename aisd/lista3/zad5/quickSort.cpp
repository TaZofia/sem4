#include <iostream>
#include <vector>
#include <cmath>
#include <sstream>
#include "functions.h"
#include "selectFunctions.h"

int partition(std::vector<int>& A, int p, int r) {

    int x = A[r];       // Pivot

    int i = p - 1;

    for(int j = p; j < r; j++) {
        countComparisons();
        if(A[j] <= x) {
            i++;
            std::swap(A[i], A[j]);
            countComparisons();
            if(i != j) {
                if(!bigArray) printArray(A);
            }
        }
    }
    std::swap(A[i+1], A[r]);
    countSwaps();

    if(i+1 != r) {
        if(!bigArray) printArray(A);
    }
    return (i+1);
}

void quickSort(std::vector<int>& A, int p, int r) {

    if(p < r) {
        std::vector<int> arrayToSelect = A;
        int median = select(arrayToSelect, p, r, std::floor((p + r) / 2));

        int index = 0;

        for(int i = 0; i < A.size(); i++) {
            countComparisons();
            if(A[i] == median) {
                index = i;
                break;
            }
        }
        std::swap(A[index], A[r]);
        countSwaps();

        int q = partition(A, p, r);
        quickSort(A, p, q-1);
        quickSort(A, q+1, r);
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

    int n = numbers[0];             // Number of elements
    numbers.erase(numbers.begin());

    if(numbers.size() >= 40) {
        bigArray = true;
    }

    std::vector<int> entranceArray = numbers;

    if(entranceArray.size() < 40) {
        std::cout << "Entrance array: ";
        printArray(numbers);
    }

    quickSort(numbers, 0, numbers.size()-1);

    if(entranceArray.size() < 40) {
        std::cout << "Entrance array again: ";
        printArray(entranceArray);

        std::cout << "Array after QuickSort: ";
        printArray(numbers);
    }
    

    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;
    
    if (isSorted(numbers)) {
        std::cout << "QS works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }
    return 0;
}