#include <iostream>
#include <vector>
#include <sstream>


int comparisons = 0;
int swaps = 0;

void printArray(const std::vector<int>& arr) {
    for (size_t i = 0; i < arr.size(); i++) {
        std::cout << (arr[i] < 10 ? "0" : "") << arr[i] << " ";
    }
    std::cout << std::endl;
}

void compare() {
    comparisons++;
}

void swap() {
    swaps++;
}


int insertionSort(int n, std::vector<int>& numbers) {

    std::vector<int> entranceArray = numbers;

    if (n < 40) {
        std::cout << "Entrance array: ";
        printArray(entranceArray);
    }

    for (int j = 1; j < n; j ++) {
        int key = numbers[j];

        int i = j - 1;
        while (i >= 0) {
            compare();
            if (numbers[i] > key) {
                numbers[i + 1] = numbers[i];
                swap();
                i--;
            } else {
                break;
            }
        }
        numbers[i + 1] = key; 
        if(n < 40) {
            std::cout << "Array after swap: ";
            printArray(numbers);
        }   
    }
    if (n < 40) {
        std::cout << "-----Entrance array again: ";
        printArray(entranceArray);
        std::cout << "Array after insertionSort: ";
        printArray(numbers);
    }
}
bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i - 1] > arr[i]) {
            return false;
        }
    }
    return true;
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


    insertionSort(n, numbers);
    
    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;
    
    if (isSorted(numbers)) {
        std::cout << "IS works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }
    return 0;
}