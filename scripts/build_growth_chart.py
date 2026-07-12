import os as _os
_BASE = _os.environ.get("AFH_PROJECT_ROOT", _os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))
_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"]="DejaVu Sans"
years=list(range(2013,2027))
# official=solid, estimate=hollow
vals={2013:2842,2014:2772,2015:2750,2016:2768,2017:2780,2018:2806,2019:2900,2020:3300,2021:3800,2022:4315,2023:4315,2024:4960,2025:5400,2026:6075}
est_years={2019,2020,2021,2025}  # true interpolations only; 2026 is the actual current-roster snapshot (Medium confidence), not an interpolation
fig,ax=plt.subplots(figsize=(11,5.8))
y=[vals[t] for t in years]
ax.plot(years,y,"-",color="#2c6e9c",lw=2,zorder=1)
for t in years:
    if t in est_years:
        ax.plot(t,vals[t],"o",mfc="white",mec="#c0392b",mew=1.8,ms=8,zorder=2)
    else:
        ax.plot(t,vals[t],"o",color="#2c6e9c",ms=8,zorder=2)
ax.axvspan(2012.5,2018.5,alpha=0.07,color="gray")
ax.text(2015.5,2600,"Flat / stagnant era\n(~2,750-2,890)",ha="center",fontsize=9,color="#555")
ax.annotate("Post-2018 surge",xy=(2022,4315),xytext=(2019.3,5200),fontsize=10,color="#c0392b",
            arrowprops=dict(arrowstyle="->",color="#c0392b"))
ax.set_title("Washington Licensed Adult Family Homes, 2013-2026\nSolid = official DSHS figures; hollow red = reconstructed estimates",fontsize=12)
ax.set_ylabel("Number of Licensed AFHs"); ax.set_xlabel("Year")
ax.set_ylim(2400,6500); ax.grid(alpha=0.25)
for t in [2013,2018,2022,2024,2026]:
    ax.text(t,vals[t]+120,f"{vals[t]:,}",ha="center",fontsize=8.5)
ax.text(0.01,-0.15,"Sources: DSHS BERK AFH Payment Methodology 2018 (2009-2018); DSHS RDA/Mancuso decks (2022-2024); DSHS ArcGIS roster (2026). 2019-2021 & 2025 interpolated.",
        transform=ax.transAxes,fontsize=7,color="#666")
plt.tight_layout()
plt.savefig(_os.path.join(OUT_DIR, "WA_AFH_Growth_2013_2026.png"),dpi=140,bbox_inches="tight")
print("growth chart saved")
