#include <time.h>
#include <stdlib.h>
#include <stdio.h>

//Found the mods with ghidra

int main() {
    srand(time(0));
    unsigned int number;
    int int_array[8];
    int_array[0] = 0x79;
    int_array[1] = 0x12c97f;
    int_array[2] = 0x135f0f8;
    int_array[3] = 0x74acbc6;
    int_array[4] = 0x56c614e;
    int_array[5] = 0xffffffe2;

    for ( int i = 0; i < 6; i++) {
        number = rand();
        int_array[i] -= (number % 10 + -1);
    }

    int local_int = 0;

    for (int j = 0; j < 6; j++) {
        local_int+=int_array[j];
    }

    printf("%d\n", local_int);
}