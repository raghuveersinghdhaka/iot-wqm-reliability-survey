# S1. Search and screening protocol

Survey: *A Cross-Layer Survey of Reliability in Low-Cost Internet of Things
Water-Quality Monitoring from Sensing to Decision* (Discover Computing)

## Database and query

- Database: IEEE Xplore (metadata search: title, abstract, index terms).
- Query template: `"water quality" AND X`, with
  `X ∈ {IoT, "Internet of Things", "wireless sensor", LoRa, LPWAN, calibration, "soft sensing"}`,
  together with `"water quality index" AND (IoT OR "wireless sensor")`.
- Filters: peer-reviewed journal articles, English, published January 2011 to 2026.
- Venue frame: IEEE journals (a consequence of the single-database frame, discussed
  under *Threats to validity*, Section 7 of the paper).
- "Recent" throughout the paper refers to this 2011–2026 window.

## Screening

Two stages (title/abstract, then full text) against four eligibility criteria:

- **E1** Peer-reviewed journal article within the search window and venue frame.
- **E2** Presents an IoT or sensor-network *system*, *method*, or *analysis*
  (non-peer-reviewed items, editorials, and works without an IoT/sensing
  component excluded).
- **E3** Targets water-quality monitoring or closely related aquatic/hydrological
  monitoring, or contributes a node-level enabling technology directly
  transferable to it (tier rule below).
- **E4** Reports enough technical detail for per-bridge classification.

Each article was merged with its own supplementary file, and snowballed records
were de-duplicated against the corpus by DOI.

**Caveat (stated in the paper):** stage-level retrieval counts were not logged
during the original search. No PRISMA-style identification funnel is claimed and
retrieval is not claimed to be exhaustive. The auditable screening artifact is the
record-level inclusion log (S2).

## Core / adjacent tier rule

- **Core (W, n=27):** the monitored medium is water and at least one measured or
  inferred quantity is a water-quality parameter or index.
- **Adjacent-enabling (A, n=12):** measures an aquatic/hydrological quantity other
  than quality (water level, flow, groundwater resources) or contributes a
  transferable node- or data-level technique demonstrated outside WQM.

Adjacent works inform per-bridge technique synthesis, but corpus-level gap claims
rest on the core set.

## Bridge coding

Eight axes per work (venue, contribution type, bridges, domain, modality,
connectivity, energy, method) against the rubric of Table 2 of the paper
(a work contributes to a bridge iff it *advances* the operator, not merely uses it).
Two authors independently double-coded the 38 works that entered per-bridge coding
at the structured-search screening stage (κ = 0.91; computation: S5). The five
snowball-identified corpus works (flagged in S2/S3) were coded by the same rubric
after the inter-rater study and are not part of the agreement statistics.

## Snowballing

Backward (reference lists) and forward (citing articles) snowballing from the
primary corpus and from prior reviews identified 7 prior reviews (Section 2.4 of
the paper) and 24 contextual references.
