#include <iostream>
#include <random>   // Mersenne Twister

int getIntFromArgs(int argc, char* argv[]) {
    if (argc != 2) {
        throw std::invalid_argument("Expected exactly one argument");
    }

    try {
        return std::stoi(argv[1]);  
    } catch (const std::invalid_argument&) {
        throw std::invalid_argument("Argument must be a valid integer.");
    }
}

int main(int argc, char* argv[]) {
    try {
        int n = getIntFromArgs(argc, argv);
        

        std::random_device rd;
        std::mt19937 mt(rd());
        std::uniform_int_distribution<int> dist(1, 2*n-1);      // Range from 1 to 2n-1

        std::cout << n << ", ";

        for(int i = 0; i < n - 1; i++) {
            std::cout << dist(mt) << ", ";
        }
        std::cout << dist(mt);
        

    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}