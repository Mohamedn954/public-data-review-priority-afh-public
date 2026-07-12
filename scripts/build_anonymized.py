"""
build_anonymized.py
-------------------
Produce the journal-safe / replication version of the Washington pilot dataset.

All direct facility identifiers are removed and replaced with stable,
non-identifying IDs (facility_id F#####, cluster_id OP###) so that no individual
home or operator can be named or re-identified. City is removed (re-identification
risk in small towns when combined with capacity, specialty, enforcement/complaint
counts, and cluster membership); County is retained as the coarsest geographic
level needed to reproduce county-level results.

Outputs (to OUT_DIR/anonymized_data/):
  WA_AFH_3County_Enriched_ANON.csv
  WA_AFH_3County_Reports_ANON.csv
  WA_AFH_Facility_RedFlags_ANON.csv
  WA_Operator_Clusters_ANON.csv
  WA_County_Concentration.csv          (copied; no identifiers)
  WA_County_Normalized_Risk.csv        (copied; no identifiers)
Private crosswalks (facility_id/cluster_id -> raw keys) are written to
DATA_DIR/private/ and are deliberately NOT part of the journal package.
"""

import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd
import shutil

ANON_DIR = _os.path.join(OUT_DIR, "anonymized_data")
PRIV_DIR = _os.path.join(DATA_DIR, "private")
_os.makedirs(ANON_DIR, exist_ok=True)
_os.makedirs(PRIV_DIR, exist_ok=True)

# ---- Build stable ID maps from the master enriched file (the universe) ----
enr = pd.read_csv(_os.path.join(DATA_DIR, "WA_AFH_3County_Enriched.csv"), dtype=str)

lic_sorted = sorted(enr["License_Number"].dropna().unique())
fac_id = {lic: f"F{str(i + 1).zfill(5)}" for i, lic in enumerate(lic_sorted)}

phone_counts = enr["phone_key"].value_counts()
multi_phones = sorted([p for p in phone_counts.index
                       if pd.notna(p) and p != "" and phone_counts[p] >= 2])
cluster_id = {p: f"OP{str(i + 1).zfill(3)}" for i, p in enumerate(multi_phones)}

# Direct identifiers / re-identification vectors to DROP (note: City included)
DROP = ["Facility_Name", "Physical_Address", "Mailing_Address", "Mail_City", "Mail_ZIP",
        "Phone", "Contact", "Reports_URL", "reports_url", "Service_Disclosure_URL",
        "addr_key", "phone_key", "source_URL", "SourceURL", "exclusion_name_match",
        "License_Expiration_Date", "Latitude", "Longitude", "ZIP", "City"]


def anonymize(df, has_phone=True):
    df = df.copy()
    if "License_Number" in df.columns:
        df.insert(0, "facility_id", df["License_Number"].map(fac_id))
        df = df.drop(columns=["License_Number"])
    if has_phone and "phone_key" in df.columns:
        df["cluster_id"] = df["phone_key"].map(cluster_id).fillna("")
    df = df.drop(columns=[c for c in DROP if c in df.columns])
    return df


# 1. Enriched (master analysis file)
anonymize(enr).to_csv(_os.path.join(ANON_DIR, "WA_AFH_3County_Enriched_ANON.csv"), index=False)

# 2. Reports
rep = pd.read_csv(_os.path.join(DATA_DIR, "WA_AFH_3County_Reports.csv"), dtype=str)
anonymize(rep, has_phone=False).to_csv(
    _os.path.join(ANON_DIR, "WA_AFH_3County_Reports_ANON.csv"), index=False)

# 3. Facility RedFlags
rf = pd.read_csv(_os.path.join(DATA_DIR, "WA_AFH_Facility_RedFlags.csv"), dtype=str)
anonymize(rf, has_phone=False).to_csv(
    _os.path.join(ANON_DIR, "WA_AFH_Facility_RedFlags_ANON.csv"), index=False)

# 4. Operator clusters: replace phone_key with cluster_id, keep aggregates only
cl = pd.read_csv(_os.path.join(DATA_DIR, "WA_Operator_PhoneClusters.csv"))
cl["cluster_id"] = cl["phone_key"].map(cluster_id)
keep = [c for c in ["cluster_id", "n_licenses", "counties", "total_enforcement",
                    "total_investigations", "total_civil_fines"] if c in cl.columns]
cl[keep].sort_values("cluster_id").to_csv(
    _os.path.join(ANON_DIR, "WA_Operator_Clusters_ANON.csv"), index=False)

# 5. County-level files (no facility identifiers) copied unchanged
for f in ["WA_County_Concentration.csv", "WA_County_Normalized_Risk.csv"]:
    src = _os.path.join(DATA_DIR, f)
    if _os.path.exists(src):
        shutil.copy(src, _os.path.join(ANON_DIR, f))

# Private crosswalks (NOT for the journal package)
pd.DataFrame({"facility_id": list(fac_id.values()),
              "License_Number": list(fac_id.keys())}).to_csv(
    _os.path.join(PRIV_DIR, "PRIVATE_facility_id_crosswalk.csv"), index=False)
pd.DataFrame({"cluster_id": list(cluster_id.values()),
              "phone_key_raw": list(cluster_id.keys())}).to_csv(
    _os.path.join(PRIV_DIR, "PRIVATE_cluster_id_crosswalk.csv"), index=False)

# ---- Reproducibility check ----
e = pd.read_csv(_os.path.join(ANON_DIR, "WA_AFH_3County_Enriched_ANON.csv"))
for c in ["n_enforcement", "phone_shared_count", "Licensed_Capacity"]:
    e[c] = pd.to_numeric(e[c], errors="coerce")
print("=== ANONYMIZED PACKAGE BUILT ===")
print(f"  Facilities: {len(e)} (expect 3457)")
print(f"  Beds: {int(e['Licensed_Capacity'].sum())} (expect 20157)")
print(f"  In clusters: {int((e['phone_shared_count'] >= 2).sum())} (expect 164)")
print(f"  >=1 enforcement: {int((e['n_enforcement'] >= 1).sum())} (expect 165)")
print(f"  Clusters: {len(cluster_id)} (expect 72)")
print(f"  County split: {dict(e['County'].value_counts())}")
print(f"  'City' column present: {'City' in e.columns} (expect False)")
