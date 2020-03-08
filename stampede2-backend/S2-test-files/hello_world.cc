/*
BASICS

Automatic Dockerization
C++ example

Prints "Hello world"
*/


#include <fstream>


int main() {

    std::ofstream ff;
    ff.open("hw.txt");
    ff << "Hello world\n";
    ff.close();

    return 0;
}
