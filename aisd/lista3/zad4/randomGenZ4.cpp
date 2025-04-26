#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <cmath>
#include <cstring>

int getIntFromArgs(int argc, char* argv[]) {
    if (argc != 3) {
        throw std::invalid_argument("Expected 2 arguments");
    }

    try {
        return std::stoi(argv[1]);  
    } catch (const std::invalid_argument&) {
        throw std::invalid_argument("Argument 1 must be a valid integer.");
    }
}

bool existsInArray(const std::vector<int>& arr, int value) {
    for (int x : arr) {
        if (x == value) return true;
    }
    return false;
}

int main(int argc, char* argv[]) {
    try {
        int n = getIntFromArgs(argc, argv);

        auto seed = std::chrono::steady_clock::now().time_since_epoch().count();
        std::mt19937 mt(seed);  
        std::uniform_int_distribution<int> distData(1, 2*n-1);      // Range from 1 to 2n-1

        std::cout << n << ", ";            // array size

        std::vector<int> arr(n);

        for(int i = 0; i < n; i++) {        // add random numbers to array
            arr[i] = distData(mt);
        }

        int indexOfElementToFind = 0;
        int elementToFind = 0;

        if (strcmp(argv[2], "start") == 0) {
            int endIndex = std::ceil(n/5);
            std::uniform_int_distribution<int> startData(0, endIndex-1);
            indexOfElementToFind = startData(mt);
            elementToFind = arr[indexOfElementToFind];

        } else if (strcmp(argv[2], "end") == 0) {
            int startIndex = std::floor((4*n)/5);
            std::uniform_int_distribution<int> endData(startIndex, n-1);
            indexOfElementToFind = endData(mt);
            elementToFind = arr[indexOfElementToFind];

        } else if (strcmp(argv[2], "middle") == 0) {
            int startIndex = std::floor((2*n)/5);
            int endIndex = std::floor((3*n)/5);
            std::uniform_int_distribution<int> middleData(startIndex, endIndex);
            indexOfElementToFind = middleData(mt);
            elementToFind = arr[indexOfElementToFind];

        } else if (strcmp(argv[2], "randomIn") == 0) {
            std::uniform_int_distribution<int> inArray(0, n-1);
            indexOfElementToFind = inArray(mt);
            elementToFind = arr[indexOfElementToFind];
        } else if (strcmp(argv[2], "randomOut") == 0) {
            do {
                elementToFind = distData(mt);
            } while (existsInArray(arr, elementToFind));
        }

         std::cout << elementToFind << ", ";

         for (int i = 0; i < n - 1; i++) {
             std::cout << arr[i] << ", ";
         }
         std::cout << arr[n - 1] << std::endl;

    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}