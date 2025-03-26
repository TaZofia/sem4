#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>

struct Node {
    int value;
    Node* next;
};

struct CircularList {
    Node* head;    
    int size;    

    CircularList() : head(nullptr), size(0) {}
};

void insert (CircularList& list, int value) {
    Node* newNode = new Node{value, nullptr};

    // Gdy w liście nie ma żadnego elementu
    if(list.size == 0) {
        newNode->next = newNode;
        list.head = newNode;
    } else {
        Node* temp = list.head;

        while(temp->next != list.head) {
            temp = temp->next;
        }

        temp->next = newNode;
        newNode->next = list.head;     
    }
    list.size++;
}

void merge(CircularList& list1, CircularList& list2) {

    if(list1.size == 0) {
        list1.head = list2.head;
        list1.size = list2.size;

    } else if (list2.size > 0) {
        Node* temp1 = list1.head;

        while(temp1->next != list1.head) {
            temp1 = temp1->next;
        }

        Node* temp2 = list2.head;
        
        while (temp2->next != list2.head) {
            temp2 = temp2->next;
        }

        temp1->next = list2.head;       // "ostatni" element listy 1 wskazuje na "początek" listy 2
        temp2->next = list1.head;       // "ostatni" element listy 2 wskazuje na "początek" listy 1

        list2.head = nullptr;

        list1.size += list2.size;
        list2.size = 0;
    }
}

int searchAndCountComparisons(CircularList& list, int searchedValue) {

    if(list.size == 0) return -1;

    Node* temp = list.head;
    int comparisons = 0;


    do{
        comparisons++;
        if (temp->value == searchedValue){
            return comparisons;
        }
        temp = temp->next;
    }while(temp != list.head);
    return comparisons;
}


int main() {

    std::srand(std::time(nullptr)); 
    CircularList l1, l2;

    for (int i = 10; i < 20; i++) {
        insert(l1, i);
        insert(l2, i+10);
    }

    std::cout<< "Lista 1 po wstawieniu 10 elementów"<< std::endl;
    Node* templ1 = l1.head;
    for(int i =0; i < l1.size; i++) {
        std::cout << templ1->value << ", ";
        templ1 = templ1->next;
    }
    std::cout << std::endl;


    std::cout<< "Lista 2 po wstawieniu 10 elementów"<< std::endl;
    Node* templ2 = l2.head;
    for(int i =0; i < l2.size; i++) {
        std::cout << templ2->value << ", ";
        templ2 = templ2->next;
    }
    std::cout << std::endl;

    merge(l1, l2);

    std::cout << "Lista po połączeniu l1 i l2" << std::endl;
    templ1 = l1.head;
    for(int i =0; i < l1.size; i++) {
        std::cout << templ1->value << ", ";
        templ1 = templ1->next;
    }
    std::cout << std::endl;


    int T[10000];
    CircularList randomList;

    for(int i = 0; i < 10000; i++) {
        int randomValue = std::rand() % 100000;
        T[i] = randomValue;
        insert(randomList, randomValue);
    }


    std::cout << "Wyszukiwanie liczb, które są na liście" << std::endl;
    int sum = 0;
    for (int i = 0 ; i < 1000; i++) {
        int randVal = std::rand() % 10000;
        int comparisonsWhileSearch = searchAndCountComparisons(randomList, T[randVal]); 
        sum += comparisonsWhileSearch;
    }

    double avg = (double)sum / 1000;

    std::ofstream file("zad2r1.txt", std::ios::app);
    if (file.is_open()) {
        file << avg << std::endl;  
        file.close();  
    } else {
        std::cerr << "Nie mozna otworzyc pliku" << std::endl;
    }

    std::cout << "Średni koszt tysiąca wyszukiwań losowych liczb, które są na liście: " << avg << std::endl;


    std::cout << "Wyszukiwanie losowej liczby z I" << std::endl;
    int sum2 = 0;
    for (int i = 0 ; i < 1000; i++) {
        int randomValue = std::rand() % 100000;
        int comparisons = searchAndCountComparisons(randomList, randomValue);
        sum2 += comparisons;
    }

    double avg2 = (double)sum2 / 1000;

    std::ofstream file2("zad2r2.txt", std::ios::app);
    if (file2.is_open()) {
        file2 << avg2 << std::endl; 
        file2.close();  
    } else {
        std::cerr << "Nie mozna otworzyc pliku" << std::endl;
    }

    std::cout << "Średni koszt tysiąca wyszukiwań losowych liczb, które nie muszą być na liście: " << avg2 << std::endl;

    return 0;
}