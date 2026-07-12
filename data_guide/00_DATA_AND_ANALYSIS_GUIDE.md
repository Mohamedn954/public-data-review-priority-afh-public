# Data Package & Analysis Guide
### A Public-Data Review-Priority Framework for Medicaid Residential Care Oversight: Evidence from Washington State Adult Family Homes
**Author:** Mohamed Noor Hussein
**Prepared:** June 27, 2026
**Scope:** Every dataset used in the manuscript, what it contains, where it came from, and exactly what analysis was performed on it.

---

## How this package is organized

This archive contains two evidence bases:

1. **Washington State AFH/HCBS evidence base** (`wa_data/`) — the primary empirical pilot covering King, Pierce, and Spokane counties.
2. **Minnesota Medicaid evidence base** (`mn_data/`) — the enforcement-record anchor used as a structural analogue.

A reproducible-analysis note for each file is given below. All facility-level Washington data was assembled from **public** sources only (DSHS license roster, DSHS RCS public-document portal, WA HCA exclusion list, U.S. Census ACS). No protected health information or non-public claims data was used.

> **Evidentiary discipline.** No Washington provider in these files is alleged to have committed fraud. Facility-level indicators are *review-priority* signals, not findings of wrongdoing. All Minnesota cases are described as **alleged / charged** pending judicial resolution.

---

## PART A — WASHINGTON DATASETS (`wa_data/`)

### A1. `WA_AFH_Facility_Master.csv` — Statewide AFH roster (raw)
- **Rows × cols:** 6,075 × 24 (one row per active AFH license, statewide, deduplicated by license number)
- **Source:** DSHS-published **ArcGIS feature service** "Long Term Care – Residential Care" (the nightly extract behind the official AFH locator), layer `Long_Term_Care_Residential_Care_view/FeatureServer/1`. Accessed 2026-06-26.
- **Key fields:** `License_Number`, `Facility_Name`, `License_Status`, `Physical_Address`, `City`, `ZIP`, `County`, `Phone`, `Licensed_Capacity`, `Specialty`, `Contract` (Medicaid contract designation), `Latitude/Longitude`, `SourceURL`, `DateAccessed`.
- **Analysis performed:** Paginated pull of all features (2,000/page), dedupe by license number, normalization of county/city/phone fields. This is the statewide universe from which the three-county pilot is drawn. Also used to derive the **current 2026 roster count (6,075 active AFHs; 35,305 licensed beds)** that anchors the growth series.

### A2. `WA_AFH_3County_Master.csv` — Three-county pilot subset
- **Rows × cols:** 3,457 × 25
- **Source:** Filtered subset of A1 to `County ∈ {King, Pierce, Spokane}`.
- **Analysis performed:** County filter + `Medicaid_Contract_Flag` derivation from the DSHS contract field. This 3,457-facility file is the **denominator** for every rate in the manuscript. County split: **King 1,795 / Pierce 1,052 / Spokane 610.** `Medicaid_Contract_Flag` is a presence proxy — any non-empty contract-field value maps to "Yes (has DSHS contract)"; it does not verify contract terms, scope, or active status, only that the public roster's contract field was non-blank.

### A3. `WA_AFH_3County_Reports.csv` — Per-facility public-document tallies (scrape)
- **Rows × cols:** 3,457 × 18
- **Source:** DSHS **RCS public-documents portal**, `fortress.wa.gov/dshs/adsaapps/lookup/AFHForms.aspx?lic=<license>`, one request per license (public records per RCW 70.128.280). Accessed 2026-06-26.
- **Analysis performed:** Threaded scrape of each facility's document folder; document URLs classified by folder token into **inspections / investigations / enforcement / limitations / other**. Enforcement subtypes decoded from filenames: `CF` = civil fine, `SP` = stop placement, `Cond` = condition on license. Produces counts: `n_inspections`, `n_investigations`, `n_enforcement`, `n_civil_fines`, `n_stop_placement`, `n_conditions`, `n_docs_total`, plus `latest_year` and `latest_enforcement_year`. This is the source of the **enforcement-intensity** measures.

