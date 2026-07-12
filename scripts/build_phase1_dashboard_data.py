#!/usr/bin/env python3
"""Build aggregate-only dashboard data for the Phase 1 Public-Data Review-Priority
Toolkit from the repo's public, de-identified anonymized_data/ files.

Reads only de-identified fields and writes only aggregate counts, rates, and
distributions. No facility name, address, license number, phone number, URL,
city, ZIP, latitude/longitude, or other provider-identifying field is read or
written anywhere in this script.

This is an illustrative sensitivity-analysis tool, not a validated model, fraud
score, or enforcement tool. See PHASE1_PUBLIC_DATA_FRAMEWORK.md for the
qualitative tier definitions and guardrails this script implements, and
README_ANONYMIZED_DATA.md for what the source files do and do not contain.

Usage: python3 build_phase1_dashboard_data.py [path-to-repo-root]
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
)

# Default thresholds — must match dashboard/phase1_tier_config.json and
# PHASE1_PUBLIC_DATA_FRAMEWORK.md exactly. All illustrative, non-validated.
DEFAULT_CLUSTER_SIZE_THRESHOLD = 3   # Network Concentration
DEFAULT_ENFORCEMENT_THRESHOLD = 2    # Enforcement Intensity
DEFAULT_INVESTIGATION_THRESHOLD = 3  # Complaint Load

ALLOWED_CLUSTER_SIZE_THRESHOLDS = [2, 3, 4]
ALLOWED_ENFORCEMENT_THRESHOLDS = [1, 2, 3]
ALLOWED_INVESTIGATION_THRESHOLDS = [1, 2, 3]

# Buckets cap at the highest allowed threshold in each dimension: a bucket value
# of N means "exactly N" for N below the cap, and "N or more" at the cap. This
# is sufficient to recompute any threshold in ALLOWED_*_THRESHOLDS client-side
# from aggregate counts alone, with no facility-level row ever shipped.
CLUSTER_BUCKET_CAP = max(ALLOWED_CLUSTER_SIZE_THRESHOLDS)       # 4
ENFORCEMENT_BUCKET_CAP = max(ALLOWED_ENFORCEMENT_THRESHOLDS)    # 3
INVESTIGATION_BUCKET_CAP = max(ALLOWED_INVESTIGATION_THRESHOLDS)  # 3

TIER_NAMES = {
    0: "Baseline Monitoring",
    1: "Elevated Public-Data Review",
    2: "High Public-Data Review Priority",
    3: "Claims Validation Candidate",
}

OVERLAP_LABELS = [
    ("none", "None"),
    ("network_only", "Network only"),
    ("enforcement_only", "Enforcement only"),
    ("investigation_only", "Complaint/investigation only"),
    ("network_enforcement", "Network + enforcement"),
    ("network_investigation", "Network + complaint/investigation"),
    ("enforcement_investigation", "Enforcement + complaint/investigation"),
    ("all_three", "All three"),
]


def find_first(*candidates):
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def overlap_key(network, enforcement, investigation):
    if network and enforcement and investigation:
        return "all_three"
    if network and enforcement:
        return "network_enforcement"
    if network and investigation:
        return "network_investigation"
    if enforcement and investigation:
        return "enforcement_investigation"
    if network:
        return "network_only"
    if enforcement:
        return "enforcement_only"
    if investigation:
        return "investigation_only"
    return "none"


def build():
    anon_dir = os.path.join(ROOT, "anonymized_data")
    facilities_path = os.path.join(anon_dir, "WA_AFH_3County_Enriched_ANON.csv")
    clusters_path = os.path.join(anon_dir, "WA_Operator_Clusters_ANON.csv")
    corrob_path = os.path.join(anon_dir, "WA_Operator_Clusters_Corroboration_ANON.csv")

    growth_path = find_first(
        os.path.join(ROOT, "wa_data_aggregate", "WA_AFH_Growth_2013_2026.csv"),
        os.path.join(ROOT, "data_package_with_everything", "wa_data", "WA_AFH_Growth_2013_2026.csv"),
    )

    facilities = read_csv(facilities_path)
    clusters = read_csv(clusters_path)
    corrob = read_csv(corrob_path)

    cluster_size = {r["cluster_id"]: int(r["n_licenses"]) for r in clusters}

    total_facilities = len(facilities)
    total_beds = sum(int(r["Licensed_Capacity"]) for r in facilities)
    enforcement_signal = sum(1 for r in facilities if int(r["n_enforcement"]) > 0)
    investigation_signal = sum(1 for r in facilities if int(r["n_investigations"]) > 0)
    in_cluster = sum(1 for r in facilities if r["cluster_id"].strip())

    # County-level aggregate summary (recomputed directly from facility-level file).
    county = defaultdict(lambda: {
        "facilities": 0, "beds": 0, "enforcement_signal": 0, "investigation_signal": 0,
        "facilities_in_operator_clusters": 0,
    })
    for r in facilities:
        c = county[r["County"]]
        c["facilities"] += 1
        c["beds"] += int(r["Licensed_Capacity"])
        if int(r["n_enforcement"]) > 0:
            c["enforcement_signal"] += 1
        if int(r["n_investigations"]) > 0:
            c["investigation_signal"] += 1
        if r["cluster_id"].strip():
            c["facilities_in_operator_clusters"] += 1
    county_summary = [{"county": k, **v} for k, v in sorted(county.items())]

    # Per-facility bucketed values (never written out row-by-row — only used
    # here, in memory, to build the aggregate cube and default-threshold views).
    def cluster_bucket_of(r):
        cid = r["cluster_id"].strip()
        if not cid:
            return 0
        return min(cluster_size.get(cid, 0), CLUSTER_BUCKET_CAP)

    def enforcement_bucket_of(r):
        return min(int(r["n_enforcement"]), ENFORCEMENT_BUCKET_CAP)

    def investigation_bucket_of(r):
        return min(int(r["n_investigations"]), INVESTIGATION_BUCKET_CAP)

    # Aggregate sensitivity cube: county x cluster_bucket x enforcement_bucket x
    # investigation_bucket -> facility count. Sufficient to recompute tier
    # counts and indicator-overlap counts for any allowed threshold combination
    # in the browser, without ever exposing a facility-level row.
    cube_counter = Counter()
    for r in facilities:
        key = (r["County"], cluster_bucket_of(r), enforcement_bucket_of(r), investigation_bucket_of(r))
        cube_counter[key] += 1
    sensitivity_cube = [
        {
            "county": county_,
            "cluster_bucket": cb,
            "enforcement_bucket": eb,
            "investigation_bucket": ib,
            "facilities": n,
        }
        for (county_, cb, eb, ib), n in sorted(cube_counter.items())
    ]

    # Default-threshold qualitative review-priority tiers and indicator overlap
    # — see PHASE1_PUBLIC_DATA_FRAMEWORK.md. Purely a convenience snapshot for
    # the dashboard's initial static view; the dashboard recomputes both from
    # sensitivity_cube for any other threshold/toggle combination in-browser.
    tier_counts = Counter()
    overlap_counts = Counter()
    network_true = enforcement_true = investigation_true = 0
    for r in facilities:
        network = cluster_bucket_of(r) >= DEFAULT_CLUSTER_SIZE_THRESHOLD
        enforcement = enforcement_bucket_of(r) >= DEFAULT_ENFORCEMENT_THRESHOLD
        investigation = investigation_bucket_of(r) >= DEFAULT_INVESTIGATION_THRESHOLD
        indicators = int(network) + int(enforcement) + int(investigation)
        tier_counts[TIER_NAMES[indicators]] += 1
        overlap_counts[overlap_key(network, enforcement, investigation)] += 1
        network_true += int(network)
        enforcement_true += int(enforcement)
        investigation_true += int(investigation)

    tier_summary = [{"tier": name, "facilities": tier_counts.get(name, 0)}
                     for name in TIER_NAMES.values()]
    indicator_overlap = [{"combination": label, "key": key, "facilities": overlap_counts.get(key, 0)}
                          for key, label in OVERLAP_LABELS]
    indicator_true_false = {
        "network_concentration": {"true": network_true, "false": total_facilities - network_true},
        "enforcement_intensity": {"true": enforcement_true, "false": total_facilities - enforcement_true},
        "complaint_investigation": {"true": investigation_true, "false": total_facilities - investigation_true},
    }

    # Aggregate cluster-size distribution (e.g. {"2": 57, "3": 12, "4": 3}).
    size_dist = Counter(str(v) for v in cluster_size.values())
    cluster_size_distribution = [{"cluster_size": k, "clusters": size_dist[k]}
                                  for k in sorted(size_dist, key=int)]

    # Aggregate corroboration summary.
    corroborated = sum(1 for r in corrob if r["corroboration_status"] == "Corroborated")
    corroboration_summary = {
        "clusters_evaluated": len(corrob),
        "corroborated": corroborated,
        "corroborated_pct": round(100 * corroborated / len(corrob), 1) if corrob else None,
    }

    growth_context = []
    if growth_path:
        for r in read_csv(growth_path):
            growth_context.append({
                "year": r["year"],
                "active_AFHs": r["active_AFHs"],
                "total_licensed_capacity": r["total_licensed_capacity"],
            })

    data = {
        "meta": {
            "title": "Phase 1 Public-Data Review-Priority Toolkit — Aggregate Dashboard Data",
            "notice": (
                "Illustrative sensitivity-analysis tool. Aggregate, de-identified public-data "
                "summary only. Not a validated model, not a fraud score, not an enforcement "
                "tool. No facility is identified anywhere in this file. See "
                "PHASE1_PUBLIC_DATA_FRAMEWORK.md for guardrails and tier definitions."
            ),
            "source_files": [
                "anonymized_data/WA_AFH_3County_Enriched_ANON.csv",
                "anonymized_data/WA_Operator_Clusters_ANON.csv",
                "anonymized_data/WA_Operator_Clusters_Corroboration_ANON.csv",
            ] + (["wa_data_aggregate/WA_AFH_Growth_2013_2026.csv" if "wa_data_aggregate" in (growth_path or "")
                  else "data_package_with_everything/wa_data/WA_AFH_Growth_2013_2026.csv"] if growth_path else []),
        },
        "headline": {
            "total_facilities": total_facilities,
            "total_beds": total_beds,
            "facilities_with_enforcement_signal": enforcement_signal,
            "facilities_with_investigation_signal": investigation_signal,
            "facilities_in_operator_clusters": in_cluster,
            "operator_cluster_count": len(clusters),
        },
        "county_summary": county_summary,
        "review_priority_tiers": tier_summary,
        "indicator_overlap": indicator_overlap,
        "indicator_true_false": indicator_true_false,
        "cluster_size_distribution": cluster_size_distribution,
        "corroboration_summary": corroboration_summary,
        "growth_context": growth_context,
        "sensitivity_cube": sensitivity_cube,
        "sensitivity_cube_dimensions": {
            "cluster_bucket_cap": CLUSTER_BUCKET_CAP,
            "enforcement_bucket_cap": ENFORCEMENT_BUCKET_CAP,
            "investigation_bucket_cap": INVESTIGATION_BUCKET_CAP,
            "note": (
                "A bucket value equal to its cap means 'this many or more'; below the cap "
                "it means exactly that many. Sufficient to recompute tier and overlap counts "
                "for any threshold in phase1_tier_config.json's allowed_values without "
                "exposing any facility-level row."
            ),
        },
        "default_thresholds": {
            "cluster_size_threshold": DEFAULT_CLUSTER_SIZE_THRESHOLD,
            "enforcement_count_threshold": DEFAULT_ENFORCEMENT_THRESHOLD,
            "investigation_count_threshold": DEFAULT_INVESTIGATION_THRESHOLD,
        },
    }
    return data


def render_dashboard_html(data, tier_config, out_dir):
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "phase1-dashboard.template.html"
    )
    if not os.path.isfile(template_path):
        return None
    with open(template_path, encoding="utf-8") as f:
        template = f.read()
    html = template.replace("__PHASE1_DATA_JSON__", json.dumps(data))
    html = html.replace("__PHASE1_TIER_CONFIG_JSON__", json.dumps(tier_config))
    out_path = os.path.join(out_dir, "phase1-dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


def build_tier_config():
    return {
        "meta": {
            "notice": (
                "All thresholds below are illustrative and non-validated. They configure an "
                "aggregate sensitivity-analysis display only; they are not a validated predictive "
                "model, and changing them does not create one. Sensitivity analysis is not an "
                "operational recommendation. Any operational use would require claims "
                "validation, human review, and due-process safeguards."
            ),
        },
        "default": {
            "cluster_size_threshold": DEFAULT_CLUSTER_SIZE_THRESHOLD,
            "enforcement_count_threshold": DEFAULT_ENFORCEMENT_THRESHOLD,
            "investigation_count_threshold": DEFAULT_INVESTIGATION_THRESHOLD,
        },
        "allowed_values": {
            "cluster_size_threshold": ALLOWED_CLUSTER_SIZE_THRESHOLDS,
            "enforcement_count_threshold": ALLOWED_ENFORCEMENT_THRESHOLDS,
            "investigation_count_threshold": ALLOWED_INVESTIGATION_THRESHOLDS,
        },
        "labels": {
            "cluster_size_threshold": "Network Concentration — minimum shared-contact cluster size (illustrative, non-validated)",
            "enforcement_count_threshold": "Enforcement Intensity — minimum formal enforcement actions on record (illustrative, non-validated)",
            "investigation_count_threshold": "Complaint/Investigation Load — minimum investigations on record (illustrative, non-validated)",
        },
    }


if __name__ == "__main__":
    data = build()
    tier_config = build_tier_config()

    out_dir = os.path.join(ROOT, "dashboard")
    os.makedirs(out_dir, exist_ok=True)

    data_path = os.path.join(out_dir, "phase1_dashboard_data.json")
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    config_path = os.path.join(out_dir, "phase1_tier_config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(tier_config, f, indent=2)

    html_path = render_dashboard_html(data, tier_config, out_dir)

    h = data["headline"]
    print("=== PHASE 1 DASHBOARD DATA BUILT ===")
    print(f"  Facilities: {h['total_facilities']}")
    print(f"  Beds: {h['total_beds']}")
    print(f"  Enforcement signal: {h['facilities_with_enforcement_signal']}")
    print(f"  Investigation signal: {h['facilities_with_investigation_signal']}")
    print(f"  In operator clusters: {h['facilities_in_operator_clusters']}")
    print(f"  Operator clusters: {h['operator_cluster_count']}")
    print(f"  Tiers (default thresholds): {dict((t['tier'], t['facilities']) for t in data['review_priority_tiers'])}")
    print(f"  Indicator overlap (default thresholds): {dict((o['key'], o['facilities']) for o in data['indicator_overlap'])}")
    print(f"  Sensitivity cube cells: {len(data['sensitivity_cube'])}")
    print(f"  Written: {data_path}")
    print(f"  Written: {config_path}")
    if html_path:
        print(f"  Dashboard HTML regenerated: {html_path}")
    else:
        print("  (dashboard template not found next to this script; HTML not regenerated)")
