#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <algorithm>
#include <sstream>
#include <vector>
#include <cmath>
#include "functions.h"

int comparisons = 0;

void countComparisons() {
    comparisons++;
}

int binarySearch(std::vector<int> &A, int p, int q, int key) {
    if(q >= p) {
         int mid = floor((q + p) / 2);
         countComparisons();
         if(A[mid] == key) {
             return 1;
         } else if(A[mid] > key) {
             return binarySearch(A, p, mid - 1, key);
         } else {
             return binarySearch(A, mid + 1, q, key);
         }
    }
    return 0;
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

    int n = numbers[0];    // Number of elements
    int elementToFind = numbers[1];

    numbers.erase(numbers.begin(), numbers.begin() + 2); // delete number of elements and element to find

    std::sort(numbers.begin(), numbers.end());

    if(n <= 30) {
        std::cout << "Entrance array: ";
        printArray(numbers);
        std::cout << "Value we're looking for: " << elementToFind << std::endl;
    }

    int result = binarySearch(numbers, 0, n - 1, elementToFind);

    if(result == 1) {
        std::cout << "Element found." << std::endl;
    } else {
        std::cout << "Element not found." << std::endl;
    }
    std::cout << "# of comparisons: " << comparisons << std::endl;
    return 0;
}