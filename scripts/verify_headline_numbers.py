#!/usr/bin/env python3
"""Verify the manuscript's headline aggregate numbers against the public,
de-identified anonymized_data/ package alone (no private-repo files needed).

This does not re-run the analysis pipeline (see README_SCRIPTS.md /
REPRODUCIBILITY_CHECK.md for why the pipeline scripts require non-public
intermediate files). It only checks that the numbers reported in the
manuscript are present in the data actually shipped in this public repo.

Usage: python3 verify_headline_numbers.py [path-to-anonymized_data-dir]
"""
import csv
import os
import sys

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "anonymized_data"
)

EXPECTED = {
    "facilities": 3457,
    "beds": 20157,
    "king": 1795,
    "pierce": 1052,
    "spokane": 610,
    "enforcement_gt0": 165,
    "investigations_gt0": 586,
    "clustered": 164,
    "clusters": 72,
    "clusters_3plus": 15,
    "max_cluster_size": 4,
}

failures = []


def check(label, actual, expected):
    status = "OK" if actual == expected else "MISMATCH"
    if actual != expected:
        failures.append(label)
    print(f"  {label}: {actual} (expect {expected}) [{status}]")


def read_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


print(f"Reading anonymized data from: {os.path.abspath(DATA_DIR)}\n")

facilities = read_csv("WA_AFH_3County_Enriched_ANON.csv")
print("=== WA_AFH_3County_Enriched_ANON.csv ===")
check("facilities", len(facilities), EXPECTED["facilities"])
check("beds", sum(int(r["Licensed_Capacity"]) for r in facilities), EXPECTED["beds"])

county_counts = {}
for r in facilities:
    county_counts[r["County"]] = county_counts.get(r["County"], 0) + 1
check("King County facilities", county_counts.get("King", 0), EXPECTED["king"])
check("Pierce County facilities", county_counts.get("Pierce", 0), EXPECTED["pierce"])
check("Spokane County facilities", county_counts.get("Spokane", 0), EXPECTED["spokane"])

enforcement_gt0 = sum(1 for r in facilities if int(r["n_enforcement"]) > 0)
investigations_gt0 = sum(1 for r in facilities if int(r["n_investigations"]) > 0)
check("Facilities with >=1 enforcement action", enforcement_gt0, EXPECTED["enforcement_gt0"])
check("Facilities with >=1 investigation", investigations_gt0, EXPECTED["investigations_gt0"])

clustered = sum(1 for r in facilities if r["cluster_id"].strip())
check("Facilities in an operator cluster", clustered, EXPECTED["clustered"])

print("\n=== WA_Operator_Clusters_ANON.csv ===")
clusters = read_csv("WA_Operator_Clusters_ANON.csv")
check("Operator clusters", len(clusters), EXPECTED["clusters"])
clusters_3plus = sum(1 for r in clusters if int(r["n_licenses"]) >= 3)
check("Clusters with >=3 licenses", clusters_3plus, EXPECTED["clusters_3plus"])
max_size = max(int(r["n_licenses"]) for r in clusters)
check("Largest cluster size", max_size, EXPECTED["max_cluster_size"])

print("\n=== WA_Operator_Clusters_Corroboration_ANON.csv ===")
corrob = read_csv("WA_Operator_Clusters_Corroboration_ANON.csv")
corroborated = sum(1 for r in corrob if r["corroboration_status"] == "Corroborated")
print(f"  Rows: {len(corrob)} | Corroborated: {corroborated} "
      f"({corroborated / len(corrob):.1%})")

print()
if failures:
    print(f"FAILED: {len(failures)} check(s) did not match: {', '.join(failures)}")
    sys.exit(1)
print("All headline numbers verified against the public anonymized data package.")
