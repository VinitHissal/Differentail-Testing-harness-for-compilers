# Differentail-Testing-harness-for-compilers
tool that generates random c programs, compiles them with GCC and Clang at different optimzation levels, and checks the output match. I filter out programs with undefined behavious, because a mismatch there isn't a compiler bug. It shows how compiler verification works at small scale.
