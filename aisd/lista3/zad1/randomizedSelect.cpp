#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <algorithm>
#include <sstream>
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
int randomPartition(std::vector<int>& A, int p, int q) {

    auto seed = std::chrono::steady_clock::now().time_since_epoch().count();
    std::mt19937 mt(seed);
    std::uniform_int_distribution<int> random(p, q);      // range from p to q

    int index = random(mt);

    std::swap(A[index], A[q]);
    countSwaps();
    if(!bigArray) {printArray(A);}

    int x = A[q];       // ranodm pivot
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

int randomizedSelect(std::vector<int>& A, int p, int q, int i) {

    if (p == q) return A[p];

    int r = randomPartition(A, p, q);
    int k = r - p + 1;
    if (i == k) return A[r];
    else if (i < k) return randomizedSelect(A, p, r - 1, i);
    else return randomizedSelect(A, r + 1, q, i - k);
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

    int psValue = randomizedSelect(numbers, 0, n-1, posStat);

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