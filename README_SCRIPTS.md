# Portable Analysis Scripts

These are the build/analysis scripts with the original hard-coded absolute paths
removed. Paths now resolve relative to the script location, or can be overridden
with environment variables, so the pipeline is reproducible from any checkout.

## Quick start for external reviewers

This public repo supports exactly two actions without needing anything else:

1. **Verify the manuscript's headline numbers** — `python3 scripts/verify_headline_numbers.py`
   (stdlib only, no install step, reads only `anonymized_data/`).
2. **Open or regenerate the Phase 1 dashboard** — open `dashboard/phase1-dashboard.html`
   directly in a browser, or regenerate it with
   `python3 scripts/build_phase1_dashboard_data.py` (stdlib only, reads only
   `anonymized_data/`).

Everything else below (the full 10-step pipeline) is included for **code
transparency and inspection**, not for public rerun — see "What's actually
runnable from this repo" below for exactly why.

## Requirements

- Python 3.9 or later
- Install dependencies with: `pip install -r scripts/requirements.txt`
  (pandas, numpy, matplotlib, requests, openpyxl — exact tested versions pinned
  in that file; only needed for the full pipeline scripts below, not for either
  quick-start action above)

See `REPRODUCIBILITY_CHECK.md` for a clean-clone, clean-venv test run of this
pipeline and what is and is not reproducible from each repository alone.

## Directory layout expected
```
<project_root>/
  ├── scripts/        <- these .py files
  ├── data/           <- intermediate + working CSVs (auto-created)
  ├── sources/        <- raw source inputs (e.g., exclusion lists)
  └── deliverables/   <- final outputs + figures (auto-created)
```

## Configuration (optional environment variables)
- `AFH_PROJECT_ROOT` — base directory (default: the script's own folder)
- `AFH_DATA_DIR`     — working data dir (default: `<root>/data`)
- `AFH_SRC_DIR`      — raw sources dir (default: `<root>/sources`)
- `AFH_OUT_DIR`      — outputs/deliverables dir (default: `<root>/deliverables`)

## Run order (full pipeline, private repo)
1. build_afh_master.py    → statewide AFH roster (ArcGIS pull)
2. build_3county.py       → King/Pierce/Spokane subset
3. scrape_reports.py      → per-facility public-document tallies
4. build_enriched.py      → join + clustering + exclusion check + county table
5. build_clusters.py      → operator clusters
6. build_rf_coding.py     → review-priority indicator coding + corrected RF matrix (WA_RedFlag_Testability_Matrix_v2.csv, corrected RF-17)
7. build_normalized.py    → Census-normalized density/risk
8. build_growth.py / build_growth_chart.py → growth series + chart
9. build_charts.py, make_figures.py → manuscript figures
10. build_anonymized.py   → journal-safe de-identified data package (City removed; IDs only)

Note: scripts that pull live public data (ArcGIS roster, RCS portal scrape) require
network access; intermediate CSVs are provided in the private repo's data package
for offline replication of the analysis steps.

## What's actually runnable from this repo

This public repo ships the scripts above so the analysis logic is auditable, but
most of them **cannot be run to completion here**, by design:

| Scripts | Status in this public repo |
|---|---|
| `build_afh_master.py`, `build_3county.py`, `scrape_reports.py` | **Inspectable only.** These pull live data from DSHS. Re-running them today would fetch today's roster, not the 2026-06-26 snapshot the manuscript analyzes — they cannot reproduce the original result even from the private repo, let alone here. |
| `build_enriched.py` through `build_anonymized.py` (steps 4–10) | **Inspectable only, from this repo.** They expect the intermediate, pre-anonymization CSVs (e.g. `WA_Operator_PhoneClusters.csv`) that live only in the private companion repository, not the de-identified `anonymized_data/` this repo ships. |
| `verify_headline_numbers.py` | **Fully runnable here.** Reads only `anonymized_data/`, stdlib only. |
| `build_phase1_dashboard_data.py` | **Fully runnable here.** Reads only `anonymized_data/` (and the public growth-context CSV), stdlib only. |

See `REPRODUCIBILITY_CHECK.md` for the full clean-room test results behind this table.

## Verifying the manuscript's headline numbers (public repo, no pipeline re-run needed)

`verify_headline_numbers.py` checks the manuscript's headline aggregate numbers
(facility count, beds, county split, enforcement/investigation counts, cluster
counts) directly against `anonymized_data/`. It uses only the Python standard
library — no `requirements.txt` install needed — and does not require any of
the non-public intermediate files described above.

```
python3 scripts/verify_headline_numbers.py
```

## Phase 1 Public-Data Review-Priority Toolkit

See `PHASE1_PUBLIC_DATA_FRAMEWORK.md` (repo root) for the qualitative
review-priority tier definitions and guardrails, and `dashboard/README.md` for
the static, offline dashboard that visualizes them. Regenerate both the
dashboard data and the dashboard HTML with:

```
python3 scripts/build_phase1_dashboard_data.py
```

Like `verify_headline_numbers.py`, this script only reads `anonymized_data/`
and uses only the Python standard library. Phase 1 stops before claims
validation, and nothing it produces should be treated as a fraud score, a
validated predictive model, or an enforcement determination.
