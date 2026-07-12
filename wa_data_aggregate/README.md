# wa_data_aggregate/ — County/statewide-year aggregate WA data

This folder holds county-level and statewide-year aggregate data for
Washington. **No file in this folder contains facility-level rows.**

## Files

| File | Description |
|---|---|
| `WA_AFH_Growth_2013_2026.csv` | Statewide licensed-AFH counts and licensed-capacity by year, 2013–2026. Includes an explicit `confidence_level` column marking interpolated / reconstructed years distinctly from official DSHS figures. |
| `WA_Medicaid_AFH_Contract_Trends_HISTORICAL.csv` | Historical statewide AFH Medicaid-contract share, 2013–2018, from the DSHS BERK Payment Methodology Analysis (2018). |
| `WA_LTC_Spending_Biennia.csv` | WA DSHS long-term-care biennial appropriation series, 2013-15 through 2025-27, with per-row source citation, appropriation level (enacted / approximate / proposed), and confidence label. Used by `scripts/build_charts.py` to render the RF-02 spending-growth chart. See the CSV itself for provenance of each value. |
| `WA_RedFlag_Testability_Matrix.csv` | An earlier version of the 20-indicator typology; the canonical version at repo root is `WA_RedFlag_Testability_Matrix_v2.csv`. |

## On the LTC spending series

The `WA_LTC_Spending_Biennia.csv` file replaces a previously hardcoded list
inside `scripts/build_charts.py`. Every biennium row now carries an explicit
source URL, access date, and confidence label. In particular:

* 2013-15 through 2021-23 are drawn from the Washington Research Council's
  2021 policy brief (Chart 1, All Funds series), which itself draws directly
  from state budget records — high confidence.
* 2023-25 = $10.44B (High confidence). Sourced to the OFM Agency
  Recommendation Summary for DSHS Long Term Care (unit 050), "Current Budget
  (2023-25 Original)" line — the originally-enacted total, before the 2024
  supplemental amendment. This baseline drives the growth claim in the
  manuscript and RF-02, now recomputed as +25.2% against the 2025-27
  proposed level.
* 2025-27 = $13.07B is the OFM Governor's *proposed* level, not enacted.
  A DSHS-reported enacted figure of approximately $12.9B is corroborated via
  The Center Square (2025).

The chart rendered by `build_charts.py` colors bars by appropriation level
(blue = enacted; orange = approximate; red = proposed) so these distinctions
are visible in the figure as well as the CSV.
