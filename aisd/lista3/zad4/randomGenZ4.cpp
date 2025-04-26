#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <cmath>

int getIntFromArgs(int argc, char* argv[]) {
    if (argc != 2) {
        throw std::invalid_argument("Expected 1 argument");
    }

    try {
        return std::stoi(argv[1]);  
    } catch (const std::invalid_argument&) {
        throw std::invalid_argument("Argument 1 must be a valid integer.");
    }
}

int main(int argc, char* argv[]) {
    try {
        int n = getIntFromArgs(argc, argv);

        auto seed = std::chrono::steady_clock::now().time_since_epoch().count();
        std::mt19937 mt(seed);  
        std::uniform_int_distribution<int> distData(1, 2*n-1);      // Range from 1 to 2n-1

        std::cout << n << ", ";

        std::cout << distData(mt) << ", ";        // random number which we are going to look for in binarySearch.cpp

        for(int i = 0; i < n - 1; i++) {
            std::cout << distData(mt) << ", ";
        }
        std::cout << distData(mt);
        

    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}