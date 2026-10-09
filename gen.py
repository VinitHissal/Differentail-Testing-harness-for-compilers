import random

OPS = ["+", "-", "*", "^", "&", "|"]

def expr(rng, vars_, depth):
    if depth == 0 or rng.random() < 0.3:
        if rng.random() < 0.5:
            return rng.choice(vars_)
        return f"{rng.randint(0, 4000000000)}u"
    a = expr(rng, vars_, depth - 1)
    b = expr(rng, vars_, depth - 1)
    kind = rng.random()
    if kind < 0.65:
        return f"({a} {rng.choice(OPS)} {b})"
    if kind < 0.80:
        return f"({a} << ({b} & 31u))"
    if kind < 0.90:
        return f"({a} >> ({b} & 31u))"
    if kind < 0.95:
        return f"({a} / ({b} | 1u))"
    return f"({a} % ({b} | 1u))"

def stmts(rng, vars_, n, depth):
    lines = []
    for _ in range(n):
        r = rng.random()
        if r < 0.65 or depth == 0:
            lines.append(f"{rng.choice(vars_)} = {expr(rng, vars_, 3)};")
        elif r < 0.85:
            body = stmts(rng, vars_, rng.randint(1, 3), depth - 1)
            lines.append(f"if ({expr(rng, vars_, 2)} % 2u) {{")
            lines += ["    " + l for l in body]
            lines.append("}")
        else:
            k = rng.randint(2, 20)
            body = stmts(rng, vars_, rng.randint(1, 3), depth - 1)
            lines.append(f"for (unsigned i{depth} = 0; i{depth} < {k}u; i{depth}++) {{")
            lines += ["    " + l for l in body]
            lines.append("}")
    return lines

def generate(seed):
    rng = random.Random(seed)
    n_vars = rng.randint(3, 6)
    vars_ = [f"v{i}" for i in range(n_vars)]
    out = ["#include <stdio.h>", "int main(void) {"]
    for v in vars_:
        out.append(f"    unsigned {v} = {rng.randint(0, 4000000000)}u;")
    out += ["    " + l for l in stmts(rng, vars_, rng.randint(5, 12), 2)]
    for v in vars_:
        out.append(f'    printf("%u\\n", {v});')
    out += ["    return 0;", "}"]
    return "\n".join(out) + "\n"

if __name__ == "__main__":
    import sys
    print(generate(int(sys.argv[1]) if len(sys.argv) > 1 else 0))