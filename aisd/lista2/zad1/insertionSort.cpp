#include <iostream>
#include <vector>
#include <sstream>


int insertionSort(int n, std::vector<int>& numbers) {
    for (int j = 1; j < n; j ++) {
        int key = numbers[j];

        i = j - 1;
        while (i > 0 && numbers[i] > key) {
            numbers[i + 1] = numbers[i];
            i -= 1;
        }
        numbers[i + 1] = key;
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

    
    insertionSort(n, numbers);

    // Wypisanie posortowanych liczb
    std::cout << n << ", ";
    for (size_t i = 0; i < numbers.size(); i++) {
        std::cout << numbers[i];
        if (i < numbers.size() - 1) std::cout << ", ";
    }
    std::cout << std::endl;



    return 0;
}