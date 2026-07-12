# Phase 1 Public-Data Review-Priority Dashboard

An interactive, static, offline dashboard that visualizes the Phase 1 public-data
review-priority toolkit described in `PHASE1_PUBLIC_DATA_FRAMEWORK.md`. It is
aggregate-only: no facility name, address, license number, phone number, URL,
city, ZIP, latitude/longitude, or other provider-identifying detail is read,
computed, or displayed anywhere in this folder. It is a non-operational
prototype: not a fraud-detection tool, not a validated predictive model, not a
risk-scoring or facility-ranking system, and not a basis for enforcement action.

## What's in this folder

- `phase1-dashboard.html` — the dashboard itself. Open it directly in any
  browser; no server, build step, or network connection is required. All data
  and configuration are embedded directly in the page (see "How it works"
  below), so there is no `fetch()`, `XMLHttpRequest`, `WebSocket`, or external
  script/stylesheet reference anywhere in the file.
- `phase1_dashboard_data.json` — the same aggregate data as a standalone JSON
  file, for anyone who wants to inspect or reuse the numbers without opening
  the dashboard.
- `phase1_tier_config.json` — the default and allowed threshold values the
  dashboard's sensitivity controls use, with labels explaining that every
  threshold is illustrative and non-validated.
- `PHASE1_RESULTS_BRIEF.md` — a one-page, plain-English explanation of what
  the dashboard shows, why the top tier may show few or no facilities under
  conservative thresholds, and what would be required to go further.

## Input files

All three generated files above come entirely from public, de-identified data
already in this repository:

- `anonymized_data/WA_AFH_3County_Enriched_ANON.csv`
- `anonymized_data/WA_Operator_Clusters_ANON.csv`
- `anonymized_data/WA_Operator_Clusters_Corroboration_ANON.csv`
- `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv` (growth-context panel only)

## Dynamic controls

The dashboard is interactive, not a static snapshot:

- **County filter** — view statewide (3-county) or single-county metrics.
- **Threshold controls** — adjust the Network Concentration (2+/3+/4+
  licenses), Enforcement Intensity (1+/2+/3+ actions), and
  Complaint/Investigation Load (1+/2+/3+ investigations) thresholds within
  the bounds set in `phase1_tier_config.json`. Network Concentration is a
  shared-contact proxy (licenses sharing a public phone number), not verified
  ownership — see `PHASE1_PUBLIC_DATA_FRAMEWORK.md`.
- **Indicator toggles** — include or exclude any of the three public-data
  indicators from the tier and overlap calculation entirely.
- **Reset to default thresholds** — returns every control to the manuscript's
  Appendix B defaults (3 licenses / 2 actions / 3 investigations).

Changing any control immediately recomputes and redraws the review-priority
tier distribution, the indicator-overlap breakdown, the headline metrics, and
the sensitivity note describing the current settings in plain language.

## Threshold sensitivity analysis

The recompute is driven entirely by `sensitivity_cube` inside
`phase1_dashboard_data.json` — a precomputed, aggregate county-level
histogram of bucketed indicator values (cluster size, enforcement count,
investigation count), built once at generation time. No facility-level row
is ever sent to the browser: the cube is mathematically sufficient to
recompute exact tier and overlap counts for any threshold combination
`phase1_tier_config.json` allows, entirely client-side, with nothing beyond
aggregate counts ever leaving the build script. `PHASE1_PUBLIC_DATA_FRAMEWORK.md`
has the full explanation of why this is a sensitivity-analysis feature and not
a modeling upgrade — the underlying rule is still just an indicator count.

## Export buttons

Two buttons let you save the *current* view (whatever county filter,
thresholds, and toggles are active) as a file:

- **Export current aggregate summary (JSON)** — the current thresholds,
  county filter, indicator toggles, and resulting tier/overlap counts.
- **Export current aggregate summary (CSV)** — the same information as flat
  rows.

Both exports contain aggregate counts and the current control settings only.
Neither ever includes a facility ID, provider ID, or any other identifying
detail — there is nothing identifying in the underlying data for an export to
leak in the first place.

## Regenerating the dashboard

Run the build script from the repository root:

```
python3 scripts/build_phase1_dashboard_data.py
```

This writes `dashboard/phase1_dashboard_data.json` and
`dashboard/phase1_tier_config.json`, and regenerates
`dashboard/phase1-dashboard.html` from `scripts/phase1-dashboard.template.html`,
so all three files never drift out of sync with each other. There is no
separate "build the HTML" step — one command keeps everything current.

## Validating the toolkit

```
python3 scripts/validate_phase1_toolkit.py
```

Checks that the dashboard JSON/HTML exist, that tier and county totals
reconcile against the total facility count, that no facility ID or prohibited
wording appears anywhere in the outputs, and that the dashboard makes no
external network call of any kind. Prints a PASS/FAIL line per check.

## Limitations and guardrails

- **This is Phase 1 only.** The dashboard shows public-data review-priority
  tiers, not claims-validated findings. No threshold setting it offers turns
  a tier into a fraud score, a validated predictive model, or an enforcement
  determination. See `PHASE1_PUBLIC_DATA_FRAMEWORK.md` for the full
  guardrails.
- **Aggregate only, by design.** The dashboard cannot and does not show,
  rank, or single out any individual facility, at any setting.
- **Thresholds are illustrative, not validated.** Moving a slider changes
  which public-data pattern counts as notable; it does not add evidence and
  does not create a validated risk model. Sensitivity analysis is not an
  operational recommendation.
- **Snapshot, not live data.** The dashboard reflects the same DSHS/SAO/Census
  snapshot (accessed 2026-06-26) used throughout the manuscript and
  replication package. Rerun the build script against a newer
  `anonymized_data/` snapshot to refresh it.
- **Three-county pilot, not statewide.** All figures describe King, Pierce,
  and Spokane counties only, consistent with the manuscript's stated scope.
- **Washington only.** This dashboard's interactive controls and sensitivity
  cube are built from Washington data only. It does not include Oregon.
  The Oregon replication (`public-data-review-priority-oregon-public`, a
  separate companion repository) is a standalone methods-transfer study (not
  a manuscript output) testing whether this project's pipeline transfers to
  a second state; it does not have its own interactive dashboard.
- **Requires human review, claims validation, and due process** before any
  operational use, regardless of which thresholds or toggles are selected.
