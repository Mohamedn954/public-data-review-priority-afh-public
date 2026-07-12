# Codebook

This is the file-by-file, field-by-field reference for every dataset shipped in this
repository. It complements `data_guide/00_DATA_AND_ANALYSIS_GUIDE.md` (which describes
*how* each file was built) by giving a compact variable dictionary for each one. Read
this alongside `PROVENANCE_MAP.md`, which maps manuscript claims back to these files.

No file in this repository contains a Washington or Oregon facility name, street
address, telephone number, license number, or exact geocoordinate. See
"De-identification and redaction rules" below for what was removed and why.

---

## Dataset inventory

| Folder | Files | What it is |
|---|---|---|
| `anonymized_data/` | 7 CSVs | The de-identified Washington 3-county pilot dataset (King, Pierce, Spokane). This is the file set `verify_headline_numbers.py` and `build_phase1_dashboard_data.py` read. |
| `wa_data_aggregate/` | 4 CSVs, 1 README | County- and statewide-year aggregates. No facility-level rows. |
| `mn_data/` | 3 CSVs, 1 XLSX | Minnesota public enforcement-record evidence base — the source typology this project adapts. |
| `WA_RedFlag_Testability_Matrix_v2.csv` (repo root) | 1 CSV | The canonical 20-indicator typology and its Washington testability status (manuscript Table 2). |
| `wa_data_aggregate/WA_RedFlag_Testability_Matrix.csv` | 1 CSV | An earlier, superseded version of the same matrix; retained for provenance (see `wa_docs/README.md`). |
| `dashboard/phase1_dashboard_data.json` | 1 JSON | Precomputed aggregate cube behind the Phase 1 dashboard. Generated from `anonymized_data/`. |
The Oregon replication (Clackamas and Washington County, all four facility types) is a
companion methods-transfer study, not part of the manuscript, and not part of this
repository; it lives in its own repository,
[`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public).
See that repository's `README.md` for its file-by-file layout.

---

## File-level summaries and variable dictionaries

### `anonymized_data/WA_AFH_3County_Enriched_ANON.csv` (3,457 rows) — primary analysis file
The master file. One row per licensed Adult Family Home in King, Pierce, or Spokane
county. This is the **denominator** for every rate reported in the manuscript.

| Field | Meaning |
|---|---|
| `facility_id` | Stable synthetic ID (`F00001`...), replaces license number and facility name. |
| `License_Status` | DSHS license status at time of the 2026-06-26 snapshot. |
| `County` | One of King / Pierce / Spokane. |
| `Licensed_Capacity` | Licensed bed count. |
| `Specialty` | DSHS-published specialty designation (e.g., specialized behavior support), where present. |
| `Contract` | Raw DSHS contract-field value. |
| `RCS_Region_Unit` | DSHS regional administrative unit. |
| `Has_Public_Reports` | **Blank for every row.** See "Schema continuity notes" below — not a redaction. |
| `DateAccessed` | Snapshot date for the roster pull (2026-06-26 unless overridden). |
| `Medicaid_Contract_Flag` | Derived. "Yes" if `Contract` is non-blank. **This is a presence proxy, not a verified determination of active Medicaid-contract status, scope, or terms** — it only reflects that the public roster's contract field was populated. |
| `n_inspections`, `n_investigations`, `n_enforcement`, `n_limitations`, `n_civil_fines`, `n_stop_placement`, `n_conditions`, `n_docs_total` | Counts of public documents by category, from the DSHS RCS reports-portal scrape. `n_docs_total` is the sum of the category counts. |
| `latest_year`, `latest_enforcement_year` | Most recent year with any public document / any enforcement document, respectively. |
| `addr_shared_count` | Number of other licenses sharing this facility's normalized address key. Present for completeness; not used as a standalone indicator in the manuscript (see `WA_RedFlag_Testability_Matrix_v2.csv`, RF-08 notes, on why address-sharing is noisier than phone-sharing for this roster). |
| `phone_shared_count` | Number of other licenses (including this one) sharing this facility's normalized phone key. `phone_shared_count ≥ 2` is the basis for `RF03_multi_home_operator`; `≥ 3` for `RF08_network_cluster`. |
| `cluster_id` | `OP001`... if `phone_shared_count ≥ 2`, else blank. Encodes **shared-contact-number membership only** — not a legal or verified finding of common ownership. |

### `anonymized_data/WA_AFH_3County_Reports_ANON.csv` (3,457 rows) — raw scrape output
Same enforcement/inspection counts as the enriched file, but one step earlier in the
pipeline (pre-join, pre-clustering). `fetch_status` records whether the scrape of that
facility's DSHS report page succeeded (`ok`) or failed with an HTTP/network error.
`years_present` is a comma-separated list of years with at least one public document.

### `anonymized_data/WA_AFH_Facility_RedFlags_ANON.csv` (3,457 rows) — indicator coding
One row per facility with the per-facility-computable review-priority indicators coded
as booleans/flags:

| Field | Meaning |
|---|---|
| `RF03_multi_home_operator` | `phone_shared_count ≥ 2` |
| `RF08_network_cluster` | `phone_shared_count ≥ 3` |
| `high_complaint_load` | `n_investigations ≥ 3` |
| `RF06_exclusion_match` | Whether this facility's name matched the WA HCA exclusion/termination list after tokenization. **0 matches found across all 3,457 facilities** — reported as a null finding, not proof of a clean roster (see manuscript limitations and `WA_RedFlag_Testability_Memo.md`). This same 0-match finding also supports RF-17 (payment holds, sanctions, and exclusions — an oversight-failure framing distinct from RF-06's enrollment-screening framing); both RF-06 and RF-17 are legitimately defined as separate indicators in the canonical typology that share this one empirical test. See manuscript Section 6.6. |
| `has_enforcement`, `has_stop_placement`, `has_condition` | Booleans derived from the corresponding `n_*` counts. |

Indicators that require non-public claims data (e.g., billing concentration, RF-10/11
impossible-hours or max-unit billing) are **not** in this file — see
`WA_RedFlag_Testability_Matrix_v2.csv` for which indicators are and are not
public-data-testable, and why.

### `anonymized_data/WA_Operator_Clusters_ANON.csv` (72 rows)
One row per multi-license operator cluster (`phone_shared_count ≥ 2` group).
`n_licenses` is cluster size (2–4 in this pilot); `counties` lists which county/counties
the cluster's facilities are in; `total_enforcement`, `total_investigations`,
`total_civil_fines` are the cluster's summed counts.

### `anonymized_data/WA_Operator_Clusters_Corroboration_ANON.csv` (72 rows)
A supplementary check on the phone-sharing proxy, keyed by the same `cluster_id`.
`corroboration_linkage_method` records what other public record (DSHS primary contact
match, WA Secretary of State CCFS registered agent or principal-office-address match,
or CCFS governor/owner-member match) independently supports common management for that
cluster. `corroboration_status` is `Corroborated` or `Uncorroborated`. 70 of 72 clusters
(97.2%) were corroborated by at least one additional public-record source; this raises
confidence in the proxy without upgrading it to a verified-ownership finding.

### `anonymized_data/WA_County_Concentration.csv` (3 rows) and `WA_County_Normalized_Risk.csv` (9 rows)
County-level aggregates. The 3-row file covers only the pilot counties; the 9-row file
extends to six additional Washington counties for density comparison, using Census ACS
65+ population as the denominator (`AFHs_per_1000_seniors`, etc.). `confidence_level`
in the 9-row file documents that enforcement/investigation rates are only available
(High confidence) for the three scraped counties — the other six carry an explicit
"not collected in pilot" label rather than a blank or an inferred value.

### `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv` (14 rows)
Statewide (not 3-county) active-AFH counts and licensed capacity, 2013–2026.
`confidence_level` distinguishes official DSHS/BERK anchor years (High) from
interpolated years (Low) — see the file itself and `WA_AFH_Growth_2013_2026.png`,
which renders interpolated years as hollow markers.

### `wa_data_aggregate/WA_LTC_Spending_Biennia.csv` (7 rows)
DSHS Long-Term Care biennial appropriation series, 2013-15 through 2025-27.
`appropriation_level` (enacted / approximate / proposed) drives the color-coding in
`figures/WA_LTC_Spending_Growth.png`. Each row carries its own `source`, `source_url`,
`accessed_date`, and `confidence_level` — this is supplementary RF-02 context, not a
numbered manuscript figure.

### `wa_data_aggregate/WA_Medicaid_AFH_Contract_Trends_HISTORICAL.csv` (4 rows)
Historical (2013–2018) statewide Medicaid-contract share for AFHs, from the DSHS BERK
2018 payment-methodology report. Used only to establish that AFHs are a predominantly
Medicaid-funded sector; not part of the 3-county pilot analysis.

### `WA_RedFlag_Testability_Matrix_v2.csv` (repo root, 20 rows) — canonical typology
The manuscript's Table 2. One row per indicator (`RF_ID` = RF-01…RF-20): `Domain`,
`Red_Flag` (the indicator's short name, inherited from the Minnesota source typology),
`Description_of_Alleged_Pattern` (the Minnesota conduct pattern that motivates the
indicator — described as alleged/charged, not adjudicated, except where a conviction is
noted), `WA_Public_Data_Testability` (Yes/Partial/No), `WA_Data_Source`,
`WA_Signal_or_Metric` (what, if anything, stands in for the indicator in Washington
public data), and `Status_Notes`.

### `wa_data_aggregate/WA_RedFlag_Testability_Matrix.csv` (20 rows) — superseded
An earlier version of the same matrix, missing the `Domain` and
`Description_of_Alleged_Pattern` columns and using a since-corrected RF-17 mapping.
Retained for provenance; not used by any current script. See `wa_docs/README.md`.

### `mn_data/MN_Medicaid_Fraud_Cases_Dataset.csv` (22 rows)
Minnesota's public enforcement-record cases: `Defendant`, `Entity`, `Program`,
`Amount`, `Charges`, `Status` (e.g., "Charged (date)", "Under Investigation", or a
noted conviction), `Source`, `Red_Flags` (which RF-## indicator codes the case
exhibits). **All entries are labeled by charge status; none is asserted as adjudicated
guilt unless the `Status` field records a conviction.**

### `mn_data/MN_Medicaid_Program_Growth_Data.csv` (12 rows) and `MN_Medicaid_Revalidation_Data.csv` (10 rows)
Minnesota HCBS program-spending growth series (by program and year) and "Revalidate
2026" provider-revalidation outcome metrics, respectively — both sourced from Minnesota
DHS/OLA public reporting.

### `dashboard/phase1_dashboard_data.json`
Machine-generated aggregate cube (county × cluster-size bucket × enforcement bucket ×
investigation bucket → facility count) that drives the Phase 1 dashboard's client-side
sensitivity controls. Contains no facility-level rows at any threshold setting; see
`scripts/validate_phase1_toolkit.py` for the automated check that enforces this.

### Oregon replication data (separate repository)
De-identified Oregon replication data (`OR_Providers_Enriched_ANON.csv`,
`OR_Reports_ANON.csv`, `OR_Facility_RedFlags_ANON.csv`, `OR_Operator_PhoneClusters_ANON.csv`,
`OR_County_Concentration.csv`, `OR_County_Normalized_Risk.csv`) uses the same
`facility_id`/`cluster_id` de-identification scheme as the Washington files, with an `OR-`
prefix to keep the two datasets visually distinct. This is a companion methods-transfer
study, not a manuscript dataset, and is not part of this repository; see the `README.md`
and `scripts/verify_oregon_numbers.py` in
[`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public)
for the full explanation and the automated headline-number check.

