# Phase 1 Results Brief

*A plain-English summary of what the Phase 1 dashboard shows and does not show.
See `PHASE1_PUBLIC_DATA_FRAMEWORK.md` for the full technical definitions and
guardrails; this page is the one-paragraph-per-question version.*

## What does Phase 1 demonstrate?

Phase 1 demonstrates that Washington's public licensing, enforcement, and
network-concentration data — the kind of information anyone can pull from a
state website — can be turned into a reproducible, rule-based triage signal
without touching any private or internal data. It shows the *mechanics* of a
public-data review-priority layer working end to end: read public data in,
apply a transparent rule, get a qualitative tier out. It does not demonstrate
that any facility has committed fraud, because the data available to Phase 1
cannot show that.

## What does the dashboard show?

The dashboard shows, for the 3,457 facilities in the King/Pierce/Spokane pilot,
how many fall into each of four qualitative tiers (Baseline Monitoring,
Elevated Public-Data Review, High Public-Data Review Priority, Claims
Validation Candidate) under a given set of indicator thresholds, and lets a
reader move those thresholds within a bounded, pre-approved range to see how
sensitive the tier counts are to that choice. Every number on the dashboard is
an aggregate count — no facility is ever named, listed, or ranked.

## Why might "Claims Validation Candidate" show zero or very few facilities?

Under the manuscript's default thresholds, zero facilities in the pilot
trigger all three public-data indicators at once. This is an expected,
honest result, not a bug: it means that in this three-county snapshot, no
facility simultaneously sits in a large shared-contact cluster, carries
multiple formal enforcement actions, *and* has a high investigation count.
Requiring all three indicators together is a deliberately conservative bar —
that is the point of a cautious Phase 1 design. A low or zero count at the
top tier reflects the rarity of concentrated public-data patterns in this
snapshot, not a failure of the tool, and it should not be read as evidence
that no oversight concerns exist — only that this specific, narrow combination
of public signals is uncommon here.

## Why do public-data signals still matter if few or no facilities reach the top tier?

Because the value of Phase 1 is triage, not verdicts. Even a handful of
facilities reaching "Elevated" or "High" review priority tells an oversight
body where a closer look at public records might be worth the time, without
requiring claims data or an investigation to start. Public-data signals are
useful precisely because they are cheap to compute and available today — they
narrow attention, they do not replace judgment, and the manuscript is explicit
that they are not a substitute for claims-level verification.

## What would Phase 2 require?

Phase 2 would require internal ProviderOne claims data — billing hours,
units, dates of service — cross-referenced against the same operator
clusters and enforcement patterns Phase 1 identifies. That data is not
public, is not included in this replication package, and is not something
this toolkit can access or approximate. Phase 2 is agency-side work by
design; Phase 1 stops at the point where a human reviewer, not an algorithm,
would decide whether a claims-data cross-check is warranted.

## Key limitations and guardrails

- Functions only as a review-priority signal — never a fraud score, a
  validated predictive model, or an enforcement determination.
- No facility is identified, ranked, or singled out anywhere in the dashboard.
- All thresholds are illustrative and non-validated; changing them changes
  which pattern counts as notable, not the underlying evidence.
- Three-county pilot only (King, Pierce, Spokane); not a statewide or
  nationwide claim.
- Requires human review, claims validation, and due process before any
  operational use — at every threshold setting the dashboard offers.
