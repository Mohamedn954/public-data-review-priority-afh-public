
import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd
import os

# 1. Create Case Dataset
cases = [
    # EIDBI (Autism)
    {"Defendant": "Faysal Abdiweli", "Entity": "EIDBI Autism Center", "Program": "EIDBI", "Amount": 16000000, "Charges": "Wire fraud, Identity theft", "Status": "Charged (May 2026)", "Source": "DOJ May 2026 Takedown", "Red_Flags": "RF-10, RF-14, RF-15"},
    {"Defendant": "Abdinajib Hassan Yussuf", "Entity": "Star Autism Center LLC", "Program": "EIDBI", "Amount": 6000000, "Charges": "Wire fraud", "Status": "Charged (Dec 2025)", "Source": "IRS-CI Dec 2025", "Red_Flags": "RF-13, RF-14"},
    {"Defendant": "Asha Farhan Hassan", "Entity": "EIDBI Autism Center", "Program": "EIDBI", "Amount": 14000000, "Charges": "Wire fraud", "Status": "Pled Guilty (Dec 2025)", "Source": "IRS-CI Dec 2025", "Red_Flags": "RF-06 (Feeding Our Future connection)"},
    
    # HSS
    {"Defendant": "Hassan Ahmed Hussein, Ahmed Abdirashid Mohamed", "Entity": "Pristine Health LLC", "Program": "HSS", "Amount": 750000, "Charges": "Wire fraud", "Status": "Charged (Dec 2025)", "Source": "IRS-CI Dec 2025", "Red_Flags": "RF-09, RF-14"},
    {"Defendant": "Kaamil Omar Sallah", "Entity": "SafeLodgings, Inc.", "Program": "HSS", "Amount": 1400000, "Charges": "Wire fraud", "Status": "Charged (Dec 2025), Fled", "Source": "IRS-CI Dec 2025", "Red_Flags": "RF-10, RF-12"},
    {"Defendant": "Anthony Waddell Jefferson, Lester Brown", "Entity": "HSS Provider", "Program": "HSS", "Amount": 3500000, "Charges": "Wire fraud", "Status": "Charged (Dec 2025)", "Source": "IRS-CI Dec 2025", "Red_Flags": "RF-09, RF-13, RF-14"},
    {"Defendant": "Moktar Hassan Aden, Mustafa Dayib Ali, Khalid Ahmed Dayib, Abdifitah Mohamud Mohamed", "Entity": "Brilliant Minds Services LLC, Foundation First Services LLC", "Program": "HSS", "Amount": 2300000, "Charges": "Wire fraud", "Status": "Charged (Sep 2025)", "Source": "IRS-CI Sep 2025", "Red_Flags": "RF-03, RF-11, RF-14"},
    {"Defendant": "Christopher Adesoji Falade, Emmanuel Oluwademilade Falade", "Entity": "Faladcare Inc.", "Program": "HSS", "Amount": 2200000, "Charges": "Wire fraud", "Status": "Charged (Sep 2025)", "Source": "IRS-CI Sep 2025", "Red_Flags": "RF-11"},
    {"Defendant": "Asad Ahmed Adow", "Entity": "Leo Human Services LLC", "Program": "HSS", "Amount": 2700000, "Charges": "Wire fraud", "Status": "Charged (Sep 2025)", "Source": "IRS-CI Sep 2025", "Red_Flags": "RF-11, RF-14"},
    {"Defendant": "Anwar Ahmed Adow", "Entity": "Liberty Plus LLC", "Program": "HSS", "Amount": 1200000, "Charges": "Wire fraud", "Status": "Charged (Sep 2025)", "Source": "IRS-CI Sep 2025", "Red_Flags": "RF-11, RF-14"},

    # ICS
    {"Defendant": "Ultimate Home Health Services LLC (Business)", "Entity": "Ultimate Home Health Services LLC", "Program": "ICS", "Amount": 1100000, "Charges": "Search Warrant", "Status": "Under Investigation (Dec 2025)", "Source": "IRS-CI Dec 2025", "Red_Flags": "RF-10, RF-13 (Deceased recipient)"},
    
    # IHS
    {"Defendant": "Healey Homes (Entity)", "Entity": "Healey Homes", "Program": "IHS", "Amount": 22000000, "Charges": "Wire fraud", "Status": "Charged (May 2026)", "Source": "DOJ May 2026 Takedown", "Red_Flags": "RF-07 (Concealed ownership of housing)"},

    # State AG Takedown / Prosecutions
    {"Defendant": "Tremayne Lamar Jackson", "Entity": "PCA Provider", "Program": "PCA", "Amount": 125000, "Charges": "7 felony theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-10, RF-12 (Out of state)"},
    {"Defendant": "Christine Marie Pryor", "Entity": "Counseling Provider", "Program": "Psychotherapy", "Amount": 150000, "Charges": "6 theft, 6 identity theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-14, RF-15"},
    {"Defendant": "Fernando Navarro", "Entity": "PCA Provider", "Program": "PCA", "Amount": 70000, "Charges": "4 felony theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-10, RF-12 (Recipient out of state)"},
    {"Defendant": "Shawki Elsaid", "Entity": "PCA Provider", "Program": "PCA", "Amount": 182000, "Charges": "8 theft, 2 identity theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-10, RF-12, RF-15"},
    {"Defendant": "Ahmed Agwa", "Entity": "PCA Provider", "Program": "PCA", "Amount": 94000, "Charges": "6 felony theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-10, RF-12, RF-13 (Deceased recipient)"},
    {"Defendant": "Edward Sherrod", "Entity": "PCA Provider", "Program": "PCA", "Amount": 60000, "Charges": "6 felony theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-10"},
    {"Defendant": "Jessica Wavra", "Entity": "ARMHS Provider", "Program": "ARMHS", "Amount": 29000, "Charges": "5 theft", "Status": "Charged (Jun 2026)", "Source": "MN AG Jun 2026", "Red_Flags": "RF-10"},
    {"Defendant": "Abdifatah Yusuf, Lul Ahmed", "Entity": "Promise Health Services LLC", "Program": "HCBS", "Amount": 7200000, "Charges": "Racketeering, Theft", "Status": "Charged (Jun 2024 / Dec 2023)", "Source": "MN AG Jun 2024", "Red_Flags": "RF-09, RF-10, RF-13"},
    {"Defendant": "Abdiweli Mohamud, Abdirashid Said", "Entity": "Minnesota Home Health Care LLC", "Program": "PCA", "Amount": 1800000, "Charges": "Racketeering, Theft", "Status": "Charged (Jun 2024 / Dec 2023)", "Source": "MN AG Jun 2024", "Red_Flags": "RF-06 (Excluded provider), RF-10"},
    {"Defendant": "Charles Omato, LaTonia Jackson", "Entity": "Driving Miss Daisy", "Program": "NEMT", "Amount": 1400000, "Charges": "Theft", "Status": "Charged (Jun 2024)", "Source": "MN AG Jun 2024", "Red_Flags": "RF-10, RF-12"}
]

