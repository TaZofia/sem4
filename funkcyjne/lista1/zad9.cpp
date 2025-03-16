#include <iostream>
#include <string>

// some function
int f (int n) {
    return n;
}
int loopApproach(int n) {
    int sum = 0;

    for (int k = 0; k <= n; k++) {
        sum += f(k);
    }
    return sum;
}
int main() {
    
    int n;
    do {
    std::cout << "Podaj n: ";
    std::cin >> n;
    } while (n<0);

    std::cout << "Wynik: " << loopApproach(n) << std::endl;

    return 0;
}
