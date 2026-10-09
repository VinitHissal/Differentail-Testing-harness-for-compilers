//
// Created by Vinit Hissal on 09/10/26.
//

/* tests/unsigned_wrap.c: defined behavior, should MATCH */
#include <stdio.h>
#include <limits.h>
int main(void) {
    volatile unsigned v = UINT_MAX;
    unsigned x = v;
    if (x + 1 > x) printf("no wrap\n"); else printf("wrapped\n");
    return 0;
}