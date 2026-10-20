#!/usr/bin/env python3

import csv, os, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_hex
from matplotlib import font_manager
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures"); os.makedirs(OUT, exist_ok=True)
SRC = "S3_consensus_coding_matrix.csv"
rows = list(csv.DictReader(open(os.path.join(HERE, SRC))))
core = [r for r in rows if r["tier"] == "W"]
adj = [r for r in rows if r["tier"] == "A"]
B = ["B1", "B2", "B3", "B4"]
BCOL = {"B1": "#2a9d8f", "B2": "#457b9d", "B3": "#e9c46a", "B4": "#e76f51"}
BLAB = {"B1": "B1\nSensing", "B2": "B2\nConnectivity", "B3": "B3\nData quality", "B4": "B4\nInference\n& decision"}
plt.rcParams.update({"font.size": 8, "axes.titlesize": 9, "axes.linewidth": 0.8,
                     "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "pdf.fonttype": 3})
if any(f.name == "Inter" for f in font_manager.fontManager.ttflist):
    plt.rcParams["font.family"] = "Inter"  

def despine(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


fig, axs = plt.subplots(2, 2, figsize=(7.2, 4.8))
yrs = [str(y) for y in (2011, 2014, 2021, 2022, 2023, 2024, 2025, 2026)]
yc = collections.Counter(r["year"] for r in rows)
ax = axs[0, 0]
YRCOL = LinearSegmentedColormap.from_list("yr", ["#d9efe9", "#2a9d8f", "#264653"])
bars = ax.bar(yrs, [yc[y] for y in yrs], color=[to_hex(YRCOL(i / 7)) for i in range(8)], width=0.62)
ax.bar_label(bars, fontsize=7)
ax.set_title("(a) Publications per year", fontsize=8.5)
ax.set_ylabel("No. of works", fontsize=8)
ax.set_ylim(0, 12)
ax.tick_params(axis="x", rotation=38)
despine(ax)

ax = axs[0, 1]
ven = [("IEEE\nSensors J.", "Sensors J."), ("IEEE\nIoT J.", "IoT J."), ("IEEE\nAccess", "Access"), ("IEEE\nOJIES", "OJIES")]
vc = collections.Counter(r["venue"] for r in rows)
bars = ax.bar([v[0] for v in ven], [vc[v[1]] for v in ven],
             color=["#2a9d8f", "#e9c46a", "#457b9d", "#e76f51"], width=0.55)
ax.bar_label(bars, fontsize=7)
ax.set_title("(b) Publications per venue", fontsize=8.5)
ax.set_ylim(0, 24)
despine(ax)

ax = axs[1, 0]
tc = collections.Counter(r["type"] for r in rows)
tl = [("System /\nimpl.", "System"), ("Data-driven\nmethod", "Method"), ("Analytical /\nmodeling", "Analytic")]
bars = ax.bar([t[0] for t in tl], [tc[t[1]] for t in tl],
             color=["#2a9d8f", "#e9c46a", "#457b9d"], width=0.5)
ax.bar_label(bars, fontsize=7)
ax.set_title("(c) Contribution type", fontsize=8.5)
ax.set_ylabel("No. of works", fontsize=8)
ax.set_ylim(0, 24)
despine(ax)

ax = axs[1, 1]
wcnt = [sum(1 for r in core if r[b] == "1") for b in B]
acnt = [sum(1 for r in adj if r[b] == "1") for b in B]
x = range(4)
ax.bar(x, wcnt, color=[BCOL[b] for b in B], width=0.55)
ax.bar(x, acnt, bottom=wcnt, color=[BCOL[b] for b in B], alpha=0.42, hatch="///",
       edgecolor="white", linewidth=0.4, width=0.55)
for i, (w, a) in enumerate(zip(wcnt, acnt)):
    ax.text(i, w + a + 0.45, str(w + a), ha="center", fontsize=7.5)
ax.set_xticks(list(x))
ax.set_xticklabels([BLAB[b] for b in B], fontsize=7)
ax.set_title("(d) Coverage per reliability bridge", fontsize=8.5)
ax.set_ylabel("No. of contributing works", fontsize=8)
ax.set_ylim(0, 30)
ax.text(0.97, 0.955, "works may span\nmultiple bridges", transform=ax.transAxes,
        ha="right", va="top", fontsize=6.5, style="italic", color="#444444")
ax.legend(handles=[Patch(facecolor="#9a9a9a", label="core water-quality studies"),
                   Patch(facecolor="#9a9a9a", alpha=0.42, hatch="///", edgecolor="white", label="adjacent-enabling studies")],
          fontsize=6.3, frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.86))
despine(ax)
fig.tight_layout(w_pad=2.2, h_pad=1.8)
fig.savefig(os.path.join(OUT, "fig3_corpus_landscape.pdf"))
plt.close(fig)


DOMS = ["Urban & industrial", "Rivers & freshwater", "Marine & estuary", "Groundwater",
        "Aquaculture", "Agriculture & soil", "Water level & hydraulic", "Generic & cross-cutting"]
DLAB = ["Urban/\nindustrial", "Rivers/\nFreshwater", "Marine/\nEstuary", "Groundwater",
        "Aquaculture", "Agriculture/\nSoil", "Water-level/\nHydraulic", "Cross-cutting/\nGeneric"]
Wm = [[sum(1 for r in core if r[b] == "1" and r["hm_domain"] == d) for d in DOMS] for b in B]
Am = [[sum(1 for r in adj if r[b] == "1" and r["hm_domain"] == d) for d in DOMS] for b in B]
tot = [[w + a for w, a in zip(wr, ar)] for wr, ar in zip(Wm, Am)]
cmap = LinearSegmentedColormap.from_list("pap", ["#f2fafb", "#b8e0e2", "#699db3", "#1d3557"])
fig, ax = plt.subplots(figsize=(7.55, 3.2))
im = ax.imshow(tot, cmap=cmap, vmin=0, vmax=10, aspect="auto")
for i in range(4):
    for j in range(8):
        w, a, t = Wm[i][j], Am[i][j], tot[i][j]
        dark = t > 5
        col = "white" if dark else "#1d3557"
        if t == 0:
            ax.text(j, i, "—", ha="center", va="center", color="#b0413e", fontsize=11, fontweight="bold")
        elif a == 0:
            ax.text(j, i, str(w), ha="center", va="center", color=col, fontsize=9)
        else:
            ax.text(j, i - 0.09, str(w), ha="center", va="center", color=col, fontsize=9)
            ax.text(j, i + 0.26, f"(+{a})", ha="center", va="center", color=col, fontsize=6.4)
ax.set_xticks(range(8)); ax.set_xticklabels(DLAB, fontsize=7)
ax.set_yticks(range(4))
ax.set_yticklabels(["B1 Sensing", "B2 Connectivity", "B3 Data quality", "B4 Inference\n& decision"], fontsize=7.5)
ax.set_title("Coverage across reliability bridges and application domains (— marks a research gap)", fontsize=9)
ax.set_xticks([x - 0.5 for x in range(1, 8)], minor=True)
ax.set_yticks([y - 0.5 for y in range(1, 4)], minor=True)
ax.grid(which="minor", color="white", linewidth=1.6)
ax.tick_params(which="both", length=0)
cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.015)
cb.set_label("No. of surveyed works", fontsize=7.5)
cb.ax.tick_params(labelsize=7)
ax.text(0.5, -0.30, "cell entries: core water-quality studies, with adjacent-enabling studies in parentheses",
        transform=ax.transAxes, ha="center", fontsize=6.6, style="italic", color="#444444")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig5_bridge_domain_heatmap.pdf"))
plt.close(fig)


MOD = [
    ("Electrochemical / potentiostat", "direct", r"$\mathregular{NO_3^-,\ NH_4^+,\ Ca^{2+}}$, COD, phosphate, pH"),
    ("Optical (fluoro/nephelometric)", "direct", "turbidity, Chl-a, phycocyanin"),
    ("Ion-selective electrode (ISE)", "direct", r"$\mathregular{NO_3^-,\ H_2PO_4^-,\ K^+}$"),
    ("Colorimetric", "direct", "nitrite"),
    ("Spectrophotometric", "direct", "multi-channel absorbance, coliforms"),
    ("Fiber-optic grating (FBG/TFBG)", "mixed", "pressure, water level, pH"),
    ("Integrated CMOS multiparameter", "mixed", "temperature, humidity, soil moisture"),
    ("RFID backscatter", "phys", "liquid level"),
    ("Beat-sensor / antenna", "phys", "water level (RMSE 2.5 mm)"),
    ("Image / vision", "phys", "groundwater flow velocity & direction"),
    ("Piezoelectric (flexible)", "phys", "tactile force / energy harvesting"),
    ("COTS probe arrays", "mixed", "pH, DO, EC, ORP, temperature"),
]
GCOL = {"direct": "#2a9d8f", "mixed": "#7ca6bf", "phys": "#457b9d"}
mcnt = collections.Counter(r["modality_group"] for r in rows if r["B1"] == "1")
name_map = {"Optical (fluoro/nephelometric)": "Optical (fluoro-nephelometric)", "Beat-sensor / antenna": "Beat sensor / antenna"}
fig, ax = plt.subplots(figsize=(7.6, 4.8))
ys = range(len(MOD) - 1, -1, -1)
for y, (name, grp, note) in zip(ys, MOD):
    n = mcnt.get(name_map.get(name, name), 0)
    ax.barh(y, n, color=GCOL[grp], height=0.62)
    ax.text(n + 0.18, y, str(n), va="center", fontsize=9)
    ax.text(n + 1.15, y, note, va="center", fontsize=8, style="italic", color="#555555")
ax.set_yticks(list(ys)); ax.set_yticklabels([m[0] for m in MOD], fontsize=9)
ax.tick_params(axis="x", labelsize=9)
ax.set_xlabel("No. of surveyed works", fontsize=9.5)
ax.set_xlim(0, 18)
ax.set_title("Low-cost sensing modalities in the surveyed corpus (Bridge B1)", fontsize=10.5)
ax.legend(handles=[Patch(facecolor=GCOL["direct"], label="direct chemical/biochemical readout"),
                   Patch(facecolor=GCOL["mixed"], label="mixed / configurable"),
                   Patch(facecolor=GCOL["phys"], label="physical / proxy readout")],
          fontsize=8.5, frameon=False, loc="center right")
despine(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "figS1_sensing_modalities.pdf"), dpi=600)
plt.close(fig)


