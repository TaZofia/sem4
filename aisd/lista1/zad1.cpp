#include <iostream>
#include <stack>
#include <queue>

void useQueue() {

    std::queue<int> queue;

    for(int i = 0; i < 50; i++){
        queue.push(i);
        std::cout << "Dodano do kolejki: " << i << std::endl;
    }

    for (int i = 0; i< 50; i++) {
        if(queue.size() == 0) {
            std::cout<< "Nie można pobrać elementu z kolejki, ponieważ jest pusta." << std::endl;
        } else {
            std::cout<< "Pobrano z kolejki: " << queue.front() << std::endl;
            queue.pop();
        }
    }
}

void useStack() {
    std::stack<int> stack;

for(int i = 0; i < 50; i++){
        stack.push(i);
        std::cout << "Dodano do stosu: " << i << std::endl;
    }

    for (int i = 0; i< 50; i++) {
        if(stack.size() == 0) {
            std::cout<< "Nie można pobrać elementu ze stosu, ponieważ jest pusty." << std::endl;
        } else {
            std::cout<< "Pobrano ze stosu: " << stack.top() << std::endl;
            stack.pop();
        }
    }
}

int main() {
    
    std::cout << "----------Kolejka----------" << std::endl;
    useQueue();
    std::cout << "----------Stos----------" << std::endl;
    useStack();
    
    return 0;
}