df_cases = pd.DataFrame(cases)
df_cases.to_csv(_os.path.join(OUT_DIR, 'MN_Medicaid_Fraud_Cases_Dataset.csv'), index=False)

# 2. Create Revalidation/Disenrollment Dataset
revalidation_data = {
    "Metric": [
        "Total High-Risk Providers Reviewed",
        "Providers Disenrolled (Failed Revalidation)",
        "Providers Approved",
        "Disenrolled: Failed Background Study",
        "Disenrolled: Failed Site Visit",
        "Disenrolled: Incomplete/Inaccurate Data",
        "Appeals Filed",
        "Inactive Providers Terminated (Oct 2025)",
        "Inactive Providers Terminated (Oct 2025-Mar 2026)",
        "Providers Referred to DHS OIG (from 3,411)"
    ],
    "Value": [
        "~5,583",
        "3,411",
        "2,061",
        "2",
        "916",
        "2,491",
        "2,055",
        "761",
        "18,109",
        "59"
    ],
    "Source": [
        "DHS PI Page / Fact Check",
        "DHS Fact Check (6/9/26)",
        "DHS PI Page",
        "DHS PI Page",
        "DHS PI Page",
        "DHS PI Page",
        "DHS Fact Check (6/9/26)",
        "DHS PI Page",
        "DHS PI Page",
        "DHS PI Page"
    ]
}

df_reval = pd.DataFrame(revalidation_data)
df_reval.to_csv(_os.path.join(OUT_DIR, 'MN_Medicaid_Revalidation_Data.csv'), index=False)

# 3. Create Program Growth Dataset
growth_data = [
    {"Program": "Housing Stabilization Services (HSS)", "Year": 2021, "Spending": "$21M - $26M", "Source": "DOJ / IRS-CI"},
    {"Program": "Housing Stabilization Services (HSS)", "Year": 2022, "Spending": "$42M", "Source": "DOJ / IRS-CI"},
    {"Program": "Housing Stabilization Services (HSS)", "Year": 2023, "Spending": "$74M", "Source": "DOJ / IRS-CI"},
    {"Program": "Housing Stabilization Services (HSS)", "Year": 2024, "Spending": "$104M", "Source": "DOJ / IRS-CI"},
    {"Program": "Housing Stabilization Services (HSS)", "Year": "2025 (first 6 mo)", "Spending": "$61M", "Source": "DOJ / IRS-CI"},
    {"Program": "EIDBI (Autism)", "Year": 2018, "Spending": "$600,000", "Source": "DOJ May 2026"},
    {"Program": "EIDBI (Autism)", "Year": 2025, "Spending": ">$400M", "Source": "DOJ May 2026"},
    {"Program": "Integrated Community Supports (ICS)", "Year": 2021, "Spending": "$4.2M", "Source": "DOJ May 2026"},
    {"Program": "Integrated Community Supports (ICS)", "Year": 2024, "Spending": "$170M", "Source": "IRS-CI Dec 2025"},
    {"Program": "Integrated Community Supports (ICS)", "Year": 2025, "Spending": ">$183M", "Source": "DOJ May 2026"},
    {"Program": "Individualized Home Supports (IHS)", "Year": 2018, "Spending": ">$100M", "Source": "DOJ May 2026"},
    {"Program": "Individualized Home Supports (IHS)", "Year": 2025, "Spending": ">$700M", "Source": "DOJ May 2026"}
]

df_growth = pd.DataFrame(growth_data)
df_growth.to_csv(_os.path.join(OUT_DIR, 'MN_Medicaid_Program_Growth_Data.csv'), index=False)

print("Datasets created successfully in " + _BASE + "/deliverables/")
