#!/usr/bin/env python3
"""Subset the full WA AFH master dataset to King, Pierce, and Spokane counties,
and derive a Medicaid-contract flag and capacity/specialty profile.
"""

import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd

SRC = _os.path.join(DATA_DIR, "WA_AFH_Facility_Master.csv")
OUT = _os.path.join(DATA_DIR, "WA_AFH_3County_Master.csv")

df = pd.read_csv(SRC, dtype=str)
df["Licensed_Capacity"] = pd.to_numeric(df["Licensed_Capacity"], errors="coerce")

counties = ["King", "Pierce", "Spokane"]
sub = df[df["County"].isin(counties)].copy()

# Derive Medicaid-contract flag: per DSHS locator, "Only facilities with DSHS
# contracts can accept Medicaid." Contract field lists contracts; treat presence
# of any LTSS contract beyond base 'Adult Family Home' OR any contract string as
# Medicaid-capable. AFHs without a DSHS contract cannot bill Medicaid.
def medicaid_flag(contract):
    if pd.isna(contract) or str(contract).strip() == "":
        return "No/Unknown"
    return "Yes (has DSHS contract)"

sub["Medicaid_Contract_Flag"] = sub["Contract"].apply(medicaid_flag)

sub.to_csv(OUT, index=False)

print("=== 3-COUNTY AFH ROSTER ===")
print("Total facilities:", len(sub))
print(sub["County"].value_counts())
print("\nTotal licensed beds:", int(sub["Licensed_Capacity"].sum()))
print("\nMedicaid contract flag:")
print(sub["Medicaid_Contract_Flag"].value_counts())
print("\nBy county - facilities and beds:")
print(sub.groupby("County")["Licensed_Capacity"].agg(["count","sum","mean"]).round(1))
print("\nSpecialty distribution:")
print(sub["Specialty"].value_counts().head(8))
print("\nSaved:", OUT)
