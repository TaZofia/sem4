#include <iostream>
#include <random>   // Mersenne Twister
#include <chrono>
#include <cmath>

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

int main(int argc, char* argv[]) {
    try {
        int n = getIntFromArgs(argc, argv);

        auto seed = std::chrono::steady_clock::now().time_since_epoch().count();
        std::mt19937 mt(seed);  
        std::uniform_int_distribution<int> distData(1, 2*n-1);      // Range from 1 to 2n-1

        int posStat = 1;    // default

        // Random positional statistic
        if(std::string(argv[2]) == "r") {

            std::uniform_int_distribution<int> distPos(1, n);
            posStat = distPos(mt);
        } else if (std::string(argv[2]) == "m") {
            posStat = floor(n / 2);
        } else {
            try {
                posStat = std::stoi(argv[2]);
            } catch (const std::invalid_argument&) {
                throw std::invalid_argument("Not int or r or m");
            }
        }

        std::cout << n << ", ";
        std::cout << posStat << ", ";

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