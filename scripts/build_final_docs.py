#!/usr/bin/env python3
import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import os
DEL = OUT_DIR + "/"

# 1. Comparison Matrix
comp_md = """# Washington vs. Minnesota: Structural Comparison Matrix
*Evidence Base Extraction: Section G*

> **Status note:** This is a supporting evidence-base memo from the project's early exploratory phase. Its framing predates the guardrail language later consolidated in `GUARDRAILS.md` and the manuscript, and an earlier draft of this table used stronger language than the evidence supports (see revision note below). It is retained for transparency and provenance. `GUARDRAILS.md` and the manuscript are canonical for framing; where this memo and those documents differ, the canonical documents control.

This matrix compares structural features of Washington's Adult Family Home (AFH) and HCBS programs against the oversight vulnerabilities documented in Minnesota's public Medicaid enforcement record. The comparison is structural, not evidentiary: it does not assert that any Washington facility or operator has engaged in the conduct described in Minnesota's enforcement cases. No fraud is alleged against any Washington provider anywhere in this document.

| Structural Domain | Minnesota (HSS / HCBS / PCA) | Washington (AFH / HCBS) | Structural Comparison |
|----------------------|------------------------------|-------------------------|-----------------------------|
| **Entry Barriers** | **Very low**, per Minnesota audit findings. Housing Stabilization Services allowed billing shortly after basic registration, with minimal physical-site verification. | **Comparatively high.** AFHs require physical property, fire/health inspections, zoning approval, and DSHS licensing before Medicaid contracting. | Washington's licensing model does not share Minnesota's low-barrier registration structure. This is a genuine structural difference, not a review-priority signal. |
| **Provider Growth** | **Rapid**, per Minnesota audit findings. HSS billing grew from roughly $2.6M to $104M within three years; EIDBI from roughly $600K to over $400M. | **Rising since 2018.** The licensed AFH count was roughly flat for a decade near 2,800, then grew to roughly 6,075 by 2026; the state LTC budget has grown alongside it (see `wa_data_aggregate/WA_LTC_Spending_Biennia.csv`). | Both programs show periods of rapid provider or spending growth. Growth alone is not a review-priority indicator; it is the context in which oversight capacity should be assessed. |
| **Network Visibility** | **Limited**, per Minnesota audit findings. Investigators described shared registered agents, P.O. boxes, and family networks obscuring common ownership. | **Limited.** Washington's public corporate registry (SOS CCFS) does not expose full beneficial ownership, and the public AFH roster does not include related-party data. A bounded proxy (shared phone numbers) identifies 72 multi-home clusters in the three pilot counties; this proxy indicates shared contact information, not verified common ownership. | Both states' public records leave related-party ownership only partially visible. This is a data-availability gap common to public licensing systems, not a finding specific to Washington operators. |
| **Oversight Analytics** | **Complaint-driven**, per the Minnesota Office of the Legislative Auditor, which found DHS relied on complaints rather than systematic claims analytics. | **Complaint-driven**, per the Washington State Auditor's 2021 performance audit, which found HCA's Division of Program Integrity relied on complaints and lacked systematic risk-based analytics. | Both oversight bodies' own auditors describe a similar reliance on reactive, complaint-driven review rather than routine claims analytics. This is a documented similarity in oversight *process*, drawn from each state's own audit findings — not a claim that Washington has experienced, or is at risk of, the same outcome as Minnesota. |
| **Billing Controls** | **Weak**, per DOJ and state enforcement filings describing billing for deceased clients, overlapping-hours billing, and out-of-state billing. | **Not publicly observable.** ProviderOne claims data is not public, so Washington's billing controls cannot be assessed from public records at all. | This is the central data gap this project documents: public records can describe licensing, enforcement, and complaint activity, but cannot show whether Washington's billing controls resemble Minnesota's. Closing this gap requires claims-informed validation with appropriate authorization, not public-data inference. |

**Summary.** Washington's AFH licensing model differs structurally from Minnesota's Housing Stabilization Services in ways that plausibly reduce exposure to the specific low-barrier registration pattern documented in Minnesota. Separately, each state's own oversight auditors have described a similar reliance on complaint-driven review rather than systematic analytics — a structural similarity in process, not an empirical finding about outcomes. Public records cannot determine whether Washington's claims-level billing controls resemble Minnesota's, because Washington's claims data is not public. That question can only be answered through claims-informed review conducted by state or federal authorities with appropriate access, and any such review would be subject to ordinary standards of evidence and due process before any conclusion about a specific provider is reached.
"""
with open(DEL+"WA_MN_Comparison_Matrix.md","w") as f: f.write(comp_md)

