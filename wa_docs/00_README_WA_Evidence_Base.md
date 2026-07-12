# Washington State AFH/HCBS Program Integrity Evidence Base

This package applies 20 review-priority indicators (RF-01 to RF-20), derived from Minnesota's public Medicaid enforcement record, to Washington State's Adult Family Home (AFH) sector, focusing on King, Pierce, and Spokane counties. It is built strictly from verifiable public data (DSHS, HCA, SAO, OFM, SOS). No Washington facility or operator is identified, ranked, or alleged to have committed fraud anywhere in this package.

## Deliverables Included

### 1. Strategic Documents
* **`WA_RedFlag_Testability_Memo.pdf`**: The core analysis of which Minnesota-derived indicators are testable in Washington, the gap in public billing data, and the findings on operator clustering and oversight capacity.
* **`WA_Data_Availability_Matrix.pdf`**: A strict accounting of what is public vs. what requires a Public Records Request (PRR). Includes the PRR target list needed to fully test the indicator typology in Washington.
* **`WA_Source_Bibliography.pdf`**: Direct URLs to the primary state data sources used.

### 2. Visualizations
* **`WA_LTC_Spending_Growth.png`**: Chart of DSHS Long-Term Care budget growth by biennium (RF-02 context). See `wa_data_aggregate/WA_LTC_Spending_Biennia.csv` for sourcing.
* **`WA_County_Concentration_Enforcement.png`**: Chart showing AFH distribution and enforcement/investigation rates across the three subject counties.

### 3. Structured Datasets (CSV)
* **`WA_AFH_Facility_RedFlags.csv`**: The master facility-level dataset (3,457 homes). Includes DSHS licensing data, scraped enforcement/complaint tallies (2023-2026), and computed indicator flags for multi-home operators (RF-03/08 proxies) and high complaint loads.
* **`WA_Operator_PhoneClusters.csv`**: The 72 multi-home operator clusters identified by shared phone numbers, aggregated with their total enforcement and investigation counts.
* **`WA_RedFlag_Testability_Matrix.csv`**: The row-by-row mapping of RF-01 through RF-20 against WA data sources.
* **`WA_County_Concentration.csv`**: Summary metrics by county.

## Key Insight
Washington's public data supports testing of structural indicators (RF-08 related-party networks, RF-18 oversight capacity, RF-19 program design) and mapping enforcement intensity. The behavioral billing-anomaly indicators that require claims review (RF-10 impossible hours, RF-11 max-unit billing, RF-13 deceased recipients) depend on data held inside HCA's ProviderOne claims system, which is not public. Extending this review-priority layer into claims-informed validation would require a state or federal body with authorized access to bring DSHS licensing/enforcement data together with internal HCA claims analytics — a step this project does not perform.
