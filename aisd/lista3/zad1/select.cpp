#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <algorithm>
#include <sstream>
#include <cmath>
#include "functions.h"

int comparisons = 0;
int swaps = 0;
bool bigArray = false;

void countSwaps() {
  swaps++;
}
void countComparisons() {
  comparisons++;
}

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


int select(std::vector<int>& A, int p, int q, int k) {

 	// (q - p + 1) this is a size of a part where we want to use select
  	int howManyFives = floor((q - p + 1) / 5);
    int rest = (q - p + 1) % 5;

    std::vector<int> medians;
    std::vector<int> indexes;
    for(int i = p; i < howManyFives; i++) {
      	int left = i * 5;
      	int right = left + 4;
        insertionSort(A, left, right);
       	int median = A[i + 2];		// Median inside each five. Element in the middle
        medians.push_back(median);
        indexes.push_back(i+2);
        printArray(A);
    }
    if (rest != 0) {
    	insertionSort(A, (q - p + 1) - rest, (q - p + 1) - 1);		// call is for the last subarray
    	int lastMedian = A[q - floor(rest / 2)];
        medians.push_back(lastMedian);
        indexes.push_back(q - floor(rest / 2));
    	printArray(A);
    }

    int medianOfMedians = select(medians, 0, medians.size() - 1, floor(medians.size() / 2));
	int indexOfMedianOfMedians = 0;
    for (int i = 0; i < indexes.size(); i++) {
		if(A[indexes[i]] == medianOfMedians) {
        	indexOfMedianOfMedians = indexes[i];
		}
    }

    // teraz będziemy robić partitiona na tablicy A tej po is z pivotem na indeksie mediany median
}

int main () {

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