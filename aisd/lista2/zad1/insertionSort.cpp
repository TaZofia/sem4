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


bool compare(int a, int b) {
    comparisons++;
    return a > b;
}

void swap(std::vector<int>& A, int i) {
    swaps++;
    A[i + 1] = A[i];
}

bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i - 1] > arr[i]) {
            return false;
        }
    }
    return true;
}


void insertionSort(std::vector<int>& numbers) {
    std::vector<int> entranceArray = numbers;
    int n = numbers.size();

    if (n < 40) {
        std::cout << "Entrance array: ";
        printArray(entranceArray);
    }

    for (int j = 1; j < n; j ++) {
        int key = numbers[j];
        int i = j - 1;
        while (i >= 0) {

            if(compare(numbers[i], key)) {
                swap(numbers, i);
                i--;

                if(n < 40) {
                    std::cout << "In progress: ";
                    printArray(numbers);
                }   
                
            } else {
                break;
            }
        }
        numbers[i + 1] = key; 
    }
    if (n < 40) {
        std::cout << "-----Entrance array again: ";
        printArray(entranceArray);
        std::cout << "Array after insertionSort: ";
        printArray(numbers);
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


    insertionSort(numbers);
    
    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;
    
    if (isSorted(numbers)) {
        std::cout << "IS works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }
    return 0;
}