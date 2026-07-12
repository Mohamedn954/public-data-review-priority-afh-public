# A Public-Data Review-Priority Framework for Medicaid Residential Care Oversight — Public Replication Package

This is the **public, journal-safe replication package** for the working paper *"A
Public-Data Review-Priority Framework for Medicaid Residential Care Oversight: Evidence
from Washington State Adult Family Homes"* (Mohamed Noor Hussein).

A companion private repository holds the original, non-anonymized facility-level data (names,
addresses, phone numbers, license numbers) used to produce this package. This repo contains
**no facility-level identifiers**.

> **In one sentence:** this project builds a public-data review-priority layer — adapted from
> Minnesota's public Medicaid enforcement record — for Washington's Adult Family Home sector,
> and stops at the point where claims-informed validation by an authorized state or federal
> body would need to begin.

## Start here, by what you need

| You are a... | Start with |
|---|---|
| **Journal reviewer** | The manuscript is posted on [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7070198); this repo verifies it — run `python3 scripts/verify_headline_numbers.py` to check every headline number against the data itself |
| **Policy reader** | [`POLICY_BRIEF.md`](POLICY_BRIEF.md) — a 2–4 page, non-technical summary of what this project shows, what it doesn't, and what it recommends |
| **Technical replicator** | [`CODEBOOK.md`](CODEBOOK.md) (what every file and field means) and [`PROVENANCE_MAP.md`](PROVENANCE_MAP.md) (which script produced which manuscript number, table, or figure) |

Four things you can do immediately, without cloning anything else or installing any
dependency beyond the Python standard library:

1. **Read the manuscript:** posted on [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7070198); the full text is not included as a file in this repository
2. **Verify the manuscript's headline numbers:** `python3 scripts/verify_headline_numbers.py`
3. **Open or regenerate the Phase 1 dashboard:** open `dashboard/phase1-dashboard.html`
   directly in a browser, or regenerate it with `python3 scripts/build_phase1_dashboard_data.py`
4. **Understand the data/package structure:** [`CODEBOOK.md`](CODEBOOK.md) for file-by-file
   detail, or `data_guide/00_DATA_AND_ANALYSIS_GUIDE.md` for the narrative walkthrough

Everything else in `scripts/` is included for code-transparency and inspection, not
necessarily for public rerun — see `README_SCRIPTS.md` for exactly which scripts are runnable
from this repo alone versus require the private companion repository.

## Guardrails, in brief

This project is a review-priority framework: it does not assign a fraud score,
function as a validated predictive model, or serve as an enforcement determination.
No Washington facility or operator is identified,
ranked, or alleged to have committed fraud. Public signals are intended to clarify what
may warrant closer administrative review and what remains unknowable without internal
claims access, human judgment, and due-process safeguards. See [`GUARDRAILS.md`](GUARDRAILS.md)
for the full statement.

## Contents

