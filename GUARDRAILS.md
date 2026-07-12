# Guardrails — What This Research Is and Is Not

This document consolidates, in one place, the use-scope and evidentiary
guardrails that apply to every artifact in this repository (the manuscript,
the anonymized data, the scripts, the Phase 1 dashboard, and any derived
figures). It exists so that anyone linking to a single file from this
repository still lands on the intended framing.

The guardrail statements below are already reproduced across `README.md`,
`README_ANONYMIZED_DATA.md`, `PHASE1_PUBLIC_DATA_FRAMEWORK.md`,
`dashboard/README.md`, `dashboard/PHASE1_RESULTS_BRIEF.md`, `LICENSE`, and
`CITATION.cff`. This file gathers them for citation convenience; the
authoritative wording in each context is in the primary document.

The Oregon replication study is a separate companion study, not part of the manuscript,
and now lives in its own dedicated public repository,
[`public-data-review-priority-oregon-public`](https://github.com/Mohamedn954/public-data-review-priority-oregon-public),
rather than as a subfolder of this repo. It carries its own equivalent guardrail language
in that repository's `README.md` and its two reports; no facility or operator is named,
it is a methods-transfer test rather than a fraud-detection exercise, and it ships only
de-identified `anonymized_data/`. The same seven guardrails below apply to it in substance;
it is not separately re-numbered here to avoid two competing "canonical" lists.

---

## The seven guardrails

**1. Not a fraud score.** Tier assignment in the Phase 1 toolkit reflects
public-data pattern concentration only. It is not a probability, a rating,
or a determination of fraud, waste, abuse, or any other adverse outcome.

**2. Not a validated predictive model.** No tier, no threshold, and no
indicator in this repository has been tested against claims outcomes or
ground-truth fraud findings. All thresholds are illustrative and
non-validated.

**3. Not an enforcement determination.** No tier implies that any named or
unnamed facility should be sanctioned, excluded, terminated, or referred
for enforcement action of any kind.

**4. No facility is identified, ranked, or singled out.** The public data
package works entirely in aggregate. Facility identifiers are stable
non-identifying tokens (`F#####`); operator clusters are stable
non-identifying tokens (`OP###`) that encode shared-contact membership only
and are not an assertion of verified common ownership. The Phase 1
dashboard exposes no facility-level rows at any threshold setting.

**5. All indicators are review-priority signals only.** They are intended
to help a human reviewer prioritize where a closer look at public records
might be worth the time. They are not findings of wrongdoing, and no
Washington facility or operator in this package is alleged to have
committed fraud.

**6. Requires human review, claims validation, and due process before any
operational use.** Any operational application would require internal
ProviderOne claims data, human judgment, and established enforcement
procedures with due-process safeguards. Phase 1 stops before claims
validation, by design; Phase 2 (claims-data cross-check) is agency-side
work and is explicitly out of scope for this repository.

**7. Named Minnesota cases are public DOJ/court-record allegations.** The
enforcement cases in `mn_data/MN_Medicaid_Fraud_Cases_Dataset.csv` are
drawn from public sources. Charges are allegations unless a conviction is
noted; defendants are presumed innocent.

---

## What this repository IS

* A **journal-safe replication package** for a working paper applying a
  20-indicator public-data review-priority typology (derived from the
  Minnesota Medicaid enforcement record) to Washington State's Adult
  Family Home sector.
* A **de-identified aggregate dataset** that reproduces every headline
  number the manuscript reports.
* A **transparent evidence layer** documenting what public data can and
  cannot support in a program-integrity review-priority context.
* A **static, offline, aggregate-only demonstration dashboard** showing
  what the Phase 1 review-priority layer would look like in practice.

## What this repository IS NOT

* Not a fraud-detection product.
* Not a facility- or operator-ranking system.
* Not a risk-scoring service.
* Not a re-runnable copy of the raw data-acquisition pipeline (the public
  package intentionally ships only de-identified final outputs; the raw,
  pre-anonymization pipeline lives in the private companion repository).
* Not a substitute for internal Medicaid Program Integrity work.

---

## Where the canonical wording lives

If you need to cite any specific guardrail statement, the authoritative
document for each is:

| Guardrail concept          | Canonical source                                          |
| -------------------------- | --------------------------------------------------------- |
| Anonymization scope        | `README_ANONYMIZED_DATA.md`                               |
| Tier definitions & scope   | `PHASE1_PUBLIC_DATA_FRAMEWORK.md`                         |
| Dashboard privacy design   | `dashboard/README.md`                                     |
| Plain-English tier reading | `dashboard/PHASE1_RESULTS_BRIEF.md`                       |
| Reproducibility scope      | `scripts/REPRODUCIBILITY_CHECK.md`                        |
| Testability of each RF     | `WA_RedFlag_Testability_Matrix_v2.csv`                    |
| Oregon companion-study scope and guardrails | `public-data-review-priority-oregon-public` repo's `README.md` |
| Licensing terms            | `LICENSE`                                                 |
| Preferred citation format  | `CITATION.cff`                                            |

## Contact

For questions about scope, reuse, or citation, see `CITATION.cff` for
author information.