LEV = {"v.high": ("#9d2226", "white"), "high": ("#e76f51", "white"),
       "med": ("#e9c46a", "#3a3a3a"), "low": ("#f4f1de", "#3a3a3a")}
ROWS = [
    ("PHY / MAC protocol families", None),
    ("LoRa / LoRaWAN", ["v.high", "low", "v.high", "high", "v.high"]),
    ("Smart Utility Network (SUN)", ["high", "med", "high", "high", "med"]),
    ("Wi-Fi", ["low", "v.high", "med", "low", "high"]),
    ("Classic WSN (ZigBee/802.15.4)", ["med", "med", "high", "med", "high"]),
    ("Link & relay architectures", None),
    ("Directional microwave link", ["v.high", "v.high", "low", "med", "low"]),
    ("RFID backscatter", ["low", "low", "v.high", "med", "v.high"]),
    ("Aerial relay (UAV / LAP)", ["v.high", "high", "low", "v.high", "low"]),
]
COLS = ["Range", "Data\nrate", "Energy\nefficiency", "Over-water\nrobustness", "Low\ncost"]
fig, ax = plt.subplots(figsize=(6.3, 4.15))
ax.set_xlim(0, 5); ax.set_ylim(0, len(ROWS)); ax.axis("off")
ax.set_title("Qualitative comparison of over-water connectivity (Bridge B2)", fontsize=9.5, pad=18)
for j, cl in enumerate(COLS):
    ax.text(j + 0.5, -0.25, cl, ha="center", va="top", fontsize=7.5)
