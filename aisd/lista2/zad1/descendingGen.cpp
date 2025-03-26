#include <iostream>

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

        for(int i = 0; i < n; i++) {
            std::cout << n - i << ", ";
        }
        std::cout << 0;
        

    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}