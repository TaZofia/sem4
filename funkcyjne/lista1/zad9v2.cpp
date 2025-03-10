#include <iostream>
#include <cmath> 


double f (double x) {
    /*
    double y = sin(x);
    return y * y + y + x;
    */

    return sin(x) * sin(x) + sin(x) + x;
}


int main() {

    double x;
    std::cout << "Podaj x: ";
    std::cin >> x;
    std::cout << "f(x) = " << f(x) << std::endl;

    return 0;
}