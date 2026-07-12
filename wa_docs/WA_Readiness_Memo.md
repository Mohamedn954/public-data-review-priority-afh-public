# Washington State AFH/HCBS Review-Priority Pilot: Readiness Memo
*Evidence Base Extraction: Section J*

> **Status note:** This is a supporting evidence-base memo from the project's early exploratory phase. Its framing predates the guardrail language later consolidated in `GUARDRAILS.md` and the manuscript. It is retained for transparency and provenance. `GUARDRAILS.md` and the manuscript are canonical for framing; where this memo and those documents differ, the canonical documents control.

## Executive Summary
This pilot applied a review-priority indicator typology, adapted from Minnesota's public Medicaid enforcement record, to Washington State's public Adult Family Home (AFH) and HCBS data. The pilot shows that a public-data review-priority layer is feasible in Washington: public records can surface network-concentration and enforcement signals, but cannot observe claims-level billing activity, which is the layer at which Minnesota's enforcement cases were ultimately built.

Washington's AFH licensing model differs structurally from Minnesota's Housing Stabilization Services at the point of entry — AFHs require physical property and inspections before Medicaid contracting, which is not true of the low-barrier registration model documented in Minnesota's HSS program. Separately, Washington's own state auditor has described oversight processes that rely on complaints rather than systematic analytics, a pattern also described by Minnesota's legislative auditor. This is a structural similarity in oversight *process*, observed independently in each state's own audit findings — not a finding that Washington has the same outcome, and not an allegation against any Washington provider.

## Key Pilot Findings

1. **The Post-2018 Growth Pattern (RF-01/02):** After roughly a decade of flat capacity (~2,800 homes through 2018), Washington's AFH sector grew to over 6,000 licensed homes by 2026. This growth pattern is structurally comparable to Minnesota's rapid program expansion in the sense that both created conditions under which oversight capacity is tested; it is not, by itself, evidence of any oversight failure in Washington.
2. **Network Concentration (RF-08):** Beneficial ownership data is not public, but the pilot identified **72 multi-license operator clusters** (up to 4 homes sharing a public phone number) in King, Pierce, and Spokane counties, using a bounded shared-contact proxy that indicates common contact information, not verified common ownership.
3. **Normalized Geographic Density (RF-03):** Normalizing supply against the Census 65+ population shows that Snohomish (8.69 homes/1,000 seniors) and Pierce (7.19) have the highest AFH density among the counties examined, with Pierce also showing the highest enforcement rate (5.8%) among the three scraped counties.
4. **Oversight-Process Parallels (RF-16/18):** Washington State Auditor (SAO) reports describe HCA's Division of Program Integrity as relying on complaints rather than systematic risk-based analytics, and not routinely assessing the credibility of DSHS/MCO referrals. Minnesota's legislative auditor described a comparable reliance on complaints prior to Minnesota's enforcement wave. The parallel is in oversight *process*, as documented by each state's own auditors — it does not establish that Washington has experienced, or will experience, an outcome similar to Minnesota's.

## Data Availability & Limitations
The pilot adhered strictly to public data, yielding transparent limitations:
- **Enforcement History:** The DSHS public reports portal retains only a rolling ~3-4 year window. Facility-level enforcement history before 2023 requires a Public Records Request (PRR).
- **Deficiency Granularity:** Specific deficiency categories (e.g., abuse, staffing) are locked inside unstructured PDFs; extracting them requires a PRR for structured DSHS database records.
- **Ownership Linkage:** The public Medicaid exclusion list cannot be reliably joined to the AFH facility roster because facility names do not reliably match licensee legal names (0 verified matches found).
- **Billing Blind Spot:** The Minnesota indicators most directly tied to Minnesota's enforcement cases (impossible hours, maximum-unit billing, out-of-state billing) depend on claims data that is strictly internal to the ProviderOne system and is not observable from any public source.

## Recommendations
To extend this pilot toward a more complete public-data review-priority layer, and toward the claims-informed validation that would be required before any provider-level conclusion, a state or federal oversight body could:
1. **Execute targeted PRRs:** Request the 42 CFR 455.104 beneficial ownership data and the structured DSHS RCS enforcement database (including pre-2023 history and WAC deficiency codes) to close the public-data gaps documented above.
2. **Pilot the Public-Data Review-Priority Tier as a non-operational prototype:** Evaluate the proposed tier framework as a triage aid only, subject to claims-data validation, human review, and due-process safeguards before it informs any audit prioritization or enforcement action.
3. **Pair licensing data with claims data, under proper authorization:** Any claims-informed validation phase would need to bring DSHS licensing/enforcement data and HCA ProviderOne claims data together under a data-use agreement with appropriate state or federal authority, so that structural signals identified here (operator clusters, enforcement intensity) can be checked against billing patterns by staff authorized to see them — not by this project, which has no such access.
