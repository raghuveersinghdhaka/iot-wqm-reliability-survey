# Reproducibility package for the cross-layer survey of reliability in low-cost IoT water-quality monitoring

Supplementary material (S1–S7) for:

> R. S. Dhaka, M. Khurana, S. Lamba, M. Sharma,
> *A Cross-Layer Survey of Reliability in Low-Cost Internet of Things Water-Quality Monitoring from Sensing to Decision*,
> Discover Computing (Springer Nature).

This package is cited by the article's **Data availability** and **Code availability**
statements. It contains the complete search protocol, the record-level screening log,
the consensus coding matrix behind every count, table, and figure of the survey, the
inter-coder agreement computation, the fully specified illustrative uncertainty budget,
and the scripts that recompute the corpus statistics and plot the data-driven figures.

## Contents

| File | Contents |
|---|---|
| `S1_search_protocol.md` | Full search protocol: query strings, fields, window, filters, eligibility criteria E1–E4, tier rule, coding-rubric summary, snowballing procedure. |
| `S2_inclusion_log.csv` | Record-level inclusion log: every record that reached full-text screening, with decision, tier, snowball flag, and reason. |
| `S3_consensus_coding_matrix.csv` | Consensus coding matrix for the 39-work corpus: bridges (B1–B4), tier, fine/heatmap domain, modality group, method, evidence class, duration, snowball flag, justification. |
| `S4_domain_crosswalk.csv` | Mapping from study-level domains to the eight domain groups of the coverage analysis. |
| `S5_intercoder_kappa.py` | Percent agreement and Cohen's κ (overall and per bridge) from two coder matrices. |
| `S6_uncertainty_budget.py` | Fully specified illustrative uncertainty budget of Section 2.2 and the complete sensitivity analysis; running it reproduces every number in Tables 3–5. |
| `S7_corpus_stats.py` | Prints every corpus statistic used in the paper, with internal consistency checks. |
| `S7_make_figures.py` | Plots the data-driven figures (Figs. 4, 5, 6, 8 and 9) from `S3_consensus_coding_matrix.csv`; every count, score and label matches the published figures. |
| *(pre-reconciliation sheets)* | Not retained as separate files (see Notes). |
| `requirements.txt` | Python dependency of the figure script (matplotlib). |

## Quick start

Python ≥ 3.9. Only the figure script needs a third-party package (matplotlib); the other
scripts use the standard library.

```bash
pip install -r requirements.txt   # matplotlib, for S7_make_figures.py

python3 S6_uncertainty_budget.py   # Tables 3–5: u_B1=2.99, u(WQI)=4.74, P(wrong call)=14.6%, all sensitivity rows
python3 S7_corpus_stats.py         # every corpus count (39 = 27 core + 12 adjacent; B1 25 / B2 17 / B3 15 / B4 15; …)
python3 S5_intercoder_kappa.py <coderA.csv> <coderB.csv> # the agreement/κ computation used at coding time
python3 S7_make_figures.py         # writes Figs. 4, 5, 6, 8 and 9 to ./figures/
```

## Figure files

`S7_make_figures.py` writes files named as the paper's figure files:

| Output file | Paper figure |
|---|---|
| `fig3_corpus_landscape.pdf` | Fig. 4 (bibliometric landscape) |
| `figS1_sensing_modalities.pdf` | Fig. 5 (B1 sensing modalities) |
| `figS2_connectivity.pdf` | Fig. 6 (B2 qualitative connectivity comparison) |
| `figS3_methods.pdf` | Fig. 8 (B3/B4 technique distribution) |
| `fig5_bridge_domain_heatmap.pdf` | Fig. 9 (bridge × domain coverage grid) |

The plots use the Inter typeface when it is installed and fall back to DejaVu Sans
otherwise.

## Notes

- `S3_consensus_coding_matrix.csv` is the single source of the corpus counts reported
  in the survey; `S7_corpus_stats.py` recomputes them from it and enforces the
  consistency checks.
- The uncertainty budget is an **illustrative, conditional** calculation under the
  stated error model (see Section 2.2 of the paper). It is not a measurement of a
  deployed system.
- The five snowball-identified corpus works are flagged in `S2`/`S3`. They were coded
  against the same rubric after the inter-rater study and are not part of the
  agreement statistics.
- The two coders' pre-reconciliation working sheets were consumed during the
  reconciliation discussions and were not retained as separate files. `S5` is the
  script used at the time. The consensus matrix and the reported per-bridge
  statistics (95.4% agreement, κ = 0.91, seven secondary-bridge disagreements over
  the 38 double-coded works) are the surviving record of that exercise.
