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

void dualPivotPartition(std::vector<int>& A, int low, int high, int& lp, int& rp) {
    if (compare(A[high], A[low]))
        swap(A, low, high);
    
    int p = A[low];
    int q = A[high];
    int i = low + 1;
    int k = low + 1;
    int j = high - 1;
    
    while (k <= j) {
        if (compare(A[k], p)) {
            swap(A, i, k);
            i++;
        } else if (!compare(A[k], q)) {
            while (k < j && !compare(A[j], q))
                j--;
            swap(A, k, j);
            j--;
            if (compare(A[k], p)) {
                swap(A, i, k);
                i++;
            }
        }
        k++;
    }
    i--, j++;
    swap(A, low, i);
    swap(A, high, j);
    lp = i;
    rp = j;
    
    if (!bigArray) printArray(A);
}

void dualPivotQuickSort(std::vector<int>& A, int low, int high) {
    if (low < high) {
        int lp, rp;
        dualPivotPartition(A, low, high, lp, rp);
        dualPivotQuickSort(A, low, lp - 1);
        dualPivotQuickSort(A, lp + 1, rp - 1);
        dualPivotQuickSort(A, rp + 1, high);
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

    int n = numbers[0]; // Number of elements
    numbers.erase(numbers.begin());

    if(numbers.size() >= 40) {
        bigArray = true;
    }

    std::vector<int> entranceArray = numbers;

    if(entranceArray.size() < 40) {
        std::cout << "Entrance array: ";
        printArray(numbers);
    }

    dualPivotQuickSort(numbers, 0, numbers.size()-1);

    if(entranceArray.size() < 40) {
        std::cout << "Entrance array again: ";
        printArray(entranceArray);

        std::cout << "Array after Dual-Pivot QuickSort: ";
        printArray(numbers);
    }
    
    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;
    
    if (isSorted(numbers)) {
        std::cout << "Dual-Pivot QS works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }
    return 0;
}
