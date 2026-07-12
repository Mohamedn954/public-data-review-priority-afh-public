# Anonymized Data Package — A Public-Data Review-Priority Framework for Medicaid Residential Care Oversight (Washington AFHs)

This package is the **journal-safe / replication** version of the Washington pilot
dataset. Because the paper is a review-priority indicator framework, all direct facility
identifiers have been removed and replaced with stable, non-identifying IDs so that
no individual home or operator can be named or re-identified from these files.

## What was removed
Facility names, physical and mailing addresses, **city**, telephone numbers,
contact-person names, DSHS license numbers, report-portal URLs, latitude/longitude,
ZIP codes, and the raw shared-phone key used for clustering. City was removed because
in small towns it could enable re-identification when combined with capacity,
specialty, enforcement/complaint counts, and cluster membership. **County** is
retained as the coarsest geographic level needed to reproduce the county-level
results.

## Note on the `Has_Public_Reports` column
The `Has_Public_Reports` column in `WA_AFH_3County_Enriched_ANON.csv` is present
but blank for every row. This is not a privacy redaction: the same column is
blank in the original, non-anonymized pipeline output as well. It was never
populated by the data-collection scripts and is superseded by `n_docs_total`
(the count of public documents found per facility), which is the field
actually used throughout the analysis. The column is left in place for
schema consistency with the pipeline rather than removed.

## ID scheme
- `facility_id` (e.g., `F00001`) — a stable per-facility identifier, assigned in a
  fixed order. Replaces the DSHS license number and facility name.
- `cluster_id` (e.g., `OP001`) — a stable identifier for a multi-license operator
  cluster (two or more licenses sharing one public contact number). A blank
  `cluster_id` means the facility is not part of a multi-home cluster. Replaces the
  raw shared-phone key. `cluster_id` encodes **membership only**; it does not reveal
  the underlying phone number and is not an assertion of verified common ownership.

## Files (all seven are included in this package)
- `WA_AFH_3County_Enriched_ANON.csv` — master analysis file (3,457 rows). All
  enforcement/complaint counts, capacity, county, contract flag, and cluster
  membership retained.
- `WA_AFH_3County_Reports_ANON.csv` — per-facility public-document tallies.
- `WA_AFH_Facility_RedFlags_ANON.csv` — facility-level review-priority indicator coding.
- `WA_Operator_Clusters_ANON.csv` — the 72 operator clusters (cluster_id, size,
  counties, aggregate enforcement/investigation/civil-fine counts).
- `WA_Operator_Clusters_Corroboration_ANON.csv` — supplementary corroboration
  check (72 rows, keyed by the same `cluster_id` values used in
  `WA_Operator_Clusters_ANON.csv`) recording, per cluster, the linkage method
  used to corroborate shared management (e.g., "DSHS Primary Contact," "CCFS
  Registered Agent or Principal-Office Address," "CCFS Governor
  (Owner/Member)") and a `corroboration_status` of "Corroborated" or
  "Uncorroborated." All 72 clusters were evaluated; 70 (97.2%) had
  additional public-record cross-check support.
- `WA_County_Concentration.csv` — county-level aggregates; no facility identifiers;
  unchanged.
- `WA_County_Normalized_Risk.csv` — county-level Census-normalized density/risk; no
  facility identifiers; unchanged.

## Reproducibility
Every headline figure in the manuscript reproduces from these files:
3,457 facilities; 20,157 licensed beds; 164 facilities in operator clusters across
72 clusters (15 with three or more homes); 165 facilities with at least one
enforcement action; county split King 1,795 / Pierce 1,052 / Spokane 610.

## Note on evidentiary framing
No Washington facility in these files is alleged to have committed fraud. Indicators
are review-priority signals only, not findings of wrongdoing.
