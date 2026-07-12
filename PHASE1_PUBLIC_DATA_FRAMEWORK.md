# Phase 1 Public-Data Review-Priority Toolkit

## Purpose

This toolkit is a working implementation of **Phase 1** of the two-phase review-priority
architecture described in the manuscript (*A Public-Data Review-Priority Framework for
Medicaid Residential Care Oversight: Evidence from Washington State Adult Family Homes*,
Section 7). It turns the manuscript's public-data indicators into a
reproducible, aggregate-only dashboard so a reader can see what a public-data
review-priority layer would actually look like in practice — without touching claims
data, without scoring individual providers, and without asserting fraud.

It is deliberately narrow in scope. It demonstrates that public licensing,
enforcement, and network-concentration data can be turned into a **qualitative
triage signal**. It does not, and cannot, demonstrate billing fraud, because the
billing data required for that (ProviderOne claims) is not public and is out of
scope for Phase 1 by design.

## Data Scope

Every number in this toolkit is computed from the repository's own public,
de-identified files:

- `anonymized_data/WA_AFH_3County_Enriched_ANON.csv`
- `anonymized_data/WA_Operator_Clusters_ANON.csv`
- `anonymized_data/WA_Operator_Clusters_Corroboration_ANON.csv`
- `wa_data_aggregate/WA_AFH_Growth_2013_2026.csv`

No facility name, address, license number, phone number, or other provider-identifying
field is read, computed, or displayed anywhere in this toolkit. All outputs are
counts, rates, and distributions aggregated at the cluster, county, or tier level.
See `README_ANONYMIZED_DATA.md` for what these source files do and do not contain.

## Qualitative Review-Priority Tiers

Phase 1 groups facilities into four qualitative tiers using the same public-data
indicators already defined in the manuscript's Appendix B (Network Concentration,
Enforcement Intensity, Complaint Load). A facility's tier is simply a count of how
many of these three public-data indicators are present — it is **not** a weighted
score, and no numeric point value is assigned to any facility.

| Indicator | Public-data trigger |
|---|---|
| Network Concentration | Facility belongs to a shared-contact operator cluster of 3 or more licenses |
| Enforcement Intensity | Facility has 2 or more formal enforcement actions on record |
| Complaint Load | Facility has 3 or more investigations on record |

**Network Concentration is a shared-contact proxy, not verified ownership.** A
cluster reflects two or more licenses sharing a public phone number; it is not
an assertion of common ownership or control, and it does not draw on any
beneficial-ownership data (which is not public). See `README_ANONYMIZED_DATA.md`
for the same caveat applied to the `cluster_id` field itself.

| Tier | Indicators present | Meaning |
|---|---|---|
| **Baseline Monitoring** | 0 | No public-data indicator triggered. Subject to routine licensing oversight only. |
| **Elevated Public-Data Review** | 1 | One public-data indicator triggered. Warrants a closer look at public records, nothing more. |
| **High Public-Data Review Priority** | 2 | Two public-data indicators triggered concurrently. Warrants prioritized administrative review. |
| **Claims Validation Candidate** | 3 | All three public-data indicators triggered concurrently. A candidate for Phase 2 claims-data cross-validation — not a fraud finding. |

Tier assignment is entirely rule-based and reproducible from the public data alone;
`scripts/build_phase1_dashboard_data.py` implements exactly the table above and
nothing more.

## Phase 1 Stops Before Claims Validation

Phase 1 ends at the "Claims Validation Candidate" tier. It does not, and cannot,
determine whether a candidate's billing is anomalous, because ProviderOne claims
data is internal to the state Health Care Authority and is not part of this
replication package. Moving a facility from "Claims Validation Candidate" to any
finding of billing irregularity is Phase 2 work, requires internal agency data,
and is explicitly out of scope here (see the manuscript, Section 7.2).

## Guardrails

- **Not a fraud score.** Tier assignment reflects public-data pattern concentration
  only, not a probability or determination of fraud.
- **Not a validated predictive model.** No tier or indicator threshold in this
  toolkit has been tested against claims outcomes or ground-truth fraud findings.
- **Not an enforcement determination.** No tier implies that any named or unnamed
  facility should be sanctioned, excluded, or referred for enforcement.
- **No facility is identified.** This toolkit works entirely in aggregate; it
  cannot and does not name, rank, or otherwise single out any individual provider.
- **Requires human review, claims validation, and due process** before any tier
  assignment is used to inform an actual audit, investigation, or enforcement
  decision. See the manuscript's Appendix B and Limitations (Section 9) for the
  same guardrails applied to the underlying PDRT concept.

## Interactive Sensitivity Dashboard

The dashboard (`dashboard/phase1-dashboard.html`) adds an **interactive sensitivity
analysis** layer on top of the fixed tier definitions above. It lets a reader adjust
the three indicator thresholds and toggle indicators on or off, and see the
aggregate tier and indicator-overlap counts update immediately in the browser.
This is a transparency feature, not a modeling upgrade — the underlying rule stays
exactly what it is: a count of how many public-data indicators are present.

A few things are true of every threshold setting the dashboard allows:

- **Threshold controls are illustrative only.** The allowed values
  (`dashboard/phase1_tier_config.json`) were chosen to bracket the manuscript's
  Appendix B defaults, not derived from any statistical validation.
- **Changing thresholds does not create a validated risk model.** Moving a
  slider changes which public-data pattern counts as "concentrated" or
  "frequent"; it does not add evidence, does not touch claims data, and does
  not make any tier assignment more or less true in a predictive sense.
- **Sensitivity analysis is not an operational recommendation.** Showing how
  tier counts shift under different thresholds is meant to help a reader
  understand the framework's mechanics and its sensitivity to arbitrary
  choices — it is not a suggestion that any particular threshold setting
  should be adopted operationally.
- **Any operational use would still require claims validation, human review,
  and due-process safeguards**, regardless of which thresholds are selected.
  The dashboard cannot and does not change this; every guardrail in this
  document applies identically at every threshold setting the dashboard
  offers.

The dashboard computes everything client-side from a precomputed aggregate
table (`sensitivity_cube` in `phase1_dashboard_data.json`) — a county-level
histogram of bucketed indicator values. No facility-level row is ever sent to
the browser; the aggregate table is sufficient to recompute tier and overlap
counts for any allowed threshold combination without exposing individual
facilities. See `dashboard/README.md` for how this is built and
`dashboard/PHASE1_RESULTS_BRIEF.md` for a plain-English walkthrough of what the
sensitivity results do and do not show.