# 2. Public-Data Review-Priority Tier Proposal (ARCHIVED, never adopted)
# NOTE: This memo is intentionally archived with a prominent warning banner
# rather than presented as an active deliverable. A numeric 0-100 rubric is
# easy to misread, out of context, as an actual risk score assigned to a real
# facility. It was never statistically validated, never applied to any real
# facility, and is not used anywhere in the manuscript, the anonymized
# dataset, or the pipeline scripts. If this script is re-run, place the
# output in wa_docs/archive/, not wa_docs/, to preserve that separation.
score_md = """# [ARCHIVED — NOT FOR OPERATIONAL USE] Proposed Public-Data Review-Priority Tier Framework

*Evidence Base Extraction: Section H*

---

**ARCHIVED DOCUMENT. DO NOT USE THIS RUBRIC TO SCORE, RANK, OR FLAG ANY REAL FACILITY OR OPERATOR.**

This memo is retained only for provenance, to document an early, exploratory idea from the project's evidence-base phase. It has been superseded and is not part of the project's canonical framing.

- **It is not a validated instrument.** The point weights below (20, 10, etc.) were never statistically calibrated, tested for false-positive rates, or reviewed against ground truth. They are illustrative placeholders, not measured coefficients.
- **It is not a fraud score.** No numeric total produced by this rubric indicates that fraud, abuse, or any wrongdoing has occurred or is likely.
- **It is not used anywhere in the manuscript, the anonymized dataset, or the pipeline scripts.** The publication-facing version of this idea is the qualitative PDRT description in the manuscript's Appendix B, which deliberately avoids assigning a single composite numeric score to any facility, precisely because a single number invites exactly the misreading this archived draft risked.
- **Do not extract, screenshot, or cite the scoring table below out of this context.** Out of context, a "60-point" or "30-point" example below could be misread as an actual risk score assigned to a real facility. It is not; the examples are hypothetical illustrations of how the point categories would combine, not a real facility's computed score.

If you are looking for the current, canonical framing of review-priority indicators, see:
- `Hussein_Manuscript.docx` / `.pdf` (Appendix B, qualitative PDRT framing)
- `GUARDRAILS.md` (repository root)
- `wa_docs/README.md` (this folder's canonical-vs-superseded index)

---

## Original memo (superseded, preserved for provenance only)

Because billing data (claims) is not public, a public-data review-priority approach must rely on licensing, concentration, and complaint signals rather than claims analytics. Based on the Minnesota review-priority indicators (RF-01 to RF-20), an early draft of this project proposed a **Public-Data Review-Priority Tier system, derived from a 0-100 point rubric,** for WA AFHs, computable entirely from the datasets generated in this pilot. This rubric was never adopted; it is shown below only to document how the idea was originally framed before being replaced with the qualitative approach in the manuscript's Appendix B.

### Scoring Components (100 Points Total) — illustrative only, never adopted

**1. Network & Concentration Signal (40 Points)**
*Proxy for RF-08 (Related-Party Networks) and RF-03 (Concentration)*
- **Shared Phone Cluster (20 pts):** Facility shares a public phone number with ≥2 other licenses.
- **Rapid Network Expansion (20 pts):** Operator cluster added ≥2 new licenses within a 12-month period.

**2. Enforcement & Complaint History (40 Points)**
*Proxy for RF-14 (Documentation) and RF-18 (Oversight Signals)*
- **Stop-Placement Order (20 pts):** Active or recent DSHS stop-placement (severe life/safety or compliance failure).
- **Repeat Enforcement (10 pts):** ≥2 enforcement letters in the 2023-2026 window.
- **High Complaint Load (10 pts):** ≥3 complaint investigations in the 2023-2026 window.

**3. Geographic Density Signal (20 Points)**
*Proxy for RF-01 (Rapid Growth)*
- **High-Density County (10 pts):** Facility located in a county exceeding 7.0 AFHs per 1,000 seniors (e.g., Snohomish, Pierce).
- **Out-of-State Operator (10 pts):** Licensee mailing address or SOS CCFS governor address is outside Washington (requires CCFS sampling).

### Hypothetical illustration only — no real facility was scored

- **Hypothetical "high review priority" combination (60+ pts):** a facility in a 4-home phone cluster (20) in a high-density county (10), with a stop-placement (20) and high complaints (10), would sum to 60 points under this never-adopted rubric.
- **Hypothetical "moderate review priority" combination (30-50 pts):** a facility in a 2-home cluster (20) with repeat enforcement (10) would sum to 30 points.
- **Hypothetical "baseline" combination (0-20 pts):** a single-home operator with a clean inspection record would sum to 0 points.

*This point rubric was never applied to any real facility in the pilot dataset. It does not allege fraud, and it is not recommended for operational use under any circumstances without claims-data validation, statistical calibration, human review, and due-process protections that were never built for it.*
"""
with open(DEL+"WA_Public_Data_Review_Priority_Tier.md","w") as f: f.write(score_md)

