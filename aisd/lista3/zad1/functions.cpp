#include "functions.h"
#include <iostream>

void printArray(std::vector<int>& arr) {
        for (size_t i = 0; i < arr.size(); i++) {
            std::cout << (arr[i] < 10 ? "0" : "") << arr[i] << " ";
        }
        std::cout << std::endl;
}

bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i - 1] > arr[i]) {
            return false;
        }
    }
    return true;
}


