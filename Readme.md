# compiler-difftest

A small differential-testing tool for C compilers. It generates random
UB-free C programs, compiles each with GCC 16 and Apple clang at -O0/-O2/-O3,
runs all six binaries, and flags any output difference.

## How undefined behavior is avoided
- Unsigned arithmetic only (no promotion to signed int)
- Shift counts masked with `& 31u`; divisors forced nonzero with `| 1u`
- All variables initialized; no function calls or side effects in expressions
- Second layer: each program is run once under UBSan and skipped if it reports UB

## Harness design
- `multiprocessing` pool (4 workers); compile and run timeouts
- Mismatches are retried once; results are classified as
  MATCH / MISMATCH / FLAKY / INFRA_ERROR / UB

## Results
200 programs x 6 configurations: 200 MATCH, 0 mismatches (13m 20s).

## Demo
`python3 difftest.py --no-ub-filter tests/known_ub/ub_overflow.c`
shows clang -O0 printing "wrapped" and -O2 printing "no wrap" for signed
overflow. UBSan flags it, and `-fwrapv` makes all six configs agree.

## Limitations
Unsigned-only, no pointers/structs/functions; UBSan is dynamic and misses
some UB; tested on one machine and one compiler pair; found no compiler bugs.