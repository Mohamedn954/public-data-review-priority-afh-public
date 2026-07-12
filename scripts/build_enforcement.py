#!/usr/bin/env python3
"""Build WA_AFH_Enforcement_2020_2026.csv (facility-level summary) from the scraped RCS reports data.
Public portal retains ~2023-2026 only; 2020-2022 facility-level history is not public (requires PRR)."""
# Shared config: snapshot date, standard paths, and standard source strings.
# Override the date via AFH_DATE_ACCESSED for a future re-run.
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from _afh_config import (  # noqa: E402
    DATE_ACCESSED, DATA_DIR, OUT_DIR, SRC_DIR, SRC_ENFORCEMENT_SCRAPE,
)

import csv, os
DEL = OUT_DIR + "/"; os.makedirs(DEL,exist_ok=True)
SRC = SRC_ENFORCEMENT_SCRAPE
BASE="https://fortress.wa.gov/dshs/adsaapps/lookup/AFHForms.aspx?lic="

rows=[]
with open(_os.path.join(DATA_DIR, "WA_AFH_3County_Reports.csv")) as f:
    for r in csv.DictReader(f):
        ni=int(r["n_investigations"] or 0)
        ne=int(r["n_enforcement"] or 0)
        ncf=int(r["n_civil_fines"] or 0)
        nsp=int(r["n_stop_placement"] or 0)
        ncond=int(r["n_conditions"] or 0)
        ninsp=int(r["n_inspections"] or 0)
        total=int(r["n_docs_total"] or 0)
        years=r["years_present"]
        # repeat finding flag: enforcement docs in >=2 distinct years
        enf_years=[y for y in str(years).split(",") if y.strip()]
        repeat_enf = "Y" if ne>=2 and len([y for y in enf_years]) >=2 else ("Y" if ne>=2 else "N")
        rows.append({
            "facility_name":r["Facility_Name"],
            "license_number":r["License_Number"],
            "county":r["County"],
            "report_window":"2023-2026 (public portal retention window)",
            "report_types_present":"; ".join([t for t,c in [("inspections",ninsp),("investigations",ni),("enforcement letters",ne),("limitations",int(r["n_limitations"] or 0))] if c>0]) or "none posted",
            "total_reports_2023_2026":total,
            "total_complaint_investigations_2023_2026":ni,
            "total_enforcement_actions_2023_2026":ne,
            "total_civil_fines_2023_2026":ncf,
            "total_stop_placements_2023_2026":nsp,
            "total_license_conditions_2023_2026":ncond,
            "total_inspections_2023_2026":ninsp,
            "years_present":years,
            "latest_enforcement_year":r["latest_enforcement_year"],
            "high_complaint_load_flag":"Y" if ni>=3 else "N",
            "repeat_enforcement_flag":"Y" if ne>=2 else "N",
            "any_enforcement_flag":"Y" if ne>0 else "N",
            "stop_placement_flag":"Y" if nsp>0 else "N",
            "license_condition_flag":"Y" if ncond>0 else "N",
            "deficiency_category":"Not structured in public portal (in-PDF text only; abuse/neglect, medication, staffing, documentation categories require reading each PDF or a PRR)",
            "data_2020_2022":"Not publicly available - DSHS RCS portal retains only a rolling ~3-4 year window; pre-2023 documents require a Public Records Request",
            "source":SRC,
            "source_URL":BASE+r["License_Number"],
            "confidence_level":"High (2023-2026 counts); facility deficiency detail Low (not structured)",
        })

cols=["facility_name","license_number","county","report_window","report_types_present",
      "total_reports_2023_2026","total_complaint_investigations_2023_2026","total_enforcement_actions_2023_2026",
      "total_civil_fines_2023_2026","total_stop_placements_2023_2026","total_license_conditions_2023_2026",
      "total_inspections_2023_2026","years_present","latest_enforcement_year","high_complaint_load_flag",
      "repeat_enforcement_flag","any_enforcement_flag","stop_placement_flag","license_condition_flag",
      "deficiency_category","data_2020_2022","source","source_URL","confidence_level"]
with open(DEL+"WA_AFH_Enforcement_2020_2026.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)

# Summary stats
tot=len(rows)
enf=sum(1 for r in rows if r["any_enforcement_flag"]=="Y")
inv=sum(1 for r in rows if r["total_complaint_investigations_2023_2026"]>0)
hc=sum(1 for r in rows if r["high_complaint_load_flag"]=="Y")
re_=sum(1 for r in rows if r["repeat_enforcement_flag"]=="Y")
sp=sum(1 for r in rows if r["stop_placement_flag"]=="Y")
cf=sum(r["total_civil_fines_2023_2026"] for r in rows)
print(f"facilities={tot}  any_enforcement={enf}  any_investigation={inv}  high_complaint_load={hc}  repeat_enforcement={re_}  stop_placement={sp}  total_civil_fine_docs={cf}")
