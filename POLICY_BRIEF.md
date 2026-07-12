# Public Records, Not Predictions: A Review-Priority Layer for Medicaid Residential Care Oversight

*A policy brief accompanying "A Public-Data Review-Priority Framework for Medicaid
Residential Care Oversight: Evidence from Washington State Adult Family Homes"
(Mohamed Noor Hussein, 2026)*

## Why this matters now

Medicaid's home- and community-based services (HCBS) sector has grown quickly across
most states, and Washington is no exception: licensed Adult Family Homes (AFHs) grew
from roughly 2,800 in 2018 to over 6,000 by 2026, alongside a long-term-care budget
that grew from $3.8 billion (2013-15) to $10.44 billion enacted (2023-25). Growth of
this kind expands access to care outside institutional settings, which is broadly the
right direction for long-term-care policy. It also expands the number of small,
dispersed providers that state program-integrity offices have to watch, at a moment
when those offices report — in their own audits — that they still rely mainly on
complaints rather than systematic data review.

Minnesota's 2024–2026 Medicaid enforcement wave is the reason this question is urgent
rather than theoretical. Minnesota's own legislative auditor warned, years before that
wave, that HCBS oversight relied on complaints rather than proactive financial review.
The warning was not acted on in time. This project asks a narrower, answerable
question: using only *public* records, what could a state see about its own AFH sector
before a comparable enforcement gap becomes urgent — and, just as importantly, what
could it not see?

## Core message

Public licensing, enforcement, and complaint records can support a **review-priority
layer**: a way of using existing public data to flag which providers might warrant a
closer look by staff who already have that authority. Public records cannot support
fraud detection on their own, because they do not include claims data — the billing
detail that Minnesota's actual cases were ultimately built on. Confusing the two is the
central mistake this brief is written to help state and federal readers avoid.

## What public data can show

Using only Washington's own public sources — the DSHS facility roster, the DSHS public
reports portal, State Auditor performance audits, and public corporate-registry
records — this project's pilot of 3,457 AFHs in three counties (King, Pierce, Spokane)
was able to:

- **Map operator concentration.** 72 multi-home clusters (164 facilities) sharing a
  public contact number, a bounded proxy for common management — corroborated by an
  independent public-record cross-check for 70 of the 72 clusters.
- **Quantify enforcement and complaint intensity.** 165 facilities with at least one
  enforcement action; 586 with at least one investigation, over a roughly four-year
  public-record window.
- **Locate a genuine oversight gap.** Cross-matching the state's own Medicaid
  provider-exclusion list against the facility roster returned zero matches — not
  because the roster is clean, but because public facility names rarely match a
  licensee's legal name, which makes exclusion screening as currently structured
  unreliable on public data alone.
- **Describe, not diagnose, an oversight-process parallel.** Washington's own State
  Auditor has described HCA's program-integrity division as relying on complaints
  rather than systematic analytics — the same process gap Minnesota's auditor
  described before Minnesota's enforcement wave. This is a similarity in process,
  observed independently in each state's own audit findings, not a finding that
  Washington has experienced or will experience Minnesota's outcome.

## What public data cannot show

- **Billing-level fraud indicators** — impossible-hours billing, overlapping-location
  billing, billing for deceased recipients — are invisible in public records because
  they require claims data (Washington's ProviderOne system), which is not public.
- **Verified common ownership.** Shared-contact clustering identifies facilities that
  plausibly share management; it is not a legal ownership finding, and it does not by
  itself justify any adverse action against a facility.
- **Any conclusion about a specific facility or operator.** Nothing in this project
  identifies, ranks, or names a Washington provider, and nothing here should be read
  as evidence that any Washington provider has committed fraud.

## Washington AFH pilot, in brief

The pilot deliberately covers three counties (King, Pierce, Spokane) rather than the
full state, to keep the enforcement-record scrape tractable and auditable. Every
number above is reproducible from the public replication package
(`anonymized_data/`, verified by `scripts/verify_headline_numbers.py`), and every
indicator is documented against a 20-item typology adapted from Minnesota's public
enforcement record, with an explicit public-data-testability rating for each item
(`WA_RedFlag_Testability_Matrix_v2.csv`).

## A two-phase oversight model

**Phase 1 — Public-data review priority (this project).** Aggregate, de-identified,
rule-based grouping of facilities into qualitative tiers (Baseline Monitoring,
Elevated Public-Data Review, High Public-Data Review Priority, Claims Validation
Candidate) using only public licensing, enforcement, and network signals. No facility
is scored, ranked, or named. This phase is complete and reproducible in this
repository (`dashboard/`, `PHASE1_PUBLIC_DATA_FRAMEWORK.md`).

**Phase 2 — Claims-informed validation (not performed here).** Before any tier could
inform an actual audit or enforcement decision, an authorized state or federal body
would need to check the public-data signal against internal claims data (billing
patterns, units of service, provider revalidation history), under a proper data-use
agreement, with human review and due-process protections at every step. This project
has no claims-data access and does not perform this phase. It describes what that
phase would require, not what it found.

## Recommendations for state and federal actors

1. **Treat a public-data review-priority layer as a triage input, not a determination.**
   It can help direct limited audit staff time toward records worth a closer look; it
   cannot substitute for the claims review, human judgment, and due process that any
   adverse action requires.
2. **Invest in the specific data linkage this project found missing**: a licensee
   legal-name-to-facility crosswalk, so exclusion-list screening actually works, and a
   structured (not PDF-locked) export of enforcement and complaint records.
3. **Pair, rather than choose between, public-data and claims-based oversight.** The
   public layer is inexpensive and immediately buildable from records the state
   already publishes; the claims layer is the only one that can confirm or rule out an
   actual billing problem. Neither replaces the other.
4. **Expect this typology to need re-tuning per state.** A 20-indicator typology built
   from Minnesota's enforcement record transfers usefully as a checklist, but which
   items are public-data-testable depends on each state's own licensing, reporting,
   and corporate-registry structure (see "Portability" in the manuscript, Section 8).
   A preliminary two-county companion test in Oregon (`public-data-review-priority-oregon-public`,
   a separate companion repository) confirms this directly: county-level density and
   enforcement-rate indicators
   transferred to a second state without any recalibration, while the shared-contact
   network proxy required facility-type-aware threshold adjustment before it produced
   a usable signal.

## Guardrails

This project is a review-priority framework rather than a fraud score, a validated
predictive model, or an enforcement determination. No Washington facility or
operator is identified,
ranked, or alleged to have committed fraud. Public signals are intended to clarify
what may warrant closer administrative review and what remains unknowable without
internal claims access, human judgment, and due-process safeguards. Named Minnesota
enforcement cases are drawn from public DOJ and court records; charges are allegations
unless a conviction is noted. Full guardrail statement: `GUARDRAILS.md`.
