#include <iostream>
#include <stdexcept>

void pushQueue(int array[], int n, int& queueCounter) {
    if(queueCounter == 99) {
        throw std::runtime_error("No place in a queue");
    } else {
        array[queueCounter] = n;
        queueCounter++;
    } 
}
int popQueue(int array[], int& queueCounter) {
    if(queueCounter > 0) {
        int elementToReturn = array[0];

        for(int i = 0; i < queueCounter; i++) {
            array[i] = array[i+1];
        }
        queueCounter--;
        return elementToReturn;

    } else {
        throw std::runtime_error("There is nothing in the queue");
    }
}

void pushStack(int array[], int n, int& stackCounter) {

    if(stackCounter == 99) {
        throw std::runtime_error("No place on a stack");
    } else {
        array[stackCounter] = n;
        stackCounter++;
    }
}

int popStack(int array[], int& stackCounter) {

    if(stackCounter > 0) {
        int elementToReturn = array[stackCounter-1];
        stackCounter--;
        return elementToReturn;

    } else {
        throw std::runtime_error("There is nothing on the stack");
    }
}

 
int main() {


    int queueArray[100];
    int stackArray[100];

    int queueCounter = 0;       // Ostatni wolny element tablicy
    int stackCounter = 0;
    
    std::cout << "----------Queue----------" << std::endl;
    for(int i = 0; i < 50; i++){
        try {
        pushQueue(queueArray, i, queueCounter);
        std::cout << "Added to queue: " << i << std::endl;
        } catch (const std::runtime_error& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }

    for (int i = 0; i < 50; i++) {
        try {
        int elem = popQueue(queueArray, queueCounter);
        std::cout << "From queue: " << elem << std::endl;
        } catch (const std::runtime_error& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }

    std::cout << "----------Stack----------" << std::endl;
    for (int i = 0; i < 50; i++) {
        try {
        pushStack(stackArray, i, stackCounter);
        std::cout << "Added to stack: " << i << std::endl;
        } catch (const std::runtime_error& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }
    for(int i = 0; i < 50; i++) {
        try {
            int elem = popStack(stackArray, stackCounter);
            std::cout << "From stack: " << elem << std::endl;
        } catch (const std::runtime_error& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }

    return 0;
}
