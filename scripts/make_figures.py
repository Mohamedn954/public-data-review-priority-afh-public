#!/usr/bin/env python3
"""Render Figure 4 (Public-Data Review-Priority Framework) and Figure 5 (Two-Phase Model)
as clean, journal-style conceptual diagrams using matplotlib."""

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
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = _os.path.join(OUT_DIR, "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"

# Muted, professional palette
PUBLIC = "#2f5d8a"      # public-data (blue)
PUBLIC_L = "#dbe6f1"
CLAIMS = "#7a5230"      # claims-data (brown)
CLAIMS_L = "#ece1d4"
FUSION = "#4a6b4d"      # fusion (green)
FUSION_L = "#dde8de"
GREY = "#444444"

def rbox(ax, x, y, w, h, text, fc, ec, fontsize=9, fontweight="normal", tc="#1a1a1a"):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                         linewidth=1.3, edgecolor=ec, facecolor=fc)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, color=tc, wrap=True)

def arrow(ax, x1, y1, x2, y2, color=GREY, style="-|>", lw=1.6, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle="arc3,rad=0")
    ax.add_patch(a)

# FIGURE 4 — Public-Data Review-Priority Framework: Public Signals + Claims-Informed Expansion
fig, ax = plt.subplots(figsize=(11, 7.2))
ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")

ax.text(6, 9.55, "Figure 4. Public-Data Review-Priority Framework",
        ha="center", fontsize=14, fontweight="bold", color="#1a1a1a")
ax.text(6, 9.12, "Public review-priority signals (testable now) and the claims-informed expansion path (requires agency data)",
        ha="center", fontsize=9.5, color=GREY, style="italic")

# Left column: PUBLIC-DATA SIGNALS (testable now)
ax.text(3.0, 8.45, "PUBLIC-DATA SIGNALS  (review-priority indicators, testable now)",
        ha="center", fontsize=9.5, fontweight="bold", color=PUBLIC)
public_items = [
    "Facility / operator growth over time  (RF-01)",
    "Operator concentration: shared phone / agent  (RF-03, RF-08)",
    "Geographic density of facilities  (RF-04)",
    "Enforcement intensity & sanction history  (RF-17)",
    "Complaint / investigation load  (RF-16)",
    "Exclusion-list linkage gaps  (RF-06)",
]
y = 7.95
for it in public_items:
    rbox(ax, 0.5, y-0.50, 5.0, 0.46, it, PUBLIC_L, PUBLIC, fontsize=8.4)
    y -= 0.62

# Right column: CLAIMS-DATA SIGNALS (requires agency data)
ax.text(9.0, 8.45, "CLAIMS-DATA SIGNALS  (require internal agency data)",
        ha="center", fontsize=9.5, fontweight="bold", color=CLAIMS)
claims_items = [
    "Impossible / overlapping service hours  (RF-10)",
    "Maximum-unit or implausible volume  (RF-11)",
    "Out-of-state / impossible-location billing  (RF-12)",
    "Billing after death, absence, discharge  (RF-13)",
    "Cloned or fabricated documentation  (RF-14)",
    "Stolen credentials / unauthorized IDs  (RF-15)",
]
y = 7.95
for it in claims_items:
    rbox(ax, 6.5, y-0.50, 5.0, 0.46, it, CLAIMS_L, CLAIMS, fontsize=8.4)
    y -= 0.62

# Fusion box at bottom
rbox(ax, 2.0, 0.55, 8.0, 1.15,
     "FUSED REVIEW-PRIORITY OUTPUT\nPublic-Data Review-Priority Tier (PDRT)  +  internal claims validation\n\u2192 review-priority triage, subject to human review and due process (not a fraud determination)",
     FUSION_L, FUSION, fontsize=9.0, fontweight="bold", tc="#1a1a1a")

# Arrows into fusion
arrow(ax, 2.6, 4.05, 4.0, 1.75, color=PUBLIC, lw=1.8)
arrow(ax, 9.4, 4.05, 8.0, 1.75, color=CLAIMS, lw=1.8, ls=(0,(5,2)))