### A4. `WA_AFH_3County_Enriched.csv` — Master analysis dataset (primary file)
- **Rows × cols:** 3,457 × 41 (**this is the file to use for replication**)
- **Source:** A2 (roster) joined to A3 (document tallies) on `License_Number`, plus derived analytic columns.
- **Analysis performed (the core of the study):**
  - **Operator-network clustering.** Built a normalized `phone_key` and `addr_key`; computed `phone_shared_count` = number of licenses sharing the same phone. Facilities with `phone_shared_count ≥ 2` are flagged as belonging to a multi-license operator cluster.
  - **Exclusion cross-check.** Tokenized facility names (dropping generic tokens like "ADULT FAMILY HOME / LLC / CARE") and matched distinctive tokens against the WA HCA/DSHS termination-and-exclusion list. Result: **0 verified name matches** in the three counties (reported transparently as a null finding).
  - **Enforcement flags.** `has_enforcement`, `has_stop_placement`, `has_condition` booleans from A3 counts.
- **Headline results reproduced from this file:**
  | Metric | King | Pierce | Spokane | Pooled |
  |---|---|---|---|---|
  | Facilities | 1,795 | 1,052 | 610 | 3,457 |
  | In operator clusters | 95 | 47 | 22 | 164 |
  | **Clustering rate** | **5.3%** | **4.5%** | **3.6%** | **4.7%** |
  | Enforcement rate | 4.5% | 5.8% | 3.8% | — |
  - Operator clusters total: **72**; facilities in clusters: **164**; facilities with ≥1 enforcement action: **165**.

### A5. `WA_AFH_Facility_RedFlags.csv` — Facility-level review-priority indicator coding
- **Rows × cols:** 3,457 × 24
- **Source:** Derived from A4 by applying the MN-derived RF-01–RF-20 indicator typology at the facility level.
- **Analysis performed:** Coded the *per-facility computable* review-priority indicators only:
  - `RF03_multi_home_operator` = `phone_shared_count ≥ 2`
  - `RF08_network_cluster` = `phone_shared_count ≥ 3`
  - `high_complaint_load` = `n_investigations ≥ 3`
  - `RF06_exclusion_match` = exclusion-list name hit (0 in pilot)
  - plus `has_enforcement / has_stop_placement / has_condition`.
  Indicators that require non-public claims data (e.g., billing concentration) are **not** coded here and are documented as non-testable in A8.

### A6. `WA_Operator_PhoneClusters.csv` — The 72 operator clusters
- **Rows × cols:** 72 × 8
- **Source:** Aggregation of A4 over `phone_key` for clusters of ≥2 licenses.
- **Analysis performed:** For each cluster: `n_licenses`, member facility names, counties, cities, and summed `total_enforcement / total_investigations / total_civil_fines`. This is the operator-concentration backbone of Section 6.

### A7. `WA_County_Concentration.csv` — County summary table
- **Rows × cols:** 3 × 12 (one row per county)
- **Source:** `groupby(County)` aggregation of A4.
- **Analysis performed:** Per county: facilities, beds, avg beds, count of facilities with enforcement / investigations / stop-placement / conditions, total civil fines, `pct_of_3county_facilities`, `enforcement_rate_pct`, `investigation_rate_pct`.

### A8. `WA_RedFlag_Testability_Matrix.csv` — RF-01–RF-20 testability map
- **Rows × cols:** 20 × 6
- **Source:** Analyst-constructed mapping of each MN-derived indicator to WA public-data availability.
- **Analysis performed:** For each RF: the WA data source, whether it is **publicly testable** (Yes / Partial / No), the WA signal/metric, and status notes. This document defines the *scope and limits* of what public data can support.

### A9. `WA_County_Normalized_Risk.csv` — Population-normalized risk
- **Rows × cols:** 9 × 21
- **Source:** A7 joined to U.S. Census **ACS** population & 65+ counts (via Census Reporter).
- **Analysis performed:** Computed `AFHs_per_1000_seniors`, `beds_per_1000_seniors`, `enforcement_actions_per_1000_seniors`, etc., so counties of different sizes are comparable. Carries `confidence_level` labels.

### A10. `WA_AFH_Growth_2013_2026.csv` — Growth time series
- **Rows × cols:** 14 × 8 (one row per year 2013–2026)
- **Source:** Official DSHS/BERK figures (2013–2018, 2022, 2024) + DSHS ArcGIS current roster (2026); intervening years **interpolated**.
- **Analysis performed:** Assembled a longitudinal active-AFH count. **Every reconstructed year carries an explicit `confidence_level` of "Low" and a note saying it is interpolated, not an official count.** Official anchors are labeled "High". Companion chart: `WA_AFH_Growth_2013_2026.png`.

