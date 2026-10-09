#!/usr/bin/env python3

import itertools, os, subprocess, sys, tempfile, re

COMPILERS = ["gcc-16", "clang"]     # adjust to your installed GCC
OPT_LEVELS = ["-O0", "-O2", "-O3"]

def has_ub(src, compiler="clang"):
    """Return True if the program triggers undefined behavior under UBSan."""
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "ubsan_bin")
        r = subprocess.run(
            [compiler, "-O0", "-w", "-fsanitize=undefined",
             "-fno-sanitize-recover=undefined", src, "-o", out],
            capture_output=True, text=True)
        if r.returncode != 0:
            return False  # can't tell; let normal testing report the compile error
        try:
            run = subprocess.run([out], capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            return False
        return "runtime error" in run.stderr
def compile_c(compiler, opt, src, out):
    try:
        r = subprocess.run([compiler, opt, "-w", src, "-o", out],
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "COMPILE_TIMEOUT"
    return r.returncode == 0, r.stderr



def run_bin(path, timeout=20):
    try:
        r = subprocess.run([path], capture_output=True, text=True, timeout=timeout)
        return (r.returncode, r.stdout)
    except subprocess.TimeoutExpired:
        return ("TIMEOUT", "")

def test_file(src):
    """Return {(compiler, opt): result} for one C file."""
    results = {}
    with tempfile.TemporaryDirectory() as d:
        for comp, opt in itertools.product(COMPILERS, OPT_LEVELS):
            out = os.path.join(d, f"{comp}{opt}")
            ok, err = compile_c(comp, opt, src, out)
            if not ok:
                results[(comp, opt)] = ("COMPILE_ERROR", err[:200])
            else:
                results[(comp, opt)] = run_bin(out)
    return results

def report(src, results):
    distinct = set(results.values())
    status = "MATCH" if len(distinct) == 1 else "MISMATCH"
    print(f"[{status}] {src}")
    if status == "MISMATCH":
        for (comp, opt), res in sorted(results.items()):
            print(f"    {comp:8s} {opt}: {res}")

if __name__ == "__main__":
    for src in sys.argv[1:]:
        if has_ub(src):
            print(f"[SKIPPED-UB] {src}")
            continue
        report(src, test_file(src))