#include <stdio.h>
int main(void) {
    unsigned sum = 0;
    for (unsigned i = 1; i <= 100; i++)
        sum += i * i;
    printf("%u\n", sum);
    return 0;
}