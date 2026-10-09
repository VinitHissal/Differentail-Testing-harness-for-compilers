import os, sys, tempfile
from multiprocessing import Pool
from gen import generate
from difftest import has_ub, test_file

def run_one(seed):
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, f"prog_{seed}.c")
        code = generate(seed)
        with open(src, "w") as f:
            f.write(code)
        if has_ub(src):
            return seed, "UB"
        res = test_file(src)
        if any(v[0] in ("COMPILE_ERROR", "TIMEOUT") for v in res.values()):
            return seed, "INFRA_ERROR"
        if len(set(res.values())) == 1:
            return seed, "MATCH"
        res2 = test_file(src)  # retry once to rule out load effects
        if len(set(res2.values())) == 1:
            return seed, "FLAKY"
        os.makedirs("mismatches", exist_ok=True)
        with open(f"mismatches/prog_{seed}.c", "w") as f:
            f.write(code)
        with open(f"mismatches/prog_{seed}.txt", "w") as f:
            for k, v in sorted(res2.items()):
                f.write(f"{k}: {v}\n")
        return seed, "MISMATCH"

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    counts = {}
    with Pool(4) as pool:
        for seed, status in pool.imap_unordered(run_one, range(n)):
            counts[status] = counts.get(status, 0) + 1
            if status in ("MISMATCH", "INFRA_ERROR", "FLAKY"):
                print(f"seed {seed}: {status}")
    print(f"\nPrograms: {n}  Configs per program: 6")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")