# 3. Updated Data Availability Matrix
avail_md = """# Washington Data Availability Matrix (Updated)
*Evidence Base Extraction: Section I*

This matrix categorizes the data required to test the 20 review-priority indicators (RF-01–RF-20) in Washington State, explicitly separating what was successfully extracted from public sources vs. what requires a Public Records Request (PRR) or internal access.

| Data Category | Availability | Source / Notes |
|---------------|--------------|----------------|
| **Current AFH Roster & Capacity** | **Public** | DSHS ArcGIS Feature Service (extracted). |
| **AFH Growth Trends (2013-2026)** | **Public (Partial)** | DSHS ALTSA / Mancuso presentations. Annual counts reconstructed; new/closed churn requires PRR. |
| **LTC Budget / Spending Growth** | **Public** | OFM / DSHS Biennial Budgets: $3.8B (2013-15) to $10.44B enacted (2023-25) to $13.07B proposed (2025-27, +25.2%). See `wa_data_aggregate/WA_LTC_Spending_Biennia.csv`. |
| **Enforcement/Complaint Counts (2023-2026)** | **Public** | DSHS RCS Reports Portal (scraped for 3 counties). |
| **Enforcement/Complaint Counts (2020-2022)** | **Requires PRR** | Public portal retains only a rolling ~3-4 year window. |
| **Deficiency Categories (Abuse, Staffing)** | **Requires PRR** | Locked inside unstructured PDFs in the public portal. |
| **Operator Networks (Shared Phone Proxy)** | **Public** | Computed from DSHS roster (72 clusters found). |
| **Beneficial Ownership (42 CFR 455.104)** | **Requires PRR** | True corporate ownership / related-party mapping is not public. |
| **Provider Exclusion Lists** | **Public** | HCA Termination List / LEIE. (Note: joining to facility names yields false positives; requires PRR for licensee legal names). |
| **Medicaid Claims / Billing Data** | **Strictly Internal** | ProviderOne data (hours, max-units, deceased billing) is exempt from public disclosure (HIPAA/PHI). |

### Recommended Public Records Requests (PRR)
To extend this pilot toward a more complete public-data review-priority system, the following specific requests should be made to DSHS/HCA:
1. **DSHS RCS:** A structured database export of all AFH enforcement actions and complaint investigations (2018-2026), including deficiency category codes (WAC citations).
2. **DSHS ALTSA:** A roster of all newly issued and revoked AFH licenses per year (2018-2026) to track operator churn.
3. **HCA:** The 42 CFR 455.104 beneficial ownership disclosure dataset for all Medicaid-contracted AFHs.
"""
with open(DEL+"WA_Data_Availability_Matrix_Updated.md","w") as f: f.write(avail_md)

# 4. Expanded Bibliography
bib_md = """# Washington Evidence Base: Expanded Bibliography
*Evidence Base Extraction: Section F*

1. **DSHS ALTSA Payment Methodology Analysis** (BERK Consulting, Feb 2018). *Source for 2009-2018 AFH growth and Medicaid-contract trends.* URL: [dshs.wa.gov](https://www.dshs.wa.gov/sites/default/files/ALTSA/msd/documents/WA%20Adult%20Family%20Homes%20Payment%20Methodology%20Analysis%20-%202.23.2018.docx)
2. **DSHS RDA / Mancuso Demographic Trends Presentations** (2023, 2024). *Source for 2022-2024 AFH counts.* URL: [waseniorlobby.org](https://waseniorlobby.org/wp-content/uploads/MANCUSO-DSHS-Research-and-Data-Analysis.pdf)
3. **DSHS ArcGIS Residential Care Feature Service** (Accessed June 2026). *Source for current 6,075 facility roster.* URL: [geo.wa.gov](https://geo.wa.gov/search?q=adult%20family%20home)
4. **DSHS RCS AFH Reports Portal** (Accessed June 2026). *Source for 2023-2026 enforcement and complaint counts.* URL: [fortress.wa.gov](https://fortress.wa.gov/dshs/adsaapps/lookup/AFHAdvLookup.aspx)
5. **WA State Auditor's Office: HCA Division of Program Integrity** (Report 1028164, April 2021). *Source for RF-16/RF-18 systemic oversight findings.*
6. **WA State Auditor's Office: Medicaid Managed Care Program Integrity** (2023).
7. **HHS-OIG / WA SAO Concurrent Enrollment Audit** (2025).
8. **WA OFM 2025-27 Proposed Biennial Budget** (DSHS Long-Term Care). *Source for $13.07B spending figure.*
9. **U.S. Census Bureau ACS 5-Year Estimates** (2023). *Source for county 65+ population denominators.*
10. **WA HCA Medicaid Provider Termination and Exclusion List** (Updated June 2026).
"""
with open(DEL+"WA_Expanded_Bibliography.md","w") as f: f.write(bib_md)
print("Final docs written.")