# Divider note (placed in the open band below the columns, above the fusion box)
ax.text(6, 3.55, "This study operationalizes the LEFT column only.\nThe RIGHT column requires a ProviderOne / claims data-use agreement (claims-informed expansion).",
        ha="center", fontsize=8.8, color=GREY, style="italic")

ax.text(6, 0.15,
        "Figure shows the conceptual architecture only. It does not show actual billing data and is not a fraud-detection model.",
        ha="center", fontsize=8, color=GREY)

plt.tight_layout()
fig.savefig(f"{OUT}/Fig4_Framework.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Figure 4 saved")

# FIGURE 5 — Two-Phase Model: Public-Data Review Priority -> Internal Claims Validation
fig, ax = plt.subplots(figsize=(11, 6.4))
ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis("off")

ax.text(6, 8.5, "Figure 5. Two-Phase Model for Public-Data Review Priority",
        ha="center", fontsize=14, fontweight="bold", color="#1a1a1a")
ax.text(6, 8.08, "Phase 1 prioritizes review using public data; Phase 2 validates with internal claims data before any action",
        ha="center", fontsize=9.5, color=GREY, style="italic")

# PHASE 1 panel
rbox(ax, 0.4, 4.3, 5.2, 3.1, "", PUBLIC_L, PUBLIC)
ax.text(3.0, 7.05, "PHASE 1 — PUBLIC-DATA REVIEW PRIORITY", ha="center",
        fontsize=10, fontweight="bold", color=PUBLIC)
p1 = ("Inputs: licensing rosters, enforcement / complaint\n"
      "records, operator-contact clustering, facility density\n\n"
      "Output: Public-Data Review-Priority Tier (PDRT)\n"
      "  \u2022 Baseline monitoring\n"
      "  \u2022 Moderate review priority\n"
      "  \u2022 High review priority\n\n"
      "Purpose: prioritize where to look \u2014 not a finding")
ax.text(3.0, 5.55, p1, ha="center", va="center", fontsize=8.5, color="#1a1a1a")

# PHASE 2 panel
rbox(ax, 6.4, 4.3, 5.2, 3.1, "", CLAIMS_L, CLAIMS)
ax.text(9.0, 7.05, "PHASE 2 — INTERNAL CLAIMS VALIDATION", ha="center",
        fontsize=10, fontweight="bold", color=CLAIMS)
p2 = ("Inputs (restricted): ProviderOne claims, service\n"
      "hours, dates, recipient eligibility, EVV records\n\n"
      "Tests: impossible hours, max-unit billing, billing\n"
      "after death/discharge, documentation integrity\n\n"
      "Output: confirmed billing irregularity? \u2192 case\n"
      "review under agency policy & due process")
ax.text(9.0, 5.55, p2, ha="center", va="center", fontsize=8.5, color="#1a1a1a")

# Arrow phase1 -> phase2
arrow(ax, 5.65, 5.85, 6.35, 5.85, color=GREY, lw=2.0)
ax.text(6.0, 6.15, "high-priority\ncases only", ha="center", fontsize=7.6, color=GREY)

# Gate note between
ax.text(6.0, 3.95, "Gate: no sanction or fraud determination at Phase 1; human review required throughout",
        ha="center", fontsize=8.6, color="#8a2f2f", fontweight="bold")

# Bottom outcome bar
rbox(ax, 1.5, 1.5, 9.0, 1.2,
     "PRESERVES PROVIDER DUE PROCESS\nPublic-data prioritization improves audit efficiency; confirmation of billing irregularities\nrequires internal claims data and established enforcement procedures.",
     FUSION_L, FUSION, fontsize=8.8, fontweight="bold")

arrow(ax, 3.0, 4.25, 4.0, 2.75, color=PUBLIC, lw=1.5)
arrow(ax, 9.0, 4.25, 8.0, 2.75, color=CLAIMS, lw=1.5, ls=(0,(5,2)))

ax.text(6, 0.9,
        "Figure presents the conceptual workflow only; it does not depict real cases and is not a fraud-detection system.",
        ha="center", fontsize=8, color=GREY)

plt.tight_layout()
fig.savefig(f"{OUT}/Fig5_TwoPhase.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("Figure 5 saved")
