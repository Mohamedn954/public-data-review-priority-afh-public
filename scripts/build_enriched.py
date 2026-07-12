#!/usr/bin/env python3
"""Build the enriched 3-county AFH dataset:
  - merge facility roster + reports tallies
  - compute within-data network clustering (shared address / phone / contact)
  - cross-check against HCA + DSHS exclusion lists
  - compute county-level concentration metrics
Outputs enriched CSV + several summary tables.
"""

import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd, numpy as np, re, json

DATA=DATA_DIR + "/"
master=pd.read_csv(DATA+"WA_AFH_3County_Master.csv",dtype=str)
reports=pd.read_csv(DATA+"WA_AFH_3County_Reports.csv",dtype=str)

num_cols=["n_inspections","n_investigations","n_enforcement","n_limitations",
          "n_civil_fines","n_stop_placement","n_conditions","n_docs_total"]
for c in num_cols:
    reports[c]=pd.to_numeric(reports[c],errors="coerce").fillna(0).astype(int)

rep_keep=["License_Number"]+num_cols+["latest_year","latest_enforcement_year","reports_url"]
df=master.merge(reports[rep_keep],on="License_Number",how="left")
for c in num_cols: df[c]=df[c].fillna(0).astype(int)

df["Licensed_Capacity"]=pd.to_numeric(df["Licensed_Capacity"],errors="coerce")

# ---- Network clustering signals (PUBLIC, computed within dataset) ----
def norm(s):
    if pd.isna(s): return ""
    return re.sub(r"\s+"," ",str(s).strip().upper())

for col,src in [("addr_key","Physical_Address"),("phone_key","Phone")]:
    if src in df.columns:
        df[col]=df[src].apply(norm)
    else:
        df[col]=""

# count licenses sharing same normalized address / phone
if df["addr_key"].astype(bool).any():
    addr_counts=df[df["addr_key"]!=""]["addr_key"].value_counts()
    df["addr_shared_count"]=df["addr_key"].map(addr_counts).fillna(1).astype(int)
else:
    df["addr_shared_count"]=1
if df["phone_key"].astype(bool).any():
    phone_counts=df[df["phone_key"]!=""]["phone_key"].value_counts()
    df["phone_shared_count"]=df["phone_key"].map(phone_counts).fillna(1).astype(int)
else:
    df["phone_shared_count"]=1

# ---- Exclusion cross-check ----
def load_excl():
    names=set()
    try:
        h=pd.read_excel(_os.path.join(SRC_DIR, "hca_termination_exclusion.xlsx"),dtype=str,header=4)
        for v in h.iloc[:,0].dropna():
            for part in str(v).split("\n"):
                p=norm(part)
                if p: names.add(p)
    except Exception as e: print("HCA excl load err",e)
    try:
        d=pd.read_excel(_os.path.join(SRC_DIR, "hca_termination_exclusion_dshs.xlsx"),dtype=str)
        for v in d.iloc[:,0].dropna(): 
            p=norm(v)
            if p: names.add(p)
    except Exception as e: print("DSHS excl load err",e)
    return names
excl_names=load_excl()

GENERIC=set("ADULT FAMILY HOME CARE LLC INC CORP HOMES SENIOR LIVING THE AND AFH II III IV HOUSE PLACE".split())
def tokens(s):
    return set(t for t in re.split(r"[^A-Z0-9]+",norm(s)) if t and t not in GENERIC and len(t)>2)
def excl_hit(fac):
    """Require a meaningful distinctive-token overlap, not a substring of generic words."""
    ft=tokens(fac)
    if not ft: return ""
    for n in excl_names:
        nt=tokens(n)
        if not nt: continue
        # require ALL distinctive tokens of the (shorter) exclusion name to be present
        if len(nt)>=2 and nt.issubset(ft):
            return n
    return ""
df["exclusion_name_match"]=df["Facility_Name"].apply(excl_hit)

df.to_csv(DATA+"WA_AFH_3County_Enriched.csv",index=False)

# ---- County concentration table ----
tot_fac=len(df); tot_beds=df["Licensed_Capacity"].sum()
ct=df.groupby("County").agg(
    facilities=("License_Number","count"),
    beds=("Licensed_Capacity","sum"),
    avg_beds=("Licensed_Capacity","mean"),
    w_enforcement=("n_enforcement",lambda s:(s>0).sum()),
    w_investigations=("n_investigations",lambda s:(s>0).sum()),
    w_stop_placement=("n_stop_placement",lambda s:(s>0).sum()),
    w_conditions=("n_conditions",lambda s:(s>0).sum()),
    civil_fines=("n_civil_fines","sum"),
).reset_index()
ct["pct_of_3county_facilities"]=(ct["facilities"]/tot_fac*100).round(1)
ct["enforcement_rate_pct"]=(ct["w_enforcement"]/ct["facilities"]*100).round(1)
ct["investigation_rate_pct"]=(ct["w_investigations"]/ct["facilities"]*100).round(1)
ct.to_csv(DATA+"WA_County_Concentration.csv",index=False)

print("=== ENRICHED DATASET ===")
print("Facilities:",tot_fac,"| Beds:",int(tot_beds))
print("\n=== COUNTY CONCENTRATION ===")
print(ct.to_string())
print("\n=== NETWORK CLUSTERING ===")
print("Facilities sharing an address with >=2 licenses:",(df["addr_shared_count"]>=2).sum())
print("Max licenses at one address:",df["addr_shared_count"].max())
print("Facilities sharing a phone with >=2 licenses:",(df["phone_shared_count"]>=2).sum())
print("Max licenses at one phone:",df["phone_shared_count"].max())
print("\n=== EXCLUSION CROSS-CHECK ===")
print("Exclusion-list name matches among AFH facility names:",(df["exclusion_name_match"]!="").sum())
print("\n=== ENFORCEMENT INTENSITY (3-county) ===")
print("Facilities w/ enforcement:",(df["n_enforcement"]>0).sum())
print("Total civil fines:",int(df["n_civil_fines"].sum()))
print("Total stop-placement orders:",int(df["n_stop_placement"].sum()))
print("Total conditions imposed:",int(df["n_conditions"].sum()))
print("Columns available:",list(df.columns))
