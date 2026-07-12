# Memo: Testability of the Minnesota Review-Priority Indicator Typology in Washington State

**Author:** Mohamed Noor Hussein
**Subject:** Applying the MN HCBS/Residential Review-Priority Indicators to WA Adult Family Homes

This memo summarizes the results of applying the 20 review-priority indicators (RF-01 to RF-20), derived from Minnesota's public Medicaid enforcement record, to Washington State's Adult Family Home (AFH) and HCBS programs, focusing on King, Pierce, and Spokane counties.

## Executive Summary
The central finding is that **the billing-level indicators most directly tied to Minnesota's enforcement cases (impossible hours, out-of-state billing, max-unit billing) are entirely invisible in Washington public data.** They require internal HCA claims analytics that this project does not have access to.

Washington's public data *does* support testing of the **structural and network-level indicators** (concentration, related-party networks, oversight capacity). Using only public DSHS and SAO data, we mapped 3,457 AFHs, identified 72 multi-home operator clusters, and quantified enforcement intensity.

## Key Findings by Category

### 1. Network & Ownership Concentration (RF-03, RF-08)
Full beneficial ownership data is not public. We built a bounded proxy for related-party networks using shared phone numbers.
* **Finding:** 164 AFHs in the three counties share a phone number with at least one other license, forming **72 distinct operator clusters** (up to 4 homes per cluster).
* **Implication:** RF-08 can be partially approximated using public shared-contact data to flag operator-concentration patterns for further review. Shared contact information indicates shared administrative contact, not verified common ownership.

### 2. Oversight Capacity (RF-18, RF-20)
Washington's oversight posture shares process-level similarities with what Minnesota's auditors described before Minnesota's enforcement wave — this is a comparison of oversight *process*, not an empirical finding about Washington outcomes.
* **Finding:** WA State Auditor (SAO) performance audits in 2021 and 2023 found that the HCA Division of Program Integrity operated without a statewide fraud plan, lacked risk-based audit targeting, and relied on a reactive (complaint-driven) posture rather than systematic data analytics.
* **Implication:** RF-18 (chronic oversight-capacity constraints) is present in Washington's own audit record, independent of any comparison to Minnesota.

### 3. The Exclusion List Linkage Gap (RF-06, RF-15)
* **Finding:** Cross-matching the WA HCA Medicaid Provider Exclusion List against the 3,457 AFH facility names yielded **zero matches**.
* **Implication:** This is a data-linkage limitation, not evidence of clean operations or of any irregularity. Because the public AFH roster uses "Doing Business As" facility names rather than the licensee's legal name, public exclusion-list screening cannot be relied on as-is. A master legal-name crosswalk would be needed to make this check meaningful, and is a natural first records request.

### 4. Enforcement & Complaint Signals (RF-14, RF-18)
* **Finding:** Scraping DSHS RCS reports found 165 facilities in the three counties with recent enforcement actions (including 180 civil fines and 41 stop-placement orders), and 46 facilities with high complaint loads (≥3 investigations).
* **Implication:** This structured enforcement layer lets us describe where operator clusters and enforcement activity coincide. For example, one four-home cluster (King County) accounted for 3 enforcement actions and 3 civil fines. [City-level detail redacted for this public release to prevent re-identification of the underlying operator, consistent with the anonymization policy in README_ANONYMIZED_DATA.md.] Coincidence between a cluster and enforcement activity is a review-priority signal, not a finding of wrongdoing by any operator in the cluster.

## Conclusion & Recommendations
The Minnesota indicator typology transfers usefully to Washington, but its application splits cleanly along a public/internal boundary:
1. **Public data** can support DSHS shared-contact clustering and scraped enforcement counts to flag operator-concentration and oversight patterns that may warrant closer administrative review.
2. **Internal claims data**, accessed by an authorized state or federal body, would be required before any billing-anomaly or enforcement conclusion could be considered — public data alone cannot support that step.
