#include <iostream>

struct Node {
    int value;
    Node* previous;
    Node* next;
};

struct List {
    Node* head;    
    int size;    

    List() : head(nullptr), size(0) {}
};



int main() {

    return 0;
}