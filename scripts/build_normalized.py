#!/usr/bin/env python3
"""Build WA_County_Normalized_Risk.csv: AFHs & beds per 1,000 seniors (65+),
plus enforcement/complaint rates (real for King/Pierce/Spokane; not-collected for others)."""
# Shared config: snapshot date, standard paths, and standard source strings.
# Override the date via AFH_DATE_ACCESSED for a future re-run.
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from _afh_config import DATE_ACCESSED, DATA_DIR, OUT_DIR, SRC_DIR, SRC_CENSUS  # noqa: E402

import csv, os
from collections import defaultdict
DEL = OUT_DIR + "/"; os.makedirs(DEL,exist_ok=True)

# Census Reporter ACS 5-year: total pop, 65+ pop
CENSUS={
 "King":(2340211,340494),"Pierce":(941170,146382),"Spokane":(555947,101284),
 "Snohomish":(864113,134546),"Clark":(527269,91801),"Thurston":(302912,58525),
 "Yakima":(258523,39149),"Benton":(218190,36016),"Franklin":(101238,11083),
}
CENSUS_SRC = SRC_CENSUS

# Facility counts/beds from statewide master roster
cnt=defaultdict(int); beds=defaultdict(int); mc=defaultdict(int)
with open(_os.path.join(DATA_DIR, "WA_AFH_Facility_Master.csv")) as f:
    for row in csv.DictReader(f):
        c=(row["County"] or "").strip().title()
        if not c: continue
        cnt[c]+=1
        try: beds[c]+=int(float(row["Licensed_Capacity"] or 0))
        except: pass
        if (row["Contract"] or "").strip(): mc[c]+=1

# Enforcement/complaint aggregates (only for the 3 scraped counties)
enf=defaultdict(lambda:defaultdict(int))
SCRAPED={"King","Pierce","Spokane"}
with open(_os.path.join(DATA_DIR, "WA_AFH_3County_Reports.csv")) as f:
    for row in csv.DictReader(f):
        c=(row["County"] or "").strip().title()
        if int(row["n_enforcement"] or 0)>0: enf[c]["enf_fac"]+=1
        if int(row["n_investigations"] or 0)>0: enf[c]["inv_fac"]+=1
        enf[c]["investigations"]+=int(row["n_investigations"] or 0)
        enf[c]["enf_actions"]+=int(row["n_enforcement"] or 0)
        enf[c]["civil_fines"]+=int(row["n_civil_fines"] or 0)
        if int(row["n_investigations"] or 0)>=3: enf[c]["high_complaint"]+=1

NA="not collected in pilot (enforcement scrape scoped to King/Pierce/Spokane)"
rows=[]
for c in ["King","Pierce","Spokane","Snohomish","Clark","Thurston","Yakima","Benton","Franklin"]:
    tot,p65=CENSUS[c]
    afhs=cnt.get(c,0); bd=beds.get(c,0); mcc=mc.get(c,0)
    afh_per_1k=round(afhs/(p65/1000),2) if p65 else ""
    beds_per_1k=round(bd/(p65/1000),2) if p65 else ""
    if c in SCRAPED:
        e=enf[c]
        enf_rate=round(e["enf_fac"]/afhs*100,1) if afhs else ""
        inv_rate=round(e["inv_fac"]/afhs*100,1) if afhs else ""
        enf_per_1k=round(e["enf_actions"]/(p65/1000),2) if p65 else ""
        inv_per_1k=round(e["investigations"]/(p65/1000),2) if p65 else ""
        high_c=e["high_complaint"]
        enf_fac=e["enf_fac"]; inv_fac=e["inv_fac"]; civ=e["civil_fines"]
    else:
        enf_rate=inv_rate=enf_per_1k=inv_per_1k=high_c=enf_fac=inv_fac=civ=NA
    rows.append({
        "county":c,
        "total_population":tot,
        "population_65plus":p65,
        "pct_65plus":round(p65/tot*100,1),
        "licensed_AFHs":afhs,
        "licensed_beds":bd,
        "Medicaid_contracted_AFHs":mcc,
        "AFHs_per_1000_seniors":afh_per_1k,
        "AFH_beds_per_1000_seniors":beds_per_1k,
        "facilities_with_enforcement":enf_fac,
        "facilities_with_investigations":inv_fac,
        "facilities_high_complaint_load":high_c,
        "enforcement_rate_pct":enf_rate,
        "investigation_rate_pct":inv_rate,
        "enforcement_actions_per_1000_seniors":enf_per_1k,
        "investigations_per_1000_seniors":inv_per_1k,
        "total_civil_fine_docs":civ,
        "facility_source":f"DSHS ArcGIS Residential Care roster (current), accessed {DATE_ACCESSED}",
        "enforcement_source":"DSHS RCS reports portal 2023-2026 scrape" if c in SCRAPED else NA,
        "census_source":CENSUS_SRC,
        "confidence_level":"High (facility & census); High (enforcement, 3 counties)" if c in SCRAPED else "High (facility & census); enforcement N/A",
    })

cols=list(rows[0].keys())
with open(DEL+"WA_County_Normalized_Risk.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)

print(f"{'County':10s} {'65+':>8s} {'AFHs':>6s} {'/1k sr':>7s} {'beds/1k':>8s} {'enf%':>6s} {'inv%':>6s}")
for r in rows:
    print(f"{r['county']:10s} {r['population_65plus']:>8,} {r['licensed_AFHs']:>6} {str(r['AFHs_per_1000_seniors']):>7} {str(r['AFH_beds_per_1000_seniors']):>8} {str(r['enforcement_rate_pct']):>6} {str(r['investigation_rate_pct']):>6}")
