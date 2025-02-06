#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
    srand(time(0));
    unsigned int number = rand();
    printf("%u\n", number);
}