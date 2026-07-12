# Provenance Map

This maps every headline claim, table, and figure in the manuscript to the file(s) and
script(s) behind it, and states plainly whether a reader can reproduce it from this
public repository alone. "Publicly reproducible" means: runnable or checkable using
only what ships in this repo, with no network access and no private-repository file.

Where a script is marked **not** publicly runnable, the underlying *output* is still
shipped and checkable — the distinction is between "you can recompute this number from
this repo" and "you can only inspect the number and the code that produced it, because
the input file lives in the private companion repository." See
`scripts/REPRODUCIBILITY_CHECK.md` for the full clean-room test behind this table.

---

## Headline aggregate numbers

| Manuscript output | Source file(s) | Script(s) | Publicly reproducible from repo alone? | Notes |
|---|---|---|---|---|
| 3,457 pilot facilities; county split King 1,795 / Pierce 1,052 / Spokane 610 | `anonymized_data/WA_AFH_3County_Enriched_ANON.csv` | `verify_headline_numbers.py` | **Yes** | Denominator for every rate in the manuscript. |
| 20,157 licensed beds | `anonymized_data/WA_AFH_3County_Enriched_ANON.csv` (`Licensed_Capacity` sum) | `verify_headline_numbers.py` | **Yes** | |
| 165 facilities with ≥1 enforcement action; 586 with ≥1 investigation | `anonymized_data/WA_AFH_3County_Enriched_ANON.csv` | `verify_headline_numbers.py` | **Yes** | |
| 72 operator clusters; 164 facilities in clusters; largest cluster size 4 | `anonymized_data/WA_Operator_Clusters_ANON.csv` | `verify_headline_numbers.py` | **Yes** | |
| 70 of 72 clusters (97.2%) corroborated | `anonymized_data/WA_Operator_Clusters_Corroboration_ANON.csv` | `verify_headline_numbers.py` (reads this file directly) | **Yes** | |
| 0 exclusion-list name matches (RF-06) | `anonymized_data/WA_AFH_Facility_RedFlags_ANON.csv` | `build_rf_coding.py` (private repo — matching logic runs against the non-anonymized roster) | **Inspectable only** | The 0-match result itself is shipped in the ANON file; the matching *process* needs the private repo's raw facility-name/exclusion-list join. |
| 6,075 statewide licensed AFHs (2026 roster anchor) | `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv` | `build_afh_master.py` (private repo, live DSHS pull) | **Inspectable only** | Statewide roster pull requires network access to DSHS ArcGIS and is a live snapshot — re-running today fetches today's roster, not 2026-06-26. |
| $10.44B (2023-25 enacted) → $13.07B (2025-27 proposed) LTC spending, +25.2% | `wa_data_aggregate/WA_LTC_Spending_Biennia.csv` | `build_charts.py` | **Yes** | Chart-generation only; underlying figures are sourced OFM/DSHS budget documents, cited per row in the CSV. |

## Tables

The mapping below reflects the manuscript's current table numbering, Table 1 through
Table 9.

| Manuscript output | Source file(s) | Script(s) | Publicly reproducible from repo alone? | Notes |
|---|---|---|---|---|
| Table 1 — Minnesota Program-Growth Anchor and Enforcement Warning Signs | `mn_data/MN_Medicaid_Program_Growth_Data.csv`, `mn_data/MN_Medicaid_Master_Evidence_Base.xlsx` | `build_excel.py`, `build_deliverables.py` | **Partially** — source CSVs ship here; the compiled narrative table is hand-assembled from them and the MN evidence base memos. | |
| Table 2 — Minnesota Red-Flag Typology: Public-Data Testability Summary by Category | `WA_RedFlag_Testability_Matrix_v2.csv` | `build_rf_coding.py` (private repo, requires roster join) | **Data file yes; full regeneration no** | The CSV itself ships at repo root and is directly inspectable; regenerating it from scratch requires the private repo's facility-level roster. |
| Table 3 — Reconstructed Washington AFH Growth, 2013–2026 | `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv` | `build_growth.py` | **Yes** | Interpolated years are explicitly flagged `confidence_level = Low` in the CSV. |
| Table 4 — Three-County Pilot Universe | `anonymized_data/WA_AFH_3County_Enriched_ANON.csv` | `verify_headline_numbers.py` | **Yes** | |
| Table 5 — Public Enforcement and Complaint Signals, 2023–2026 | `anonymized_data/WA_AFH_3County_Enriched_ANON.csv`, `anonymized_data/WA_County_Concentration.csv` | `build_normalized.py` (private repo, joins pre-anonymization data) | **Data files yes; full regeneration no** | Both output CSVs ship here and reproduce the table's numbers directly. |
| Table 6 — Illustrative Operator Networks via Shared-Phone Clustering | `anonymized_data/WA_Operator_Clusters_ANON.csv`, `anonymized_data/WA_Operator_Clusters_Corroboration_ANON.csv` | `build_clusters.py` (private repo, requires raw phone field) | **Data files yes; full regeneration no** | Clustering logic needs the raw (non-anonymized) shared-phone key, which does not ship here by design. |
| Table 7 — Comparison-County Normalized AFH Density | `anonymized_data/WA_County_Normalized_Risk.csv` | `build_normalized.py` (private repo) | **Data file yes; full regeneration no** | Uses Census ACS 65+ population as denominator; enforcement/investigation columns are `"not collected in pilot"` outside the three scraped counties, by design. |
| Table 8 (Appendix) — Full Indicator Typology and WA Testability | `WA_RedFlag_Testability_Matrix_v2.csv` | `build_rf_coding.py` | **Data file yes; full regeneration no** | Same file as Table 2, presented at full 20-row detail. |
| Table 9 — Proposed Public-Data Review-Priority Tier Components | `wa_docs/archive/WA_Public_Data_Review_Priority_Tier.md` (archived, never adopted) | `build_final_docs.py` | **Yes** (as a document; the tier logic itself is illustrative and non-validated) | Archived with a prominent warning banner: the manuscript's qualitative Appendix B framing is canonical; this exploratory 0–100 rubric was never applied to any real facility. |