y = len(ROWS)
for name, scores in ROWS:
    y -= 1
    if scores is None:
        ax.text(-0.12, y + 0.5, name, ha="right", va="center", fontsize=7.6,
                fontweight="bold", color="#264653", style="italic")
        continue
    ax.text(-0.12, y + 0.5, name, ha="right", va="center", fontsize=7.5)
    for j, s in enumerate(scores):
        bg, fg = LEV[s]
        ax.add_patch(plt.Rectangle((j + 0.02, y + 0.06), 0.96, 0.88, facecolor=bg, edgecolor="white", lw=1.2))
        ax.text(j + 0.5, y + 0.5, s, ha="center", va="center", fontsize=7.3, color=fg)
ax.text(2.5, -1.25, "Ordinal synthesis (1 low – 4 very high) of corpus deployment evidence against the stated anchors;\nnot a measured benchmark and not a ranking of methods.",
        ha="center", va="top", fontsize=6.4, style="italic", color="#444444")
ax.set_ylim(-2.1, len(ROWS))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "figS2_connectivity.pdf"), bbox_inches="tight")
plt.close(fig)


TECH = [
    ("Calibration / drift correction", 1, "B3"),
    ("Interference / artefact correction", 4, "B3"),
    ("Anomaly & data-quality assessment", 3, "B3"),
    ("In-sensor / edge pre-processing", 1, "B3"),
    ("Reconstruction / matrix mapping", 1, "B3"),
    ("Regression (linear / polynomial)", 1, "B4"),
    ("Neural soft-sensing (GRNN/MPR)", 1, "B4"),
    ("Multimodal / spatiotemporal fusion", 1, "B4"),
    ("Forecasting (model-based)", 1, "B4"),
    ("Index weighting (WQI / PCA / entropy)", 2, "B4"),
    ("Digital twin", 1, "B4"),
    ("Game-theoretic decision", 1, "B4"),
    ("MCDM / fuzzy routing", 1, "B4"),
    ("Kalman / link propagation", 1, "B4"),
    ("Control / actuation", 2, "B4"),
    ("ML level estimation", 1, "B4"),
]
fig, ax = plt.subplots(figsize=(7.05, 4.6))
ys = range(len(TECH) - 1, -1, -1)
for y, (name, n, br) in zip(ys, TECH):
    ax.barh(y, n, color=BCOL[br], height=0.6)
    ax.text(n + 0.07, y, str(n), va="center", fontsize=7.5)
ax.set_yticks(list(ys)); ax.set_yticklabels([t[0] for t in TECH], fontsize=7.3)
ax.set_xlabel("No. of surveyed works", fontsize=8)
ax.set_xlim(0, 5)
ax.set_title("Data-quality and inference techniques in the surveyed corpus", fontsize=9)
ax.legend(handles=[Patch(facecolor=BCOL["B3"], label="B3  data-quality methods"),
                   Patch(facecolor=BCOL["B4"], label="B4  inference & decision methods")],
          fontsize=6.8, frameon=False, loc="lower right")
despine(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "figS3_methods.pdf"))
plt.close(fig)

print("figures written to", os.path.abspath(OUT))
