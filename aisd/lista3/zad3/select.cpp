#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <algorithm>
#include <sstream>
#include <cmath>
#include "functions.h"

int divider = 1;
int shift = 0;

void insertionSort(std::vector<int>& A, int p, int r) {
    for (int j = p + 1; j <= r; j++) {
        int key = A[j];
        int i = j - 1;
        while (i >= p && (A[i] > key)) {
            countComparisons();
            A[i + 1] = A[i];
            countSwaps();
            i--;
        }
        A[i + 1] = key;
    }
    if(!bigArray) {printArray(A);}
}

int modifiedPartition(std::vector<int>& A, int p, int q, int pivot) {

    int x = A[pivot];       // partition with given pivot

    std::swap(A[pivot], A[q]); // move to the end
    countSwaps();

    int i = p - 1;

    for(int j = p; j < q; j++) {
        countComparisons();
        if((A[j] <= x)) {
            i++;
            std::swap(A[i], A[j]);
            countSwaps();
            if(i != j) {
                if(!bigArray) {printArray(A);}
            }
        }
    }
    std::swap(A[i + 1], A[q]);
    countSwaps();

    if(i+1 != q) {
        if(!bigArray) {printArray(A);}
    }
    return (i+1);
}


int select(std::vector<int>& A, int p, int q, int i) {

    if (p == q) {
        return A[p];
    }

    int n = q - p + 1;
    int howMany = n / divider;
    int rest = n % divider;

    std::vector<int> medians;
    std::vector<int> medianIndices;

    for (int j = 0; j < howMany; j++) {
        int left = p + j * divider;
        int right = left + (divider - 1);
        insertionSort(A, left, right);
        int median = A[left + shift];
        medians.push_back(median);
    }

    if (rest != 0) {
        int left = p + howMany * divider;
        int right = q;
        insertionSort(A, left, right);
        int mid = left + (right - left) / 2;
        medians.push_back(A[mid]);
    }

    int medianOfMedians;
    if (medians.size() == 1) {
        medianOfMedians = medians[0];
    } else {
        medianOfMedians = select(medians, 0, medians.size() - 1, medians.size() / 2);
    }

    // Find the index of the medianOfMedians in the original array
    int pivotIndex = p;
    for (int j = p; j <= q; j++) {
        if (A[j] == medianOfMedians) {
            pivotIndex = j;
            break;
        }
    }

    int partitionIndex = modifiedPartition(A, p, q, pivotIndex);
    int k = partitionIndex - p + 1;

    if (i == k) {
        return A[partitionIndex];
    } else if (i < k) {
        return select(A, p, partitionIndex - 1, i);
    } else {
        return select(A, partitionIndex + 1, q, i - k);
    }
}

int getIntFromArgs(int argc, char* argv[]) {
    if (argc != 2) {
        throw std::invalid_argument("Expected 1 argument");
    }

    try {
        return std::stoi(argv[1]);  
    } catch (const std::invalid_argument&) {
        throw std::invalid_argument("Argument 1 must be a valid integer.");
    }
}

int main (int argc, char* argv[]) {


    divider = getIntFromArgs(argc, argv);
    shift = std::floor(divider / 2);

    std::string input;
    std::getline(std::cin, input);
    std::stringstream ss(input);
    std::vector<int> numbers;
    std::string token;

    while (std::getline(ss, token, ',')) {
        numbers.push_back(std::stoi(token));
    }

    int n = numbers[0];             // Number of elements
    int posStat = numbers[1];

    numbers.erase(numbers.begin(), numbers.begin() + 2);

    std::vector<int> entranceArray = numbers;

    if(numbers.size() > 30) {
        bigArray = true;
    }
    if(!bigArray) {
      std::cout << "Entrance array: ";
      printArray(entranceArray);
    }

    int psValue = select(numbers, 0, numbers.size() - 1, posStat);

    if (!bigArray) {
        std::cout << "---------Entrance array again: ";
        printArray(entranceArray);
        std::cout << "Array after Randomized Select: ";
        printArray(numbers);
        std::cout << "-----------------Sorted array: ";
        std::sort(entranceArray.begin(), entranceArray.end());
        printArray(entranceArray);
    }

    std::cout << posStat << " positional statistics: " << psValue << std::endl;

    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;

    return 0;
}