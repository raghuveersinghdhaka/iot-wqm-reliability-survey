#!/usr/bin/env python3

import csv, collections, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "S3_consensus_coding_matrix.csv"
rows = list(csv.DictReader(open(os.path.join(HERE, SRC))))
B = ["B1", "B2", "B3", "B4"]
DOMS = ["Urban & industrial", "Rivers & freshwater", "Marine & estuary", "Groundwater",
        "Aquaculture", "Agriculture & soil", "Water level & hydraulic", "Generic & cross-cutting"]

assert len(rows) == 39, len(rows)
core = [r for r in rows if r["tier"] == "W"]
adj = [r for r in rows if r["tier"] == "A"]
print(f"TOTAL {len(rows)} = core {len(core)} + adjacent {len(adj)}")
assert len(core) == 27 and len(adj) == 12

for field in ["year", "venue", "type", "evid"]:
    c = collections.Counter(r[field] for r in rows)
    print(field, dict(sorted(c.items())))

snow = [r["key"] for r in rows if r["snowball_identified"] == "1"]
print("snowball-identified:", snow)

print("\nBridge coverage (works may span bridges): core+adjacent")
for b in B:
    w = sum(1 for r in core if r[b] == "1")
    a = sum(1 for r in adj if r[b] == "1")
    print(f"  {b}: {w + a} total = {w} core + {a} adjacent")

print("\nHeatmap cells  core(adjacent):")
hdr = "bridge".ljust(8) + "".join(d[:14].ljust(16) for d in DOMS)
print(hdr)
for b in B:
    line = b.ljust(8)
    for d in DOMS:
        w = sum(1 for r in core if r[b] == "1" and r["hm_domain"] == d)
        a = sum(1 for r in adj if r[b] == "1" and r["hm_domain"] == d)
        cell = f"{w}" + (f"(+{a})" if a else "") if (w or a) else "--"
        line += cell.ljust(16)
    print(line)

print("\nModalities (B1 works):")
mc = collections.Counter(r["modality_group"] for r in rows if r["B1"] == "1")
for k, v in mc.most_common():
    print(f"  {k}: {v}")
assert sum(mc.values()) == sum(1 for r in rows if r["B1"] == "1")

print("\nEvidence by bridge (L lab / F field / D data-modeling):")
for b in B:
    c = collections.Counter(r["evid"] for r in rows if r[b] == "1")
    print(f"  {b}: " + ", ".join(f"{k}={c.get(k,0)}" for k in ["L", "F", "D"]))
dur = [(r["key"], r["duration"]) for r in rows if r["duration"] not in ("--", "n.r.")]
print("documented durations:", dur)
print("\nAll checks passed.")