| Path | Contents |
|---|---|
| `anonymized_data/` | De-identified replication dataset (3,457 facilities as `facility_id`/`cluster_id`; see `README_ANONYMIZED_DATA.md`) |
| `scripts/` | The full analysis pipeline (portable, path-agnostic); see `README_SCRIPTS.md` for run order |
| `figures/` | The 5 manuscript figures (3 aggregate charts + 2 conceptual diagrams), plus 1 supplementary context chart (`WA_LTC_Spending_Growth.png`, RF-02 background, not a numbered manuscript figure) |
| `data_guide/` | Overview of the full data package and how the pipeline fits together |
| `mn_data/`, `mn_docs/` | Minnesota Medicaid public enforcement-record evidence base used to derive the 20-indicator review-priority typology |
| `wa_docs/` | Narrative memos on Washington data availability, indicator testability, and audit findings — see `wa_docs/README.md` for which are canonical |
| `wa_data_aggregate/` | County/statewide-year aggregate WA data (growth series, contract-rate trends, indicator testability matrix) — no facility-level rows |
| `WA_RedFlag_Testability_Matrix_v2.csv` | The 20-indicator typology (manuscript Table 3) |
| `PHASE1_PUBLIC_DATA_FRAMEWORK.md` | The Phase 1 public-data review-priority toolkit: qualitative tier definitions and guardrails |
| `dashboard/` | A static, offline dashboard visualizing the Phase 1 toolkit's aggregate output; see `dashboard/README.md` |
| `GUARDRAILS.md` | Consolidated one-page statement of what this research is and is not (not a fraud score, not a validated predictive model, not an enforcement determination, etc.) |
| `CODEBOOK.md` | Dataset inventory and variable dictionary, file by file |
| `PROVENANCE_MAP.md` | Manuscript claim/table/figure → source file → script, with a reproducibility flag for each |
| `RELEASE_OVERVIEW.md` | Citation, version, validation status, and this release's relationship to the private companion repository |
| `POLICY_BRIEF.md` | Non-technical summary for state and federal policy audiences |
| [`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public) | A standalone companion study, in its own repository, testing whether this project's pipeline transfers to a second state (Oregon) |

## What's excluded from this public package

The raw, facility-level Washington rosters (license numbers, facility names, street addresses,
phone numbers, exact geocoordinates) are **not included here** — those live only in the private
repository. Every headline aggregate number reported in the manuscript can be independently
verified against `anonymized_data/` alone, using the standalone `scripts/verify_headline_numbers.py`
(no dependencies beyond the Python standard library). Full re-execution of the raw-data
acquisition pipeline (steps 1–3 in `README_SCRIPTS.md`) additionally requires non-public
intermediate files that live only in the private repository — this public package is the
transparent, de-identified evidence layer, not a re-runnable copy of the raw pipeline. See
`scripts/REPRODUCIBILITY_CHECK.md` for the full breakdown of what is and is not reproducible
from each repository alone, and `PROVENANCE_MAP.md` for the same breakdown organized by
manuscript output.

One narrative memo (`wa_docs/WA_RedFlag_Testability_Memo.md`) has a single city-level detail
redacted relative to the private version, because in combination with cluster size and
enforcement counts it could have enabled re-identification of a specific operator — consistent
with the anonymization policy described in `README_ANONYMIZED_DATA.md` (which removes city for
the same reason). The redaction is marked inline.

## Phase 1 Public-Data Review-Priority Toolkit

`PHASE1_PUBLIC_DATA_FRAMEWORK.md` and `dashboard/` are a working implementation of
Phase 1 of the manuscript's two-phase architecture (Section 7): a reproducible,
aggregate-only view of what the public-data indicators look like in practice,
grouping facilities into four qualitative review-priority tiers (Baseline
Monitoring, Elevated Public-Data Review, High Public-Data Review Priority, Claims
Validation Candidate) using rule-based counts of public-data indicators, not a
numeric score. Regenerate the underlying data and dashboard with
`python3 scripts/build_phase1_dashboard_data.py`. As with the rest of this
package, Phase 1 stops before claims validation: no output here functions as a
fraud score, a validated predictive model, or an enforcement determination.

The dashboard includes interactive **aggregate sensitivity controls**: a
county filter, adjustable indicator thresholds within a fixed, pre-approved
range, and indicator on/off toggles, all recomputed client-side from a
precomputed aggregate table with no facility-level row ever exposed. This
is a transparency and sensitivity-analysis feature, not a validation upgrade —
every threshold offered remains illustrative and non-validated, and moving a
control never turns Phase 1 into an operational, predictive, or enforcement
tool. See `dashboard/README.md` and `dashboard/PHASE1_RESULTS_BRIEF.md` for
details, and `scripts/validate_phase1_toolkit.py` to verify the toolkit stays
aggregate-only and de-identified.

## Oregon replication study (companion, not part of the manuscript)

The Oregon replication is a standalone methods-transfer test, not a manuscript finding: it
runs this project's pipeline scripts, unmodified except for file paths and Oregon-specific
field mappings, against public data for two Oregon counties (Clackamas and Washington
County) across all four Oregon-licensed residential facility types (AFH, ALF, RCF, NF). It
now lives in its own dedicated repository,
[`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public),
rather than as a subfolder of this repo. As with the rest of this package, only
de-identified data is included there; raw Oregon data with real names, addresses, and
phone numbers lives only in that repository's private companion,
[`public-data-review-priority-oregon`](https://github.com/Mohamedn954/public-data-review-priority-oregon).
See that repository's `README.md` for the full breakdown of what is public, what is
excluded, and how to verify the numbers yourself.

## Note on evidentiary framing

No Washington facility or operator is alleged to have committed fraud. All indicators in this
package are review-priority signals only, not findings of wrongdoing. Named
Minnesota enforcement cases (`mn_data/MN_Medicaid_Fraud_Cases_Dataset.csv`) are drawn from public
DOJ/court records; charges are allegations unless a conviction is noted. See
[`GUARDRAILS.md`](GUARDRAILS.md) for the consolidated one-page statement of what this research is
and is not.

## License and citation

This repository is licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for
the preferred citation.
