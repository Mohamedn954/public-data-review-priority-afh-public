import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import os
DEL = OUT_DIR + "/"

# Data Availability Matrix
with open(DEL+"WA_Data_Availability_Matrix.md","w") as f:
    f.write("""# Washington AFH/HCBS Data Availability Matrix

This matrix evaluates the public availability of key program-integrity data points required to operationalize the MN review-priority indicator typology in Washington State.

| Data Category | Publicly Available? | Source / Location | Notes & Limitations |
|---------------|---------------------|-------------------|---------------------|
| **Facility Roster & Capacity** | Yes | DSHS ArcGIS Portal (Residential Care) | Geocoded nightly extract. Requires deduplication to isolate current active licenses. |
| **Medicaid Contract Status** | Yes | DSHS AFH Locator | Contract types (e.g., AFH, Specialized Behavior Support) are published per facility. |
| **Inspection & Complaint Counts** | Yes (via scraping) | DSHS RCS Forms Portal | Public per facility (`AFHForms.aspx?lic=X`). Must be scraped to build structured datasets. |
| **Enforcement Actions (Fines/Conditions)** | Yes (via scraping) | DSHS RCS Forms Portal | Embedded in facility PDF folders ("enforcement letters"). Not published as a standalone structured dataset. |
| **Program Spending Growth** | Yes (aggregate) | OFM / DSHS Biennial Budget | High-level LTC spending is public: All-Funds rose from $3.8B (2013-15) to $10.44B enacted (2023-25) to $13.07B proposed (2025-27, +25.2%). See `wa_data_aggregate/WA_LTC_Spending_Biennia.csv` for the full sourced series. Per-provider or per-recipient payment data is not public. |
| **Provider Exclusions/Sanctions** | Yes | HCA Termination List / LEIE | Downloadable lists exist, but joining them to the AFH roster is unreliable because facility names rarely match the licensee's legal/personal name. |
| **Beneficial Ownership / Related Parties** | **No** | WA SOS CCFS (Partial) | CCFS is bot-gated and only shows registered agents/governors. Full 42 CFR 455.104 ownership disclosures are not public. |
| **Provider-Level Billing Data** | **No** | HCA ProviderOne | Claims data (units, dates, overlapping hours) is strictly internal. |
| **Oversight Audit Findings** | Yes | WA State Auditor (SAO) | High-quality PI performance audits (2021, 2023) are public. |

## Public Records Request (PRR) Target List
To fully test the MN review-priority indicator typology, the following datasets must be requested from DSHS/HCA:
1. **Master Licensee Legal Name Crosswalk:** Mapping every AFH facility name to its exact legal licensee name and UBI number (to enable exclusion-list matching).
2. **Provider Ownership Disclosures:** The full related-party and beneficial ownership data collected under 42 CFR 455.104.
3. **Provider-Level Medicaid Payments:** Annual Medicaid dollars paid per AFH operator (to test RF-03 billing concentration).
4. **Enforcement Dataset:** A structured tabular export of all civil fines, stop-placement orders, and license conditions (to avoid PDF scraping).
""")

# Testability Memo
with open(DEL+"WA_RedFlag_Testability_Memo.md","w") as f:
    f.write("""# Memo: Testability of the Minnesota Review-Priority Indicator Typology in Washington State

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
""")

# Bibliography
with open(DEL+"WA_Source_Bibliography.md","w") as f:
    f.write("""# Washington State Evidence Base: Source Bibliography

1. **WA DSHS Long Term Care - Residential Care Dataset**
   * Source: Washington State Geospatial Open Data Portal (ArcGIS Hub)
   * URL: `https://geo.wa.gov/search?q=adult%20family%20home`
   * Use: Section A facility master dataset.

2. **WA DSHS AFH Locator & Reports Portal**
   * Source: DSHS Aging and Long-Term Support Administration (ALTSA)
   * URL: `https://fortress.wa.gov/dshs/adsaapps/lookup/AFHAdvLookup.aspx`
   * Use: Section B inspection, investigation, and enforcement data.

3. **WA State Auditor (SAO) Medicaid Program Integrity Audits**
   * Source: Office of the Washington State Auditor
   * Files: 2021 HCA PI Audit, 2023 MCO PI Audit
   * Use: Section G oversight capacity and systemic findings.

4. **WA OFM/DSHS Long-Term Care Budget Summaries**
   * Source: Office of Financial Management (OFM)
   * URLs:
     - 2023-25 enacted baseline ($10.44B, originally-enacted): `https://ofm.wa.gov/budget/state-budget-2023-25/24-proposed-supplemental/agency-recommendation-summaries/300/050/`
     - 2025-27 proposed level ($13.07B policy level): `https://ofm.wa.gov/budget/state-budget-2025-27/proposed-biennial/agency-recommendation-summaries/300/050/`
   * Use: Section C program spending growth (+25.2% from the 2023-25 enacted baseline to the 2025-27 proposed level).

5. **WA HCA Provider Termination and Exclusion List**
   * Source: Washington State Health Care Authority
   * URL: `https://www.hca.wa.gov/billers-providers-partners/become-apple-health-provider/provider-termination-and-exclusion-list`
   * Use: Section F exclusion and sanction cross-checks.

6. **WA SOS Corporations and Charities Filing System (CCFS)**
   * Source: Washington Secretary of State
   * URL: `https://ccfs.sos.wa.gov/`
   * Use: Section E ownership and registered-agent sampling.
""")
print("docs built")