---

## De-identification and redaction rules

Removed from every public file, relative to the private companion repository's raw
data: facility name, physical/mailing address, **city**, telephone number,
contact-person name, DSHS license number, report-portal URL, latitude/longitude, ZIP
code, and the raw shared-phone key used for clustering.

- **Why city was removed:** in smaller jurisdictions, city combined with capacity,
  specialty, and enforcement/complaint counts could narrow a facility down to a small
  enough set to risk re-identification. **County** is retained as the coarsest
  geographic level needed to reproduce the county-level results.
- **`facility_id` and `cluster_id`** are assigned in a fixed order and are stable
  within this release, but carry no information about license number, registration
  date, or phone number.
- **One narrative memo** (`wa_docs/WA_RedFlag_Testability_Memo.md`) has a single
  city-level detail redacted inline, for the same re-identification reason, relative
  to the private repository's version.

## Schema continuity notes

**`Has_Public_Reports` (in `WA_AFH_3County_Enriched_ANON.csv`) is blank for every row.**
This is not a privacy redaction — the same column is blank in the original,
non-anonymized pipeline output. It was never populated by the data-collection scripts
and is superseded by `n_docs_total` (the count of public documents actually found per
facility), which is the field used throughout the analysis. It is left in the schema,
rather than dropped, so the file's column layout stays stable across pipeline runs and
matches the private repository's schema exactly.

