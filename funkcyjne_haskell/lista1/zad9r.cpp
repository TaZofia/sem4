#include <iostream>
#include <string>

// some function
int f (int n) {
    return n;
}


int recurency(int n) {
    if (n == 0) return f(0);  
    return f(n) + recurency(n - 1); 
}

int main() {
    
    int n;
    do {
    std::cout << "Podaj n: ";
    std::cin >> n;
    } while (n<0);

    std::cout << "Wynik: " << recurency(n) << std::endl;

    return 0;
}