## Figures

| Manuscript output | Source file(s) | Script(s) | Publicly reproducible from repo alone? | Notes |
|---|---|---|---|---|
| Figure 1 — Minnesota HSS Spending Growth vs. Projected Cost | `figures/HSS_Spending_Growth_Chart.png`; data in `mn_data/MN_Medicaid_Program_Growth_Data.csv` | `make_figures.py` | **Yes** | |
| Figure 2 — Reconstructed Washington AFH Growth (2013–2026) | `figures/WA_AFH_Growth_2013_2026.png`; data in `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv` | `build_growth_chart.py` | **Yes** | Hollow markers denote interpolated (Low-confidence) years; solid markers denote official anchors. |
| Figure 3 — AFH Concentration and Enforcement Intensity (King/Pierce/Spokane) | `figures/WA_County_Concentration_Enforcement.png`; data in `anonymized_data/WA_County_Concentration.csv` | `build_charts.py` | **Yes** | |
| Figure 4 — Public-Data Review-Priority Framework: Public Signals and Claims-Informed Expansion | `figures/Fig4_Framework.png` | `make_figures.py` | **Yes** (diagram, no underlying data file) | Conceptual diagram, not a data visualization. |
| Figure 5 — Two-Phase Model: Public-Data Review Priority Followed by Internal Claims Validation | `figures/Fig5_TwoPhase.png` | `make_figures.py` | **Yes** (diagram, no underlying data file) | Conceptual diagram, not a data visualization. |
| Supplementary — WA LTC Spending Growth by Biennium (RF-02 context, not a numbered figure) | `figures/WA_LTC_Spending_Growth.png`; data in `wa_data_aggregate/WA_LTC_Spending_Biennia.csv` | `build_charts.py` | **Yes** | |

## Phase 1 dashboard

| Manuscript output | Source file(s) | Script(s) | Publicly reproducible from repo alone? | Notes |
|---|---|---|---|---|
| Phase 1 dashboard (all tiers, county summaries, sensitivity cube) | `dashboard/phase1_dashboard_data.json`, `dashboard/phase1_tier_config.json`, `dashboard/phase1-dashboard.html` | `build_phase1_dashboard_data.py` | **Yes** | Reads only `anonymized_data/` and `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv`; stdlib only. `validate_phase1_toolkit.py` checks the output stays aggregate-only. |

---

## Oregon replication study (companion, not a manuscript output)

The Oregon replication is not part of the manuscript and not part of this repository; it
now lives in its own repository,
[`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public)
(public) and
[`public-data-review-priority-oregon`](https://github.com/Mohamedn954/public-data-review-priority-oregon)
(private, raw data). See that repository's own provenance documentation for the mapping
from `OR_Replication_Report.md` outputs to source files and scripts.

---

## How to read the "publicly reproducible" column

- **Yes** — Run the listed script(s) against files already in this repo; you get the
  same output. No install beyond the Python standard library for the two flagship
  scripts (`verify_headline_numbers.py`, `build_phase1_dashboard_data.py`); other
  "Yes" rows may need `pip install -r scripts/requirements.txt`.
- **Data file yes; full regeneration no** — The output file ships here and you can
  inspect, re-derive summary statistics from, or re-plot it directly. Re-running the
  *generating* script from scratch requires an intermediate file that lives only in
  the private companion repository (by design — see `README.md`, "What's excluded").
- **Inspectable only** — Neither the raw input nor a reproducible snapshot of it is
  public (e.g., a live government data pull). The code is here for audit; the exact
  historical result is not independently re-derivable from this repo.
- **N/A** — Narrative/qualitative content with no underlying data file.
