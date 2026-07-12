#!/usr/bin/env python3

import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd
DATA=DATA_DIR + "/"
df=pd.read_csv(DATA+"WA_AFH_3County_Enriched.csv",dtype=str)
df["phone_shared_count"]=pd.to_numeric(df["phone_shared_count"],errors="coerce").fillna(1).astype(int)
for c in ["n_enforcement","n_investigations","n_civil_fines"]:
    df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0).astype(int)

# Verify the exclusion match
hit=df[df["exclusion_name_match"].fillna("")!=""]
print("=== EXCLUSION MATCH DETAIL ===")
print(hit[["License_Number","Facility_Name","City","County","exclusion_name_match"]].to_string())

# Phone-based operator clusters (>=2 licenses share a phone)
clusters=df[(df["phone_shared_count"]>=2) & (df["phone_key"].fillna("")!="")].copy()
clusters=clusters.sort_values(["phone_shared_count","phone_key"],ascending=[False,True])
agg=clusters.groupby("phone_key").agg(
    n_licenses=("License_Number","count"),
    facilities=("Facility_Name",lambda s:" | ".join(sorted(set(s))[:6])),
    counties=("County",lambda s:",".join(sorted(set(s)))),
    cities=("City",lambda s:",".join(sorted(set(s))[:6])),
    total_enforcement=("n_enforcement","sum"),
    total_investigations=("n_investigations","sum"),
    total_civil_fines=("n_civil_fines","sum"),
).reset_index().sort_values("n_licenses",ascending=False)
agg.to_csv(DATA+"WA_Operator_PhoneClusters.csv",index=False)
print("\n=== PHONE CLUSTERS (top 15) ===")
print("Total multi-license phone clusters:",len(agg))
print(agg.head(15).to_string())