### A11. `WA_Medicaid_AFH_Contract_Trends_HISTORICAL.csv`
- **Rows × cols:** 4 × 10
- **Source:** DSHS BERK 2018 report, Tables 3.1/3.4 (official).
- **Analysis performed:** Tracks the share of AFHs holding a Medicaid contract (≈88% across 2013–2018), establishing AFHs as a predominantly Medicaid-funded sector.

---

## PART B — MINNESOTA DATASETS (`mn_data/`)

### B1. `MN_Medicaid_Master_Evidence_Base.xlsx` — Master workbook (primary file)
- **Tabs:** README, High-Risk Categories (14), Enforcement Cases (22), Revalidation Data, Program Growth.
- **Source:** DOJ, IRS-CI, MN Attorney General / MFCU press releases; MN DHS; CMS FY2023 PI review; OLA audits. Each row carries a source attribution.
- **Analysis performed:** Consolidation of all MN enforcement and program-integrity evidence into one workbook; basis for the RF-01–RF-20 framework and the MN figures.

### B2. `MN_Medicaid_Fraud_Cases_Dataset.csv` — Charged/alleged cases
- **Rows × cols:** 22 × 8
- **Fields:** `Defendant`, `Entity`, `Program` (HSS/PCA/ICS/IHS/NEMT/ARMHS/HCBS), `Amount`, `Charges`, `Status`, `Source`, `Red_Flags`.
- **Analysis performed:** Each case tagged with the indicator pattern(s) it exhibits (RF-03, RF-09, RF-10, etc.), mapping real enforcement actions to the typology. **All entries labeled by charge status ("Charged (date)", "Under Investigation"); none asserted as adjudicated guilt.**

### B3. `MN_Medicaid_Program_Growth_Data.csv`
- **Rows × cols:** 12 × 4 (`Program`, `Year`, `Spending`, `Source`)
- **Analysis performed:** Program-spending growth series (e.g., Housing Stabilization Services) underlying the MN growth chart (`HSS_Spending_Growth_Chart.png`) and the RF-01/RF-02 rapid-growth argument.

### B4. `MN_Medicaid_Revalidation_Data.csv`
- **Rows × cols:** 10 × 3 (`Metric`, `Value`, `Source`)
- **Analysis performed:** Tabulates MN DHS "Revalidate 2026" provider-revalidation outcomes used to discuss enrollment-integrity screening.

---

## PART C — SUPPORTING DOCUMENTS

Bundled under `wa_docs/` and `mn_docs/`: source bibliographies (with URLs + access dates), the data-availability matrices, the WA↔MN comparison matrix, the readiness memo, the review-priority indicator library (Minnesota source typology), and PDFs of each. The 5 manuscript figures are under `figures/`.

## PART D — ANALYSIS SCRIPTS (`scripts/`)

Every number is reproducible. Run order:
1. `build_afh_master.py` → A1 (pull ArcGIS roster)
2. `build_3county.py` → A2 (county filter)
3. `scrape_reports.py` → A3 (RCS document scrape)
4. `build_enriched.py` → A4 (join + clustering + exclusion check + county table)
5. `build_clusters.py` → A6 (operator clusters)
6. `build_rf_coding.py` → A5, A8 (review-priority indicator coding + testability)
7. `build_normalized.py` → A9 (Census normalization)
8. `build_growth.py` / `build_growth_chart.py` → A10/A11 + chart
9. MN: `build_deliverables.py`, `build_excel.py` → B1–B4
10. `build_charts.py`, `manuscript/make_figures.py` → figures

---

## Confidence & limitations (read before citing)
- **Official, high-confidence:** current AFH roster, per-facility public-document counts, county splits, operator-cluster counts, enforcement counts.
- **Reconstructed/estimated (Low confidence, labeled in-file):** 2019–2021 and 2025 growth-year interpolations.
- **Proxy measures:** operator "clusters" are inferred from *shared phone numbers*, a public proxy for common operation — not a legal finding of common ownership.
- **Null finding (reported honestly):** 0 exclusion-list name matches among the 3,457 pilot facilities.
- Public data cannot test billing-level indicators (no public per-provider Medicaid payment data); those are flagged "No/Partial" in A8.
