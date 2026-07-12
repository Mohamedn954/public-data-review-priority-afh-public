#!/usr/bin/env python3
"""Pull the full current WA Adult Family Home roster from the DSHS-published
ArcGIS feature service (the nightly extract behind the official AFH locator),
deduplicate by license number, and write a clean facility master dataset.

Source: Long Term Care - Residential Care (owner DSHSAdmin)
Layer: .../Long_Term_Care_Residential_Care_view/FeatureServer/1
"""

# Shared config: snapshot date and standard paths.
# Override the date via AFH_DATE_ACCESSED for a future re-run.
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from _afh_config import DATE_ACCESSED, DATA_DIR, OUT_DIR, SRC_DIR  # noqa: E402

import requests, json, time
import pandas as pd

LAYER = "https://services2.arcgis.com/WW3T8U6q5EkZ9U3n/arcgis/rest/services/Long_Term_Care_Residential_Care_view/FeatureServer/1"

FIELDS = [
    "LicenseNumber","LocationNumber","FacInstanceId","FacilityType","FacilityName",
    "FacilityStatus","LocationAddress","LocationCity","LocationState","LocationZipCode",
    "LocationCounty","MailAddress","MailCity","MailState","MailZipCode","TelephoneNmbr",
    "RCSRegionUnit","Speciality","SpecialityCode","contract","ContractCode","FacilityPOC",
    "LicensedBedCount","LicenseExpirationDate","ServiceDisclosure","Has_Reports",
    "Reports_Location","Latitude","Longitude","GDLPublishDate","GDLArchiveDate"
]

def fetch_all(where):
    out = []
    offset = 0
    page = 2000
    while True:
        params = {
            "where": where,
            "outFields": ",".join(FIELDS),
            "returnGeometry": "false",
            "resultOffset": offset,
            "resultRecordCount": page,
            "orderByFields": "LicenseNumber,LocationNumber",
            "f": "json",
        }
        r = requests.get(LAYER + "/query", params=params, timeout=60)
        d = r.json()
        feats = d.get("features", [])
        if not feats:
            break
        out.extend([f["attributes"] for f in feats])
        if len(feats) < page:
            break
        offset += page
        time.sleep(0.3)
    return out

# Current (non-archived) Adult Family Home records
where = "FacilityType='AF' AND GDLArchiveDate IS NULL"
rows = fetch_all(where)
print(f"Fetched {len(rows)} current AF geocode rows")

df = pd.DataFrame(rows)

# Convert epoch-millis dates to readable dates
for c in ["LicenseExpirationDate","GDLPublishDate","GDLArchiveDate"]:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], unit="ms", errors="coerce").dt.date

# Deduplicate by license number (keep the row with the most recent publish date)
df_sorted = df.sort_values(["LicenseNumber","GDLPublishDate"], ascending=[True, False])
df_unique = df_sorted.drop_duplicates(subset=["LicenseNumber"], keep="first").copy()
print(f"Unique AFH facilities by license number: {len(df_unique)}")

# Add provenance columns
df_unique["SourceURL"] = LAYER
df_unique["DateAccessed"] = DATE_ACCESSED

# Rename to friendlier headers for the deliverable
rename = {
    "LicenseNumber":"License_Number","FacilityName":"Facility_Name","FacilityStatus":"License_Status",
    "LocationAddress":"Physical_Address","LocationCity":"City","LocationState":"State",
    "LocationZipCode":"ZIP","LocationCounty":"County","MailAddress":"Mailing_Address",
    "MailCity":"Mail_City","MailState":"Mail_State","MailZipCode":"Mail_ZIP",
    "TelephoneNmbr":"Phone","Speciality":"Specialty","contract":"Contract",
    "FacilityPOC":"Contact","LicensedBedCount":"Licensed_Capacity",
    "LicenseExpirationDate":"License_Expiration_Date","ServiceDisclosure":"Service_Disclosure_URL",
    "Has_Reports":"Has_Public_Reports","Reports_Location":"Reports_URL",
    "RCSRegionUnit":"RCS_Region_Unit",
}
df_unique = df_unique.rename(columns=rename)

col_order = [
    "License_Number","Facility_Name","License_Status","Physical_Address","City","ZIP","County",
    "Mailing_Address","Mail_City","Mail_ZIP","Phone","Licensed_Capacity","License_Expiration_Date",
    "Specialty","Contract","Contact","RCS_Region_Unit","Has_Public_Reports","Reports_URL",
    "Service_Disclosure_URL","Latitude","Longitude","SourceURL","DateAccessed"
]
col_order = [c for c in col_order if c in df_unique.columns]
df_unique = df_unique[col_order]

df_unique.to_csv(_os.path.join(DATA_DIR, "WA_AFH_Facility_Master.csv"), index=False)
print("Saved WA_AFH_Facility_Master.csv")

# Quick profile
print("\n=== PROFILE ===")
print("Total facilities:", len(df_unique))
print("Counties:", df_unique["County"].nunique())
print("Total licensed capacity:", df_unique["Licensed_Capacity"].sum())
print("\nTop 10 counties by facility count:")
print(df_unique["County"].value_counts().head(10))
print("\nContract (Medicaid) values sample:")
print(df_unique["Contract"].value_counts().head(10))
print("\nSpecialty values sample:")
print(df_unique["Specialty"].value_counts().head(10))
print("\nHas_Public_Reports:")
print(df_unique["Has_Public_Reports"].value_counts())
