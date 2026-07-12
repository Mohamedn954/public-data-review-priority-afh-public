# Release Overview

## Canonical citation

> Hussein, M. N. (2026). *A Public-Data Review-Priority Framework for Medicaid
> Residential Care Oversight: Evidence from Washington State Adult Family Homes*
> [Data set and replication package]. Version 1.0.
> https://github.com/Mohamedn954/public-data-review-priority-afh-public

Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff) at the repo
root; GitHub's "Cite this repository" widget reads that file directly.

## Contents of this release

- A de-identified, journal-safe replication dataset (`anonymized_data/`, `wa_data_aggregate/`)
- The Minnesota public-enforcement-record evidence base used to derive the indicator
  typology (`mn_data/`, `mn_docs/`)
- Portable, path-agnostic analysis scripts (`scripts/`) with a stated reproducibility
  scope (`scripts/REPRODUCIBILITY_CHECK.md`, `PROVENANCE_MAP.md`)
- A static, offline Phase 1 public-data review-priority dashboard (`dashboard/`)
- Guardrail, provenance, and reference documentation: `GUARDRAILS.md`, `CODEBOOK.md`,
  `PROVENANCE_MAP.md`, `POLICY_BRIEF.md`, `data_guide/`
- A standalone Oregon replication study, testing whether this project's pipeline
  transfers to a second state; a companion to, not part of, the manuscript, and now
  published in its own repository,
  [`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public),
  rather than as a subfolder here. The manuscript is hosted on SSRN
  (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7070198) rather than duplicated
  as a file in this repository; the Oregon paper will be posted separately. This repo
  is the data/scripts/dashboard layer that lets a reader independently verify what
  the manuscript reports.

## Validation status

- **Internal consistency:** `verify_headline_numbers.py` confirms every headline
  number in the manuscript reproduces from `anonymized_data/`.
- **Dashboard aggregate-only guarantee:** `validate_phase1_toolkit.py` confirms the
  Phase 1 dashboard exposes no facility-level row, no raw identifying column name, and
  no prohibited term, at any threshold setting.
- **Oregon replication study:** now a separate repository
  ([`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public)),
  where its own `verify_oregon_numbers.py` confirms the headline numbers reported in
  the Oregon paper reproduce from `anonymized_data/` alone, and that no raw facility
  identifier leaks into it. This is a companion methods-transfer study, not a
  manuscript output, and carries the same "not externally validated" status as the
  rest of this release.
- **External validation:** none. This release has **not** been peer-reviewed, has
  **not** been validated against Washington HCA/DSHS claims data, and has **not** been
  reviewed or endorsed by any Washington state agency, Minnesota state agency, or
  federal body. It is an independent research replication package.
- **Not validated:** the Phase 1 review-priority tiers and the exploratory 0–100
  point rubric archived at `wa_docs/archive/WA_Public_Data_Review_Priority_Tier.md`
  (never adopted; see its archived-document warning banner) are illustrative
  only. No tier or score in this repository has been checked against claims outcomes
  or confirmed fraud/waste/abuse findings.

## Guardrails and intended use

This project is a review-priority framework. It does not operate as a fraud score,
a validated predictive model, or an enforcement determination. No Washington facility
or operator is identified, ranked, or alleged to have committed fraud. Public signals
are intended to clarify what may warrant closer administrative review and what
remains unknowable without internal claims access, human judgment, and due-process
safeguards. Full statement: [`GUARDRAILS.md`](GUARDRAILS.md).

**Intended use:** academic research, methods replication, and as a discussion input
for state or federal program-integrity offices considering a public-data review-priority
layer. **Not intended use:** as a standalone tool for auditing, sanctioning, excluding,
or making any adverse determination about a specific facility or operator; as a
validated risk score; or as a substitute for claims-informed program-integrity review.

## Relationship to the private companion repository

A private companion repository holds the non-anonymized, facility-level Washington
and Oregon data (license numbers, facility names, street addresses, phone numbers)
used to produce this public package, along with the full manuscript and standalone
paper files. This public repository is the transparent, de-identified evidence layer
intended for external review and replication; it deliberately does not ship raw
pipeline intermediate files or facility-level identifiers. See `README.md` ("What's
excluded from this public package") and `scripts/REPRODUCIBILITY_CHECK.md` for the
exact boundary between what each repository can reproduce.

## Archival location / DOI

- **DOI:** not yet minted. *(Recommended next step: archive a tagged release on
  Zenodo or OSF and mint a DOI, then update this section and `CITATION.cff`
  accordingly.)*
- **Archival copy:** not yet deposited in a long-term archive independent of GitHub.
  *(Recommended: Zenodo's GitHub integration, which archives a snapshot of each
  tagged release automatically once connected.)*
- **Current authoritative location:** the `main` branch, tagged `v1`, at
  https://github.com/Mohamedn954/public-data-review-priority-afh-public. A DOI-backed
  archive (e.g., Zenodo) is a stronger permanent-record citation than a git tag or a
  GitHub URL alone, and is the recommended next step before citing this release as
  external evidence.
