#!/usr/bin/env python3

import csv, sys

def load(p):
    return {r["key"]: [int(r[b]) for b in ("B1", "B2", "B3", "B4")]
            for r in csv.DictReader(open(p))}

def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    p1a, p1b = sum(a) / n, sum(b) / n
    pe = p1a * p1b + (1 - p1a) * (1 - p1b)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")

if __name__ == "__main__":
    A, Bc = load(sys.argv[1]), load(sys.argv[2])
    keys = sorted(set(A) & set(Bc))
    flatA = [v for k in keys for v in A[k]]
    flatB = [v for k in keys for v in Bc[k]]
    po, k = kappa(flatA, flatB)
    print(f"{len(keys)} works, {len(flatA)} decisions: agreement={100*po:.1f}%  kappa={k:.2f}")
    for i, b in enumerate(("B1", "B2", "B3", "B4")):
        po_b, k_b = kappa([A[k_][i] for k_ in keys], [Bc[k_][i] for k_ in keys])
        print(f"  {b}: agreement={100*po_b:.1f}%  kappa={k_b:.2f}")
