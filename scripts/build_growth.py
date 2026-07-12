#!/usr/bin/env python3
"""Build WA_AFH_Growth_2013_2026.csv and WA_Medicaid_AFH_Contract_Trends (historical portion)
from official DSHS sources, with explicit confidence labels for reconstructed values."""
# Shared config: snapshot date, standard paths, and standard source strings.
# Override the date via AFH_DATE_ACCESSED for a future re-run.
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from _afh_config import (  # noqa: E402
    DATE_ACCESSED, DATA_DIR, OUT_DIR, SRC_DIR,
    SRC_BERK, SRC_MAN23, SRC_MAN24, SRC_ARC,
)

import csv, os
DEL = OUT_DIR + "/"; os.makedirs(DEL,exist_ok=True)

# active_AFHs, new_AFH_licenses, closed_or_inactive_AFHs, total_licensed_capacity, source, notes, confidence
rows = [
 # year, active, new, closed, capacity, source, notes, confidence
 [2013, 2842, "not public", "not public", 15596, SRC_BERK, "Official DSHS SFY 2013 figure (as of end of July). New/closed per-year counts not published as a public series.", "High"],
 [2014, 2772, "not public", "not public", 15214, SRC_BERK, "Official DSHS SFY 2014. Net decline of 70 homes vs 2013.", "High"],
 [2015, 2750, "not public", "not public", 15190, SRC_BERK, "Official DSHS SFY 2015. Trough of the flat decade.", "High"],
 [2016, 2768, "not public", "not public", 15316, SRC_BERK, "Official DSHS SFY 2016.", "High"],
 [2017, 2780, "not public", "not public", 15533, SRC_BERK, "Official DSHS SFY 2017. King County alone = 1,036 AFHs (Sept 2017).", "High"],
 [2018, 2806, "not public", "not public", 15741, SRC_BERK, "Official DSHS SFY 2018. End of the flat/stagnant era before the post-2018 surge.", "High"],
 [2019, "~2,900 (est)", "not public", "not public", "~16,100 (est)", "Reconstructed (interpolation between 2018 DSHS=2,806 and 2022 DSHS=4,315)", "ESTIMATE. No clean public annual count located for 2019. Linear/early-surge interpolation; treat as indicative only.", "Low"],
 [2020, "~3,300 (est)", "not public", "not public", "~17,800 (est)", "Reconstructed (interpolation 2018->2022)", "ESTIMATE. Surge believed to begin ~2019-2020. Value interpolated; not an official count.", "Low"],
 [2021, "~3,800 (est)", "not public", "not public", "~20,400 (est)", "Reconstructed (interpolation 2018->2022)", "ESTIMATE. Interpolated; not an official count.", "Low"],
 [2022, 4315, "not public", "not public", "~23,000 (est)", SRC_MAN23, "DSHS GIS count as of Aug 25 2022 (carried into 2023 deck). Capacity estimated from ~5.3 beds/home; bed count for this year not separately published.", "Medium"],
 [2023, 4315, "not public", "not public", "~23,000 (est)", SRC_MAN23, "DSHS deck reports 4,315 'as of July 27 2023' using Aug-2022 GIS extract; 2022 and 2023 effectively share this anchor. Capacity estimated.", "Medium"],
 [2024, 4960, "not public", "not public", "~28,000 (est)", SRC_MAN24, "Official DSHS GIS count as of Aug 14 2024. Cross-check: industry sources cite ~5,088 by Dec 2024. Capacity estimated from bed/home ratio.", "High"],
 [2025, "~5,400 (est)", "not public", "not public", "~31,000 (est)", "Reconstructed (interpolation 2024->2026)", "ESTIMATE. Between Aug-2024 official (4,960) and 2026 roster. Interpolated.", "Low"],
 [2026, 6075, "not public", "not public", 35305, SRC_ARC, f"Current DSHS ArcGIS roster deduped by license number (accessed {DATE_ACCESSED}). NOTE: geocoded view may slightly over-count vs DSHS RDA methodology; treat as upper-bound current snapshot. 35,305 licensed beds.", "Medium"],
]

with open(DEL+"WA_AFH_Growth_2013_2026.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["year","active_AFHs","new_AFH_licenses","closed_or_inactive_AFHs","total_licensed_capacity","source","notes","confidence_level"])
    for r in rows: w.writerow(r)
print("WA_AFH_Growth_2013_2026.csv written:",len(rows),"rows")

# Historical Medicaid-contract trend (official 2009-2018 from BERK Table 3.4) + current snapshot
mc_rows = [
 # year, county(blank=statewide), total_AFHs, mc_AFHs, pct, contract_type, specialty, source, notes, confidence
 [2013,"STATEWIDE",2842,2496,round(2496/2842*100,1),"AFH Medicaid contract (all types)","All","DSHS BERK 2018 Table 3.1/3.4","Official. 87.8% of AFHs Medicaid-contracted in 2013.","High"],
 [2015,"STATEWIDE",2750,2438,round(2438/2750*100,1),"AFH Medicaid contract (all types)","All","DSHS BERK 2018 Table 3.1/3.4","Official. 88.7% contracted.","High"],
 [2017,"STATEWIDE",2780,2454,round(2454/2780*100,1),"AFH Medicaid contract (all types)","All","DSHS BERK 2018 Table 3.1/3.4","Official. 88.3% contracted.","High"],
 [2018,"STATEWIDE",2806,2478,round(2478/2806*100,1),"AFH Medicaid contract (all types)","All","DSHS BERK 2018 Table 3.1/3.4","Official. 88.3% contracted; 13,889 of 15,741 beds in MC facilities.","High"],
]
with open(DEL+"WA_Medicaid_AFH_Contract_Trends_HISTORICAL.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["year","county","total_AFHs","Medicaid_contracted_AFHs","percent_Medicaid_contracted","contract_type","specialty_designation","source","notes","confidence_level"])
    for r in mc_rows: w.writerow(r)
print("historical MC trend written")
