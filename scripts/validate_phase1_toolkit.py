#!/usr/bin/env python3
"""Validate the Phase 1 Public-Data Review-Priority Toolkit's generated outputs.

Checks that the dashboard JSON/HTML exist, that tier and county totals
reconcile against the total facility count, that no facility-identifying
detail or prohibited language appears anywhere in the outputs, and that the
dashboard makes no external network calls of any kind.

Prints a PASS/FAIL line per check and exits non-zero if anything fails.

Usage: python3 validate_phase1_toolkit.py [path-to-repo-root]
"""
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
)
DASHBOARD_DIR = os.path.join(ROOT, "dashboard")
DATA_PATH = os.path.join(DASHBOARD_DIR, "phase1_dashboard_data.json")
HTML_PATH = os.path.join(DASHBOARD_DIR, "phase1-dashboard.html")

# Prohibited terms — flagged unless they appear as part of an approved
# guardrail negation (e.g. "not a fraud score", "not a validated risk model").
PROHIBITED_TERMS = [
    "fraud risk",
    "risk score",
    "validated risk model",
    "provider ranking",
    "facility ranking",
]
GUARDRAIL_PREFIXES = [
    "not a ", "not an ", "isn't a ", "isn't an ",
    "is not a ", "is not an ", "does not create a ", "does not create an ",
]

# No external calls of any kind in the static dashboard.
FORBIDDEN_CALLS = ["fetch(", "XMLHttpRequest", "WebSocket"]

# facility_id format is F##### (e.g. F00001); cluster_id format is OP### (e.g.
# OP001) — cluster_id is an aggregate grouping key, not a facility identifier,
# and is not checked for. Only facility_id-shaped tokens are treated as a leak.
FACILITY_ID_PATTERN = re.compile(r"\bF\d{5}\b")

results = []


def check(label, passed, detail=""):
    results.append((label, passed, detail))
    status = "PASS" if passed else "FAIL"
    line = f"[{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)


def find_prohibited(text):
    hits = []
    lower = text.lower()
    for term in PROHIBITED_TERMS:
        start = 0
        while True:
            idx = lower.find(term, start)
            if idx == -1:
                break
            preceding = lower[max(0, idx - 25):idx]
            if any(preceding.endswith(prefix) for prefix in GUARDRAIL_PREFIXES):
                pass  # approved guardrail usage
            else:
                hits.append((term, text[max(0, idx - 40):idx + len(term) + 10]))
            start = idx + len(term)
    return hits


def find_external_refs(html):
    refs = re.findall(r'(?:src|href)\s*=\s*["\'](https?:)?//[^"\']+["\']', html)
    return refs


def main():
    data_exists = os.path.isfile(DATA_PATH)
    check("dashboard/phase1_dashboard_data.json exists", data_exists, DATA_PATH)

    html_exists = os.path.isfile(HTML_PATH)
    check("dashboard/phase1-dashboard.html exists", html_exists, HTML_PATH)

    if not (data_exists and html_exists):
        print("\nCannot continue — required file(s) missing.")
        return 1

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    with open(HTML_PATH, encoding="utf-8") as f:
        html = f.read()

    total = data["headline"]["total_facilities"]

    tier_total = sum(t["facilities"] for t in data["review_priority_tiers"])
    check("Default tier totals equal total facility count",
          tier_total == total, f"tiers sum={tier_total}, total={total}")

    county_total = sum(c["facilities"] for c in data["county_summary"])
    check("County totals equal total facility count",
          county_total == total, f"counties sum={county_total}, total={total}")

    cube_total = sum(cell["facilities"] for cell in data.get("sensitivity_cube", []))
    check("Sensitivity cube totals equal total facility count",
          cube_total == total, f"cube sum={cube_total}, total={total}")

    data_json_text = json.dumps(data)
    combined_text_for_id_scan = data_json_text + html
    id_hits = FACILITY_ID_PATTERN.findall(combined_text_for_id_scan)
    check("No facility IDs (F##### pattern) in dashboard JSON or HTML",
          len(id_hits) == 0, f"found: {sorted(set(id_hits))}" if id_hits else "")

    # Field-name leak check: look for the literal source-column names that would
    # only appear if raw identifying columns were accidentally serialized, in
    # the actual JSON text (nested, not just top-level keys/values).
    raw_column_leaks = [c for c in ["Facility_Name", "License_Number", "phone_number",
                                     "Latitude", "Longitude", "ZIP_Code", "\"City\""]
                         if c in data_json_text]
    check("No raw identifying column names embedded in dashboard JSON",
          len(raw_column_leaks) == 0, f"found: {raw_column_leaks}" if raw_column_leaks else "")

    prohibited_hits = find_prohibited(html) + find_prohibited(json.dumps(data))
    check("No prohibited terms outside approved guardrail language",
          len(prohibited_hits) == 0,
          "; ".join(f"'{t}' near: ...{ctx}..." for t, ctx in prohibited_hits[:5]) if prohibited_hits else "")

    forbidden_call_hits = [c for c in FORBIDDEN_CALLS if c in html]
    check("Dashboard HTML contains no fetch()/XMLHttpRequest/WebSocket calls",
          len(forbidden_call_hits) == 0, f"found: {forbidden_call_hits}" if forbidden_call_hits else "")

    external_refs = find_external_refs(html)
    check("Dashboard HTML has no external script/stylesheet/network references",
          len(external_refs) == 0, f"found: {external_refs}" if external_refs else "")

    print()
    passed = sum(1 for _, ok, _ in results if ok)
    failed = len(results) - passed
    if failed == 0:
        print(f"ALL {passed} CHECKS PASSED.")
        return 0
    else:
        print(f"{failed} of {len(results)} CHECKS FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
