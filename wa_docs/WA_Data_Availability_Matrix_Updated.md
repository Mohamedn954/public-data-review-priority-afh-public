# Washington Data Availability Matrix (Updated)
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
