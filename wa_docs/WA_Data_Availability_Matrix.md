# Washington AFH/HCBS Data Availability Matrix

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
