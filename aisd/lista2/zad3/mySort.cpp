#include <iostream>
#include <vector>
#include <sstream>
#include <cmath>
#include <climits>

int comparisons = 0;
int swaps = 0; // teraz to liczba przypisań (writeów), ale trzymamy nazwę "swaps" jako mySwap()

bool bigArray = false;

void printArray(const std::vector<int>& arr) {
    if (!bigArray) {
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

bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i - 1] > arr[i]) {
            return false;
        }
    }
    return true;
}

void mySwap(std::vector<int>& A, int index, int value) {
    swaps++;
    A[index] = value;
}

void merge(std::vector<int>& A, int p, int q, int r) {
    int n1 = q - p + 1;
    int n2 = r - q;

    std::vector<int> L(n1);
    std::vector<int> R(n2);

    for (int i = 0; i < n1; i++) {
        L[i] = A[p + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = A[q + 1 + j];
    }

    int i = 0, j = 0;
    int k = p;

    while (i < n1 && j < n2) {
        if (compare(L[i], R[j])) {
          	mySwap(A, k, L[i]);
            i++;
        }
        else {
          	mySwap(A, k, R[j]);
            j++;
        }
        k++;
    }
     while (i < n1) {
        mySwap(A, k, L[i]);
        i++;
        k++;
    }
    while (j < n2) {
  		mySwap(A, k, R[j]);
  		j++;
  		k++;
    }
    std::cout << "Array after merge from " << p << " to " << r << ": ";
    printArray(A);
}

void mySort(std::vector<int>& A) {
    int n = A.size();
    if (n <= 1) return;

    std::vector<std::pair<int, int>> blocks;

    int i = 0;
    while (i < n) {
        int start = i;
        while (i + 1 < n && compare(A[i], A[i + 1])) i++;		// we are looking for ascending pairs
        blocks.push_back({start, i});
        i++;
    }
	while (blocks.size() > 1) {
        std::vector<std::pair<int, int>> new_blocks;

        // merge pairs
        for (size_t j = 0; j + 1 < blocks.size(); j += 2) {
            int p = blocks[j].first;
            int q = blocks[j].second;
            int r = blocks[j + 1].second;
            merge(A, p, q, r);
            new_blocks.push_back({p, r});
        }

        // add last block
        if (blocks.size() % 2 != 0) {
            new_blocks.push_back(blocks.back());
        }

        blocks = new_blocks;
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

    int n = numbers[0]; // liczba elementów
    numbers.erase(numbers.begin());

    if (numbers.size() >= 40) {
        bigArray = true;
    }

    std::vector<int> entranceArray = numbers;

    if (!bigArray) {
        std::cout << "Entrance array: ";
        printArray(numbers);
    }

    mySort(numbers);

    if (!bigArray) {
        std::cout << "Entrance array again: ";
        printArray(entranceArray);

        std::cout << "Array after mySort: ";
        printArray(numbers);
    }

    std::cout << "# of comparisons: " << comparisons << std::endl;
    std::cout << "# of swaps: " << swaps << std::endl;

    if (isSorted(numbers)) {
        std::cout << "mySort works" << std::endl;
    } else {
        std::cout << "Error: Array not sorted" << std::endl;
    }

    return 0;
}
