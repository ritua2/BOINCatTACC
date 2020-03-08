/*
BASICS

Automatic Dockerization
C example

Prints "Hello world"
*/


#include <stdio.h>


int main() {

    FILE *ff = fopen("hw.txt", "w");

    fprintf(ff, "Hello world\n");
    fclose(ff);
    return 0;
}
