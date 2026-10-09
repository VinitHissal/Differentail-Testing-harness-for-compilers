//
// Created by Vinit Hissal on 09/10/26.
//

/* tests/eval_order.c: unspecified behavior, may MISMATCH */
#include <stdio.h>
int f(void) { printf("f "); return 1; }
int g(void) { printf("g "); return 2; }
int main(void) { printf("%d\n", f() + g()); return 0; }