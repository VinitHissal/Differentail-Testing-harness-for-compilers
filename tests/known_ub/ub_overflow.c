//
// Created by Vinit Hissal on 09/10/26.
//

#include <stdio.h>
#include <limits.h>
int main(void) {
    volatile int v = INT_MAX;  /* hides the value from the constant folder */
    int x = v;
    if (x + 1 > x)
        printf("no wrap\n");
    else
        printf("wrapped\n");
    return 0;
}
