
import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

d = _os.path.join(OUT_DIR, '')
cases = pd.read_csv(d+'MN_Medicaid_Fraud_Cases_Dataset.csv')
reval = pd.read_csv(d+'MN_Medicaid_Revalidation_Data.csv')
growth = pd.read_csv(d+'MN_Medicaid_Program_Growth_Data.csv')

# High-risk categories table
highrisk = pd.DataFrame({
    "High_Risk_Service_Type": [
        "Adult Companion Services","Adult Day Services","Adult Rehabilitative Mental Health Services (ARMHS)",
        "Assertive Community Treatment (ACT)","Community First Services and Supports (CFSS)",
        "Early Intensive Developmental and Behavioral Intervention (EIDBI)","Housing Stabilization Services (HSS)",
        "Individualized Home Supports (IHS)","Integrated Community Supports (ICS)","Intensive Residential Treatment Services (IRTS)",
        "Night Supervision Services","Nonemergency Medical Transportation (NEMT)","Recovery Peer Support","Recuperative Care"
    ],
    "Designation_Wave": ["Oct 2025 (9 more)","Oct 2025","Oct 2025","Oct 2025","Oct 2025","May 2025 (first)","May 2025 (first)",
        "Oct 2025","Oct 2025","Oct 2025","Oct 2025","Oct 2025","Oct 2025","Oct 2025"]
})

# Build Excel workbook
with pd.ExcelWriter(d+'MN_Medicaid_Master_Evidence_Base.xlsx', engine='openpyxl') as xw:
    pd.DataFrame({"Minnesota Medicaid Program Integrity Evidence Base":[
        "Compiled by Mohamed Noor Hussein | June 2026",
        "All data from official/public sources (DOJ, IRS-CI, MN AG/MFCU, MN DHS, MN OLA, CMS, HHS-OIG).",
        "EVIDENTIARY NOTE: 'Charged'/'alleged' cases are accusations only; defendants presumed innocent.",
        "Tabs: High-Risk Categories | Enforcement Cases | Revalidation Data | Program Growth"
    ]}).to_excel(xw, sheet_name='README', index=False)
    highrisk.to_excel(xw, sheet_name='High-Risk Categories', index=False)
    cases.to_excel(xw, sheet_name='Enforcement Cases', index=False)
    reval.to_excel(xw, sheet_name='Revalidation Data', index=False)
    growth.to_excel(xw, sheet_name='Program Growth', index=False)
print("Excel workbook created.")

# Chart: HSS growth
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10,6))
years = ['Predicted','2021','2022','2023','2024','2025*']
vals = [2.6, 26, 42, 74, 104, 122]  # 2025 first 6mo $61M annualized ~122
bars = ax.bar(years, vals, color=['#888888','#4878CF','#4878CF','#EE854A','#EE854A','#C44E52'])
ax.set_title('Minnesota Housing Stabilization Services Spending Growth:\nProjected vs. Actual Claims Paid', fontsize=14, fontweight='bold')
ax.set_ylabel('Claims Paid (USD Millions)', fontsize=12)
ax.set_xlabel('Year (*2025 annualized from $61M in first 6 months)', fontsize=10)
for b,v in zip(bars,vals):
    ax.text(b.get_x()+b.get_width()/2, v+2, f'${v}M', ha='center', fontweight='bold', fontsize=10)
ax.annotate('DHS predicted ~$2.6M/yr', xy=(0,2.6), xytext=(0.5,55),
            arrowprops=dict(arrowstyle='->',color='red'), fontsize=10, color='red')
plt.tight_layout()
plt.savefig(d+'HSS_Spending_Growth_Chart.png', dpi=150, bbox_inches='tight')
print("Chart created.")
