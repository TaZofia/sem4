#include <iostream>
#include <vector>
#include <sstream>


int comparisons = 0;
int swaps = 0;

bool bigArray = false;

void printArray(const std::vector<int>& arr) {
    if(!bigArray) {
        for (size_t i = 0; i < arr.size(); i++) {
            std::cout << (arr[i] < 10 ? "0" : "") << arr[i] << " ";
        }
        std::cout << std::endl;
    }
}

bool compare(int a, int b) {
    comparisons++;
    return a <= b;
}

void swap(std::vector<int>& A, int i, int j) {
    swaps++;
    int temp = A[j];
    A[j] = A[i];
    A[i] = temp;
}

int partition(std::vector<int>& A, int p, int r) {
    int x = A[r];       // Pivot
    int i = p - 1;

    for(int j = p; j < r; j++) {
        if(compare(A[j], x)) {
            i++;
            swap(A, i, j);
            if(i != j) {
                printArray(A);
            }
        }
    }
    swap(A, i + 1, r);

    if(i+1 != r) {
        printArray(A);
    }
    return (i+1);
}

void quickSort(std::vector<int>& A, int p, int r) {

    if(p < r) {
        int q = partition(A, p, r);
        quickSort(A, p, q-1);
        quickSort(A, q+1, r);
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