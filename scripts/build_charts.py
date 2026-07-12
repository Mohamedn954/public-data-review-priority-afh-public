import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.family"]="DejaVu Sans"
DATA = DATA_DIR + "/"; DEL = OUT_DIR + "/"
import os; os.makedirs(DEL,exist_ok=True)

# ---- Chart 1: WA LTC spending growth by biennium ------------------------
#
# Source series: `wa_data_aggregate/WA_LTC_Spending_Biennia.csv`.
# The CSV carries per-biennium values, appropriation level (enacted /
# approximate / proposed), source citation, source URL, access date, and
# confidence level. See the CSV for exact provenance of each value.
#
# Summary of provenance at time of writing:
#   * 2013-15 through 2021-23  -- Washington Research Council PB 21-08 (2021),
#                                 Chart 1, All Funds series (High confidence).
#   * 2023-25                  -- OFM Agency Recommendation Summary, DSHS
#                                 Long Term Care (unit 050), "Current Budget
#                                 (2023-25 Original)" line: $10.44B (High
#                                 confidence; W1 resolved). The same OFM page
#                                 also shows a post-supplemental maintenance
#                                 level of $10.50B and a 2024 policy-level
#                                 total of $10.53B; $10.44B (originally
#                                 enacted) is used for consistency with the
#                                 as-originally-enacted basis of the other rows.
#   * 2025-27                  -- Governor's PROPOSED level ($13.07B, OFM
#                                 Agency Recommendation Summary). DSHS
#                                 separately reports an enacted 2025-27
#                                 figure of ~$12.9B (Center Square 2025);
#                                 the ~$0.17B gap is proposed-vs-enacted.
# -----------------------------------------------------------------------

# Locate the biennial-spending CSV in wa_data_aggregate/. Search both the
# repo root layout (public repo) and the data-package layout (private repo).
def _find_ltc_csv():
    _repo_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    for candidate in [
        _os.path.join(_repo_root, "wa_data_aggregate", "WA_LTC_Spending_Biennia.csv"),
        _os.path.join(_BASE, "wa_data_aggregate", "WA_LTC_Spending_Biennia.csv"),
        _os.path.join(_BASE, "data_package_with_everything", "wa_data",
                      "WA_LTC_Spending_Biennia.csv"),
    ]:
        if _os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError(
        "WA_LTC_Spending_Biennia.csv not found. Expected under "
        "wa_data_aggregate/ (public repo) or data_package_with_everything/wa_data/ "
        "(private repo)."
    )

ltc_df = pd.read_csv(_find_ltc_csv())
# Preserve CSV row order for display order on the chart.
biennia = ltc_df["biennium"].tolist()
ltc = ltc_df["all_funds_billions"].astype(float).tolist()

# Mark the last biennium with an asterisk to indicate proposed-not-enacted,
# matching the CSV's appropriation_level field.
_display_biennia = [
    (b + "*") if str(lvl).strip().lower() == "proposed" else b
    for b, lvl in zip(biennia, ltc_df["appropriation_level"].tolist())
]

# Color bars by appropriation level so proposed / approximate values are
# visually distinct from enacted, verified values. All three categories are
# defined even when the current CSV has no "approximate" row, so the palette
# stays correct if a future biennium is entered with that classification.
_level_color = {
    "enacted": "#2c6e9c",       # solid blue for verified enacted
    "approximate": "#e67e22",   # orange for uncorroborated / low-confidence
    "proposed": "#c0392b",      # red for proposed / not-yet-enacted
}
_bar_colors = [
    _level_color.get(str(lvl).strip().lower(), "#888888")
    for lvl in ltc_df["appropriation_level"].tolist()
]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(_display_biennia, ltc, color=_bar_colors)
ax.set_ylabel("Long-Term Care Total Funds ($ Billions)")
ax.set_title(
    "Washington DSHS Long-Term Care Spending Growth by Biennium",
    fontsize=11,
)
for b, v in zip(bars, ltc):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.15, f"${v}B",
            ha="center", fontsize=9)

# Legend
from matplotlib.patches import Patch
_legend_handles = [
    Patch(color="#2c6e9c", label="Enacted (verified)"),
    Patch(color="#e67e22", label="Approximate / uncorroborated"),
    Patch(color="#c0392b", label="Proposed (not enacted)"),
]
ax.legend(handles=_legend_handles, loc="upper left", fontsize=8, framealpha=0.9)

ax.text(
    0.01, -0.24,
    "2013-15 to 2021-23: Washington Research Council (PB 21-08, 2021), Chart 1, All Funds.\n"
    "2023-25: OFM Agency Recommendation Summary, DSHS Long Term Care (unit 050), originally-enacted total.\n"
    "*2025-27 is the OFM Governor's proposed (not enacted) level, \\$13.07B; DSHS separately reports an enacted 2025-27\n"
    "figure of approximately \\$12.9B (The Center Square, 2025). See wa_data_aggregate/WA_LTC_Spending_Biennia.csv.",
    transform=ax.transAxes, fontsize=7, color="#555",
)
plt.tight_layout()
plt.savefig(DEL + "WA_LTC_Spending_Growth.png", dpi=140, bbox_inches="tight")
plt.close(fig)
print("saved spending chart")

# ---- Chart 2: County concentration + enforcement --------------------------
ct=pd.read_csv(DATA+"WA_County_Concentration.csv")
fig,(a1,a2)=plt.subplots(1,2,figsize=(13,5.5))
a1.bar(ct["County"],ct["facilities"],color=["#2c6e9c","#27ae60","#e67e22"])
a1.set_title("Licensed Adult Family Homes by County")
a1.set_ylabel("Number of AFHs")
for i,v in enumerate(ct["facilities"]): a1.text(i,v+15,f"{int(v)}",ha="center")
x=np.arange(len(ct)); w=0.38
a2.bar(x-w/2,ct["enforcement_rate_pct"],w,label="Enforcement rate %",color="#c0392b")
a2.bar(x+w/2,ct["investigation_rate_pct"],w,label="Investigation rate %",color="#f39c12")
a2.set_xticks(x); a2.set_xticklabels(ct["County"])
a2.set_title("Enforcement & Investigation Rates by County (2023-2026)")
a2.set_ylabel("% of facilities"); a2.legend()
plt.tight_layout()
plt.savefig(DEL+"WA_County_Concentration_Enforcement.png",dpi=140,bbox_inches="tight")
plt.close(fig)
print("saved county chart")

# ---- Top operator clusters w/ enforcement ---------------------------------
cl=pd.read_csv(DATA+"WA_Operator_PhoneClusters.csv")
cl["risk"]=cl["total_enforcement"]+cl["total_investigations"]+cl["total_civil_fines"]
top=cl.sort_values(["n_licenses","risk"],ascending=False).head(12)
print("\n=== TOP OPERATOR CLUSTERS ===")
print(top[["n_licenses","counties","total_enforcement","total_investigations","total_civil_fines","facilities"]].to_string())