## Interpretation cautions

- **`Medicaid_Contract_Flag` is a presence proxy.** A non-blank contract field maps to
  "Yes"; this does not verify current active status, contract scope, or terms.
- **`cluster_id` / `phone_shared_count` are a bounded proxy for shared administrative
  contact, not verified common ownership.** Corroboration (see
  `WA_Operator_Clusters_Corroboration_ANON.csv`) raises confidence for 70 of 72
  clusters but does not convert the proxy into a legal ownership finding.
- **`RF06_exclusion_match = 0` for all facilities is a null finding, not a clean bill of
  health.** The public exclusion list could not be reliably joined to the roster
  because facility "Doing Business As" names rarely match a licensee's legal name.
- **Interpolated years in the growth series carry `confidence_level = Low`** and should
  not be read as official DSHS counts.
- **None of these files identifies, ranks, or makes a finding of wrongdoing against any
  Washington facility or operator.** Every indicator here is a review-priority signal,
  not evidence of fraud, waste, or abuse.

## Relationship to manuscript outputs

Every headline number in the manuscript is reproducible from `anonymized_data/` alone
via `python3 scripts/verify_headline_numbers.py`. For the specific mapping from each
manuscript number, table, and figure to the file(s) and script(s) behind it, see
`PROVENANCE_MAP.md`.

The Oregon replication is a separate, companion study, not part of the manuscript, and now
lives in its own repository,
[`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public);
its own headline numbers are reproducible from that repository's `anonymized_data/` alone
via its `scripts/verify_oregon_numbers.py`.
