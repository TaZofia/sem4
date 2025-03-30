#include <iostream>
#include <vector>
#include <sstream>

int comparisons = 0;
int swaps = 0;
const int MAXFORIS = 10;  // Maksymalny rozmiar podtablicy dla InsertionSort

void printArray(const std::vector<int>& arr) {
    for (size_t i = 0; i < arr.size(); i++) {
        std::cout << (arr[i] < 10 ? "0" : "") << arr[i] << " ";
    }
    std::cout << std::endl;
}

bool compareIS(int a, int b) {
    comparisons++;
    return a > b;
}

void swapIS(std::vector<int>& A, int i) {
    swaps++;
    A[i + 1] = A[i];
}
bool compareQS(int a, int b) {
    comparisons++;
    return a <= b;
}

void swapQS(std::vector<int>& A, int i, int j) {
    swaps++;
    int temp = A[j];
    A[j] = A[i];
    A[i] = temp;
}


bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i - 1] > arr[i]) {
            return false;
        }
    }
    return true;
}

void insertionSort(std::vector<int>& A) { 
    for (int j = 1; j < A.size(); j ++) {
        int key = A[j];
        int i = j - 1;
        while (i >= 0) {

            if(compareIS(A[i], key)) {
                swapIS(A, i);
                i--;

                if(A.size() < 40) {
                    std::cout << "In progressIS: ";
                    printArray(A);
                }   

            } else {
                break;
            }
        }
        A[i + 1] = key; 
    }
}

int partition(std::vector<int>& A, int p, int r) {
    int x = A[r];       // Pivot
    int i = p - 1;

    for(int j = p; j < r; j++) {
        if(compareQS(A[j], x)) {
            i++;
            swapQS(A, i, j);
            if(i != j) {
                if(A.size() < 40) {
                    std::cout << "In progress: ";
                    printArray(A);
                }   
            }
        }
    }
    swapQS(A, i + 1, r);

    if(i+1 != r) {
        if(A.size() < 40) {
            std::cout << "In progress: ";
            printArray(A);
        }   
    }
    return (i+1);
}

void hybridQuickSort(std::vector<int>& A, int p, int r) {
    if (p < r) {
        // small array -> insertion sort
        if (r - p + 1 <= MAXFORIS) {
            insertionSort(A);
            return;
        }
        
        int q = partition(A, p, r);
        hybridQuickSort(A, p, q - 1);
        hybridQuickSort(A, q + 1, r);
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

    int n = numbers[0];  // Liczba elementów
    numbers.erase(numbers.begin());

    std::vector<int> entranceArray = numbers;

    if (numbers.size() < 40) {
        std::cout << "Entrance array: ";
        printArray(numbers);
    }

    hybridQuickSort(numbers, 0, numbers.size() - 1);

    if (numbers.size() < 40) {
        std::cout << "--------Entrance array again: ";
        printArray(entranceArray);
        std::cout << "Array after Hybrid QuickSort: ";
        printArray(numbers);
    }

    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;

    if (isSorted(numbers)) {
        std::cout << "Hybrid QS works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }

    return 0;
}
