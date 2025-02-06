#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
    srand(time(0));
    for (int i = 0; (int)i < 0x32; i = i + 1) {
        int rand_num = rand() % 100;
        printf("%d\n",rand_num);
    }
}