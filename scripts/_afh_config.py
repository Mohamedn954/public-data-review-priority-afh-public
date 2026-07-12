"""Shared configuration for the WA AFH analysis pipeline.

Every script in this directory reads its snapshot date and standard output
paths from here rather than hardcoding literal strings, so that a future
re-run of the pipeline can be relabeled with a new snapshot date by setting
a single environment variable (AFH_DATE_ACCESSED) or editing this file
once, rather than by grepping and hand-editing every script.

Public repo note: this file is imported by pipeline scripts but is not
required to run the two supported public-repo actions (verify_headline_numbers.py
and build_phase1_dashboard_data.py), both of which use only the Python
standard library and do not depend on a snapshot date.
"""

import os as _os

# ---------------------------------------------------------------------------
# Snapshot date (single source of truth for the whole pipeline)
# ---------------------------------------------------------------------------
# The manuscript reports figures anchored on the state's public data as of
# this date. Override via AFH_DATE_ACCESSED for a future re-run.
DATE_ACCESSED = _os.environ.get("AFH_DATE_ACCESSED", "2026-06-26")

# ---------------------------------------------------------------------------
# Standard project paths (overridable via env vars)
# ---------------------------------------------------------------------------
# Resolve relative to the script's own folder by default, so the pipeline
# is portable across checkouts.
_BASE = _os.environ.get(
    "AFH_PROJECT_ROOT",
    _os.path.dirname(_os.path.abspath(__file__)),
)
DATA_DIR = _os.environ.get("AFH_DATA_DIR", _os.path.join(_BASE, "data"))
OUT_DIR  = _os.environ.get("AFH_OUT_DIR",  _os.path.join(_BASE, "deliverables"))
SRC_DIR  = _os.environ.get("AFH_SRC_DIR",  _os.path.join(_BASE, "sources"))

_os.makedirs(DATA_DIR, exist_ok=True)
_os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Standard source strings
# ---------------------------------------------------------------------------
# IMPORTANT DISTINCTION:
#   - SRC_BERK / SRC_MAN23 / SRC_MAN24 cite specific historical third-party
#     documents (a 2018 BERK report, 2022/2024 Mancuso decks). The date those
#     documents were looked up is a fixed historical fact and must NOT move
#     just because this pipeline is rerun later with a different
#     AFH_DATE_ACCESSED — the researcher would not have re-accessed a 2018
#     PDF on some future rerun date. These three keep their own fixed access
#     date, independent of DATE_ACCESSED.
#   - SRC_ARC / SRC_ENFORCEMENT_SCRAPE / SRC_CENSUS describe THIS pipeline's
#     own live pulls (the current ArcGIS roster, the current RCS scrape, the
#     current Census API call) and correctly move with DATE_ACCESSED, since
#     rerunning the pipeline on a new date really does mean those sources
#     were re-accessed on that new date.
_HISTORICAL_ACCESS_DATE = "2026-06-26"  # fixed; do not tie to AFH_DATE_ACCESSED

SRC_BERK = (
    "DSHS AFH Payment Methodology Analysis (BERK), 2.23.2018 (Table 3.1/3.4); "
    "https://www.dshs.wa.gov/sites/default/files/ALTSA/msd/documents/"
    "WA%20Adult%20Family%20Homes%20Payment%20Methodology%20Analysis%20-%202.23.2018.docx; "
    f"accessed {_HISTORICAL_ACCESS_DATE}"
)
SRC_MAN23 = (
    "DSHS RDA / Mancuso Senior Lobby 2023 deck (DSHS Enterprise GIS "
    "Geospatial Data Library, accessed Aug 25 2022); "
    "https://waseniorlobby.org/wp-content/uploads/Mancuso-SeniorLobby-2023-2.pdf; "
    f"accessed {_HISTORICAL_ACCESS_DATE}"
)
SRC_MAN24 = (
    "DSHS RDA / Mancuso 2024 deck (DSHS Enterprise GIS Geospatial Data "
    "Library, Aug 14 2024); "
    "https://waseniorlobby.org/wp-content/uploads/MANCUSO-DSHS-Research-and-Data-Analysis.pdf; "
    f"accessed {_HISTORICAL_ACCESS_DATE}"
)
SRC_ARC = (
    "DSHS ArcGIS 'Long Term Care - Residential Care' feature service "
    f"(current roster, deduped by license); accessed {DATE_ACCESSED}"
)
SRC_ENFORCEMENT_SCRAPE = (
    f"DSHS RCS public reports portal (AFHForms.aspx), scraped {DATE_ACCESSED}"
)
SRC_CENSUS = (
    "U.S. Census Bureau ACS 5-year (B01001) via Census Reporter API; "
    f"accessed {DATE_ACCESSED}"
)
